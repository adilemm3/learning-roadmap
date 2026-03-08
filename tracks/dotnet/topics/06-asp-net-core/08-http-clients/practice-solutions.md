# HTTP Clients & IHttpClientFactory — Подсказки и решения

## Задача 1: Выбери тип клиента

<details><summary>Подсказка</summary>

Подумай: один сервис, несколько потребителей, нужна типобезопасность. Какой из трёх типов (Basic/Named/Typed) подходит лучше всего?

</details>

<details><summary>Решение</summary>

Typed client — рекомендуемый подход: типобезопасность, Single Responsibility, DI инжектит автоматически.

```csharp
// Typed client — отдельный класс, инкапсулирует работу с конкретным API.
// HttpClient приходит через constructor injection от IHttpClientFactory.
// Фабрика управляет пулом handler-ов — не нужно думать о socket exhaustion.
public class PushNotificationClient(HttpClient client)
{
    public async Task SendAsync(PushRequest request)
    {
        // PostAsJsonAsync — extension из System.Net.Http.Json.
        // Сериализует request в JSON и отправляет POST.
        // BaseAddress уже задан при регистрации — здесь только relative path.
        await client.PostAsJsonAsync("/notifications", request);
    }
}

// Регистрация в DI.
// AddHttpClient<T> делает три вещи:
// 1. Регистрирует PushNotificationClient как transient
// 2. При каждом resolve создаёт HttpClient с настроенным handler из пула
// 3. Handler ротируется каждые 2 минуты (дефолт) — решает проблему DNS
services.AddHttpClient<PushNotificationClient>(client =>
{
    // BaseAddress — общий префикс для всех запросов этого клиента.
    // Задаётся один раз при регистрации, не при каждом вызове.
    client.BaseAddress = new Uri("https://push.api.com");

    // Timeout — максимальное время ожидания ответа.
    // 15 секунд — разумный дефолт для push-уведомлений.
    client.Timeout = TimeSpan.FromSeconds(15);
});
```

**Почему не Named:** строковые ключи — риск опечаток, нет типобезопасности. Приходится резолвить через `IHttpClientFactory.CreateClient("name")`.

**Почему не Basic:** `new HttpClient()` напрямую — нет пула handler-ов, нет ротации DNS, нет централизованной конфигурации.

</details>

## Задача 2: Настрой таймауты

<details><summary>Подсказка</summary>

Два разных таймаута: `client.Timeout` — общий, `Policy.TimeoutAsync` — per-request внутри retry. Порядок регистрации политик определяет порядок выполнения (последний = внешний).

</details>

<details><summary>Решение</summary>

**Концепция:** Два уровня таймаутов. `client.Timeout` — потолок на всю операцию (включая все retry-попытки). `Policy.TimeoutAsync` — ограничение на каждую отдельную попытку внутри retry-цикла. Без per-request таймаута одна зависшая попытка съест весь общий таймаут.

```csharp
services.AddHttpClient<InventoryClient>(client =>
{
    client.BaseAddress = new Uri("https://inventory.api.com");

    // Общий таймаут — потолок на ВСЮ операцию.
    // Включает все retry-попытки + паузы между ними.
    // Если 3 retry по 10 сек + backoff (2+4+8=14 сек) = 44 сек < 60 сек — влезает.
    client.Timeout = TimeSpan.FromSeconds(60);
})
// Порядок регистрации: первый AddPolicy = внешний, последний = внутренний.
// Retry оборачивает Timeout: при таймауте одной попытки — retry делает следующую.
.AddTransientHttpErrorPolicy(p => p.WaitAndRetryAsync(
    retryCount: 3,
    // Exponential backoff: 2^1=2s, 2^2=4s, 2^3=8s.
    // Увеличивающиеся паузы дают серверу время на восстановление.
    sleepDurationProvider: attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt))))
// Per-request таймаут — ограничивает КАЖДУЮ отдельную попытку.
// Если сервер не ответил за 10 сек — попытка отменяется, retry начинает следующую.
.AddPolicyHandler(Policy.TimeoutAsync<HttpResponseMessage>(10));
```

**Порядок выполнения** (снаружи → внутрь): `client.Timeout(60s)` → `Retry(3)` → `Timeout(10s)` → HTTP запрос.

</details>

## Задача 3: Найди баг в тесте

<details><summary>Подсказка</summary>

Как создаётся `HttpClient`? Через фабрику или напрямую? Если напрямую — кто будет делать retry?

</details>

<details><summary>Решение</summary>

**Баг:** `mockHttp.ToHttpClient()` создаёт HttpClient напрямую, минуя `IHttpClientFactory`. Polly-политики регистрируются через `AddHttpClient<T>()` и встраиваются в pipeline фабрики. Если HttpClient создан вручную — pipeline не задействован, retry не работает.

