# HTTP Clients & IHttpClientFactory — Практика

<!-- 5 новых задач для самостоятельной отработки -->
<!-- Задачи из учебных сессий — в session.md -->

## Задача 1: Выбери тип клиента
> Сложность: Easy | Тип: архитектура

У тебя есть `NotificationService`, который отправляет push-уведомления через внешний API (`https://push.api.com`). Сервис используется в 3 контроллерах. Какой тип HTTP-клиента выбрать и почему? Напиши регистрацию в DI.

<details><summary>Подсказка</summary>

Подумай: один сервис, несколько потребителей, нужна типобезопасность. Какой из трёх типов (Basic/Named/Typed) подходит лучше всего?

</details>

<details><summary>Решение</summary>

Typed client — рекомендуемый подход: типобезопасность, Single Responsibility, DI инжектит автоматически.

```csharp
public class PushNotificationClient(HttpClient client)
{
    public async Task SendAsync(PushRequest request)
    {
        await client.PostAsJsonAsync("/notifications", request);
    }
}

services.AddHttpClient<PushNotificationClient>(client =>
{
    client.BaseAddress = new Uri("https://push.api.com");
    client.Timeout = TimeSpan.FromSeconds(15);
});
```

Named client подошёл бы тоже, но строковые ключи — риск опечаток. Basic — слишком примитивен для повторного использования.

</details>

## Задача 2: Настрой таймауты
> Сложность: Easy | Тип: реализация

Настрой HTTP-клиент `InventoryClient` так, чтобы:
- Общий таймаут на весь запрос (включая retry): 60 секунд
- Таймаут на каждую отдельную попытку: 10 секунд
- 3 retry с exponential backoff

<details><summary>Подсказка</summary>

Два разных таймаута: `client.Timeout` — общий, `Policy.TimeoutAsync` — per-request внутри retry. Порядок регистрации политик определяет порядок выполнения (последний = внешний).

</details>

<details><summary>Решение</summary>

```csharp
services.AddHttpClient<InventoryClient>(client =>
{
    client.BaseAddress = new Uri("https://inventory.api.com");
    client.Timeout = TimeSpan.FromSeconds(60); // общий таймаут включая все retry
})
.AddTransientHttpErrorPolicy(p => p.WaitAndRetryAsync(
    retryCount: 3,
    sleepDurationProvider: attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt))))
.AddPolicyHandler(Policy.TimeoutAsync<HttpResponseMessage>(10)); // per-request
```

Порядок выполнения (снаружи → внутрь): Retry → Timeout(10s) → HTTP запрос.
`client.Timeout = 60s` — ограничивает всю цепочку сверху.

</details>

## Задача 3: Найди баг в тесте
> Сложность: Medium | Тип: дебаг

Тест проверяет retry, но всегда проходит даже когда retry отключен. Найди почему:

```csharp
[Fact]
public async Task GetOrder_Retries_On500()
{
    var callCount = 0;
    var mockHttp = new MockHttpMessageHandler();

    mockHttp
        .When("/orders/42")
        .Respond(_ =>
        {
            callCount++;
            return callCount < 3
                ? new HttpResponseMessage(HttpStatusCode.InternalServerError)
                : new HttpResponseMessage(HttpStatusCode.OK)
                  {
                      Content = new StringContent("""{"id": 42}""",
                          Encoding.UTF8, "application/json")
                  };
        });

    var client = mockHttp.ToHttpClient();
    client.BaseAddress = new Uri("https://orders.api.com");
    var ordersClient = new OrdersClient(client);

    var order = await ordersClient.GetOrder(42);

    order.Should().NotBeNull();
    callCount.Should().BeGreaterThan(1);
}
```

<details><summary>Подсказка</summary>

Как создаётся `HttpClient`? Через фабрику или напрямую? Если напрямую — кто будет делать retry?

</details>

<details><summary>Решение</summary>

Баг: `mockHttp.ToHttpClient()` создаёт HttpClient напрямую, без `IHttpClientFactory` и без Polly-политик. Retry не подключён — запрос идёт один раз, получает 500, `OrdersClient` либо бросает исключение, либо возвращает null. Тест проходит потому что `callCount = 1 > 1` — false, но `Should().BeGreaterThan(1)` может не быть достигнут если перед ним исключение.

Исправление — использовать `ServiceCollection` + `ConfigurePrimaryHttpMessageHandler`:

```csharp
var services = new ServiceCollection();
services.AddHttpClient<OrdersClient>(c =>
        c.BaseAddress = new Uri("https://orders.api.com"))
    .AddTransientHttpErrorPolicy(p =>
        p.WaitAndRetryAsync(3, _ => TimeSpan.Zero))
    .ConfigurePrimaryHttpMessageHandler(() => mockHttp);

var provider = services.BuildServiceProvider();
var ordersClient = provider.GetRequiredService<OrdersClient>();
```

</details>

## Задача 4: Спроектируй Circuit Breaker
> Сложность: Medium | Тип: архитектура

