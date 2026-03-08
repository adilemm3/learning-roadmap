# HTTP Clients & IHttpClientFactory — Практика

> Подсказки и решения → `practice-solutions.md`

## Задача 1: Выбери тип клиента
> Сложность: Easy | Тип: архитектура

У тебя есть `NotificationService`, который отправляет push-уведомления через внешний API (`https://push.api.com`). Сервис используется в 3 контроллерах. Какой тип HTTP-клиента выбрать и почему? Напиши регистрацию в DI.

## Задача 2: Настрой таймауты
> Сложность: Easy | Тип: реализация

Настрой HTTP-клиент `InventoryClient` так, чтобы:
- Общий таймаут на весь запрос (включая retry): 60 секунд
- Таймаут на каждую отдельную попытку: 10 секунд
- 3 retry с exponential backoff

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

## Задача 4: Спроектируй Circuit Breaker
> Сложность: Medium | Тип: архитектура

Сервис `ShippingClient` вызывает API доставки. В пиковые часы API иногда лежит по 2-5 минут. Сейчас при падении API все 8 инстансов сервиса делают по 3 retry каждый → API не может восстановиться.

Спроектируй resilience-стратегию: какие политики, в каком порядке, с какими параметрами?

## Задача 5: Идемпотентный retry для платежей
> Сложность: Hard | Тип: архитектура

`PaymentGatewayClient` отправляет запросы на списание средств. Требования:
1. Retry при сетевых ошибках (connection refused, DNS failure)
2. НЕ retry при таймауте (операция могла выполниться)
3. Поддержка Idempotency-Key для безопасного retry
4. Circuit Breaker при системном падении шлюза

Напиши typed client + регистрацию с Polly-политиками + DelegatingHandler для Idempotency-Key.