**Почему тест «проходит»:** запрос идёт один раз, получает 500, `callCount = 1`. `Should().BeGreaterThan(1)` падает — но если `OrdersClient.GetOrder` бросает исключение на 500, то assert вообще не достигается, и тест падает по другой причине (не по retry).

```csharp
// Правильный подход: собрать реальный DI-контейнер с Polly-политиками,
// но подменить транспортный слой на mock.
var services = new ServiceCollection();

services.AddHttpClient<OrdersClient>(c =>
        c.BaseAddress = new Uri("https://orders.api.com"))
    // Retry-политика — 3 попытки, без пауз (TimeSpan.Zero) чтобы тест не ждал.
    // В проде будет exponential backoff, в тестах — мгновенные retry.
    .AddTransientHttpErrorPolicy(p =>
        p.WaitAndRetryAsync(3, _ => TimeSpan.Zero))
    // ConfigurePrimaryHttpMessageHandler подменяет ТРАНСПОРТ (самый нижний handler).
    // Polly-политики остаются в pipeline — запросы проходят через retry,
    // но вместо реального HTTP идут в mock.
    .ConfigurePrimaryHttpMessageHandler(() => mockHttp);

// BuildServiceProvider создаёт контейнер.
// GetRequiredService резолвит OrdersClient — фабрика создаёт HttpClient
// с полным pipeline: Retry → MockHttpMessageHandler.
var provider = services.BuildServiceProvider();
var ordersClient = provider.GetRequiredService<OrdersClient>();
```

**Ключевой принцип:** тестируй через тот же pipeline что и в проде. Подменяй только транспорт, не обходи middleware.

</details>

## Задача 4: Спроектируй Circuit Breaker

<details><summary>Подсказка</summary>

Проблема — retry storm. Нужен Circuit Breaker чтобы прекратить бомбардировку при системном сбое. Подумай: CB снаружи или внутри retry? Какой `durationOfBreak` если падение длится 2-5 мин?

</details>

<details><summary>Решение</summary>

**Концепция:** Retry storm — когда при падении сервиса каждый клиент делает N retry, умножая нагрузку. 8 инстансов × 4 попытки = 32 запроса на каждый вызов. Circuit Breaker «размыкает цепь» после серии ошибок — дальнейшие запросы получают мгновенный отказ (fast fail) без обращения к серверу. Через `durationOfBreak` CB пробует один запрос (Half-Open) — если успешен, замыкается обратно.

```csharp
services.AddHttpClient<ShippingClient>(client =>
{
    client.BaseAddress = new Uri("https://shipping.api.com");
    // Общий таймаут на всю операцию включая retry.
    client.Timeout = TimeSpan.FromSeconds(45);
})
// CB СНАРУЖИ retry — видит итоговый результат после всех попыток.
// Если retry справился (3-я попытка успешна) — CB не считает это ошибкой.
// CB внутри retry считал бы каждую неудачную попытку — ложные срабатывания.
.AddTransientHttpErrorPolicy(p => p.CircuitBreakerAsync(
    // После 5 последовательных ошибок (уже после retry) — размыкаем.
    // 5 а не 1 — чтобы единичные сбои не триггерили CB.
    handledEventsAllowedBeforeBreaking: 5,
    // 60 секунд паузы. API лежит 2-5 мин — за 60 сек Half-Open
    // попробует один запрос и узнает восстановился ли сервис.
    // Если нет — ещё 60 сек паузы. Итого ~2-5 циклов до восстановления.
    durationOfBreak: TimeSpan.FromSeconds(60)))
// Retry внутри CB — 3 попытки с exponential backoff.
.AddTransientHttpErrorPolicy(p => p.WaitAndRetryAsync(
    retryCount: 3,
    sleepDurationProvider: attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt))))
// Per-request таймаут — не ждать зависший запрос дольше 10 сек.
.AddPolicyHandler(Policy.TimeoutAsync<HttpResponseMessage>(10));
```

**Порядок выполнения:** CB → Retry → Timeout → HTTP.

**Эффект:**
- Без CB: 8 инстансов × 4 попытки = 32 запроса при каждом вызове
- С CB: после 5 провалов — 0 запросов на 60 сек, затем 1 пробный

</details>

## Задача 5: Идемпотентный retry для платежей

<details><summary>Подсказка</summary>

`AddTransientHttpErrorPolicy` ретраит все transient-ошибки включая таймаут. Нужна кастомная политика через `AddPolicyHandler` с явным фильтром — retry только на `HttpRequestException`. Для Idempotency-Key: `DelegatingHandler` добавляет заголовок перед каждым запросом.