Сервис `ShippingClient` вызывает API доставки. В пиковые часы API иногда лежит по 2-5 минут. Сейчас при падении API все 8 инстансов сервиса делают по 3 retry каждый → API не может восстановиться.

Спроектируй resilience-стратегию: какие политики, в каком порядке, с какими параметрами?

<details><summary>Подсказка</summary>

Проблема — retry storm. Нужен Circuit Breaker чтобы прекратить бомбардировку при системном сбое. Подумай: CB снаружи или внутри retry? Какой `durationOfBreak` если падение длится 2-5 мин?

</details>

<details><summary>Решение</summary>

```csharp
services.AddHttpClient<ShippingClient>(client =>
{
    client.BaseAddress = new Uri("https://shipping.api.com");
    client.Timeout = TimeSpan.FromSeconds(45);
})
.AddTransientHttpErrorPolicy(p => p.CircuitBreakerAsync(
    handledEventsAllowedBeforeBreaking: 5,
    durationOfBreak: TimeSpan.FromSeconds(60)))
.AddTransientHttpErrorPolicy(p => p.WaitAndRetryAsync(
    retryCount: 3,
    sleepDurationProvider: attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt))))
.AddPolicyHandler(Policy.TimeoutAsync<HttpResponseMessage>(10));
```

Порядок: CB (снаружи) → Retry → Timeout (внутри).

- CB снаружи видит итоги retry-серий. Если retry справился — CB не считает ошибкой.
- `durationOfBreak: 60s` — даёт API минуту на восстановление. Half-Open пропустит 1 пробный запрос.
- Без CB: 8 инстансов × 4 попытки = 32 запроса при каждом вызове. С CB: после 5 провалов — 0 запросов на 60 сек.

</details>

## Задача 5: Идемпотентный retry для платежей
> Сложность: Hard | Тип: архитектура

`PaymentGatewayClient` отправляет запросы на списание средств. Требования:
1. Retry при сетевых ошибках (connection refused, DNS failure)
2. НЕ retry при таймауте (операция могла выполниться)
3. Поддержка Idempotency-Key для безопасного retry
4. Circuit Breaker при системном падении шлюза

Напиши typed client + регистрацию с Polly-политиками + DelegatingHandler для Idempotency-Key.

<details><summary>Подсказка</summary>

`AddTransientHttpErrorPolicy` ретраит все transient-ошибки включая таймаут. Нужна кастомная политика через `AddPolicyHandler` с явным фильтром — retry только на `HttpRequestException`. Для Idempotency-Key: `DelegatingHandler` добавляет заголовок перед каждым запросом.

</details>

<details><summary>Решение</summary>

```csharp
public class PaymentGatewayClient(HttpClient client)
{
    public async Task<PaymentResult> ChargeAsync(ChargeRequest request)
    {
        var response = await client.PostAsJsonAsync("/charges", request);
        response.EnsureSuccessStatusCode();
        return await response.Content.ReadFromJsonAsync<PaymentResult>()!;
    }
}

public class IdempotencyKeyHandler : DelegatingHandler
{
    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request, CancellationToken cancellationToken)
    {
        if (request.Method == HttpMethod.Post || request.Method == HttpMethod.Put)
        {
            request.Headers.TryAddWithoutValidation("Idempotency-Key", Guid.NewGuid().ToString());
        }
        return await base.SendAsync(request, cancellationToken);
    }
}

// Регистрация
services.AddTransient<IdempotencyKeyHandler>();

services.AddHttpClient<PaymentGatewayClient>(client =>
{
    client.BaseAddress = new Uri(configuration["PaymentGateway:BaseUrl"]!);
    client.Timeout = TimeSpan.FromSeconds(30);
})
.AddHttpMessageHandler<IdempotencyKeyHandler>()
.AddTransientHttpErrorPolicy(p => p.CircuitBreakerAsync(
    handledEventsAllowedBeforeBreaking: 5,
    durationOfBreak: TimeSpan.FromSeconds(30)))
.AddPolicyHandler(Policy
    .Handle<HttpRequestException>()            // только сетевые ошибки
    .OrResult<HttpResponseMessage>(r =>
        r.StatusCode >= HttpStatusCode.InternalServerError)
    .WaitAndRetryAsync(3, attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt))))
.AddPolicyHandler(Policy.TimeoutAsync<HttpResponseMessage>(10));
```

Ключевые решения:
- **Кастомная retry-политика** вместо `AddTransientHttpErrorPolicy` — явно фильтрует `HttpRequestException` (сетевые) и 5xx, но НЕ `TimeoutRejectedException`
- **IdempotencyKeyHandler** как `DelegatingHandler` — добавляется в pipeline до Polly, каждый retry получает тот же заголовок через цепочку handler-ов
- **CB снаружи** — при системном падении шлюза fast fail, не бомбардировать

Нюанс: `Guid.NewGuid()` генерирует новый ключ на каждый **запрос** (не на каждый retry). `DelegatingHandler.SendAsync` вызывается один раз — retry повторяет `base.SendAsync`, не пересоздавая handler-цепочку.

</details>