</details>

<details><summary>Решение</summary>

**Концепция:** Платежи — неидемпотентные операции. Retry при таймауте опасен: запрос мог дойти до шлюза и списать деньги, а мы не получили ответ. Retry создаст двойное списание. Поэтому: retry только на сетевые ошибки (запрос гарантированно не дошёл) + Idempotency-Key для безопасного повтора (шлюз дедуплицирует по ключу).

```csharp
// Typed client — инкапсулирует взаимодействие с платёжным шлюзом.
public class PaymentGatewayClient(HttpClient client)
{
    public async Task<PaymentResult> ChargeAsync(ChargeRequest request)
    {
        // PostAsJsonAsync сериализует request и отправляет POST.
        // Idempotency-Key уже добавлен DelegatingHandler-ом ниже по pipeline.
        var response = await client.PostAsJsonAsync("/charges", request);

        // EnsureSuccessStatusCode бросает HttpRequestException на 4xx/5xx.
        // Polly-политика ниже перехватит 5xx для retry.
        response.EnsureSuccessStatusCode();

        return await response.Content.ReadFromJsonAsync<PaymentResult>()!;
    }
}

// DelegatingHandler — middleware в pipeline HttpClient.
// Выполняется ДО Polly-политик и ДО транспорта.
// При retry — SendAsync DelegatingHandler вызывается ОДИН раз,
// retry повторяет base.SendAsync (транспорт), а не весь pipeline.
// Поэтому Guid.NewGuid() генерируется один раз на запрос, не на каждый retry.
public class IdempotencyKeyHandler : DelegatingHandler
{
    protected override async Task<HttpResponseMessage> SendAsync(
        HttpRequestMessage request, CancellationToken cancellationToken)
    {
        // Idempotency-Key нужен только для мутирующих операций.
        // GET идемпотентен по определению — ключ не нужен.
        if (request.Method == HttpMethod.Post || request.Method == HttpMethod.Put)
        {
            // Шлюз дедуплицирует запросы с одинаковым ключом.
            // Если retry отправит тот же запрос — шлюз вернёт результат первого.
            request.Headers.TryAddWithoutValidation(
                "Idempotency-Key", Guid.NewGuid().ToString());
        }
        return await base.SendAsync(request, cancellationToken);
    }
}

// --- Регистрация ---

// DelegatingHandler регистрируется как transient — новый экземпляр на каждый запрос.
services.AddTransient<IdempotencyKeyHandler>();

services.AddHttpClient<PaymentGatewayClient>(client =>
{
    client.BaseAddress = new Uri(configuration["PaymentGateway:BaseUrl"]!);
    // Общий таймаут — потолок на всю операцию.
    client.Timeout = TimeSpan.FromSeconds(30);
})
// AddHttpMessageHandler встраивает IdempotencyKeyHandler в pipeline.
// Порядок: IdempotencyKeyHandler → CB → Retry → Timeout → Transport.
.AddHttpMessageHandler<IdempotencyKeyHandler>()
// CB снаружи — при системном падении шлюза fast fail.
.AddTransientHttpErrorPolicy(p => p.CircuitBreakerAsync(
    handledEventsAllowedBeforeBreaking: 5,
    durationOfBreak: TimeSpan.FromSeconds(30)))
// КАСТОМНАЯ retry-политика вместо AddTransientHttpErrorPolicy.
// AddTransientHttpErrorPolicy ретраит ВСЕ transient-ошибки включая таймаут.
// Для платежей таймаут НЕ должен вызывать retry — операция могла выполниться.
.AddPolicyHandler(Policy
    // HttpRequestException — сетевые ошибки: connection refused, DNS failure.
    // Запрос гарантированно НЕ дошёл до сервера — retry безопасен.
    .Handle<HttpRequestException>()
    // 5xx — сервер получил запрос но упал при обработке.
    // С Idempotency-Key retry безопасен — шлюз дедуплицирует.
    .OrResult<HttpResponseMessage>(r =>
        r.StatusCode >= HttpStatusCode.InternalServerError)
    // НЕ перечислен TimeoutRejectedException — при таймауте retry НЕ будет.
    .WaitAndRetryAsync(3, attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt))))
// Per-request таймаут — ограничивает каждую отдельную попытку.
.AddPolicyHandler(Policy.TimeoutAsync<HttpResponseMessage>(10));
```

**Ключевые решения:**
- **Кастомная retry-политика** — явный фильтр `HttpRequestException` + 5xx, без `TimeoutRejectedException`
- **IdempotencyKeyHandler** — один ключ на запрос, не на retry (DelegatingHandler вызывается один раз)
- **CB снаружи** — fast fail при системном падении, не бомбардировать умирающий шлюз

</details>
