# HTTP Clients & IHttpClientFactory — Шпаргалка

## Проблема и решение

| Проблема | Причина | Решение |
|----------|---------|---------|
| Port exhaustion | `new HttpClient()` per request → TIME_WAIT 4 мин | `IHttpClientFactory` |
| DNS не обновляется | `static HttpClient` — handler живёт вечно | Ротация handler каждые 2 мин |
| Race condition | `DefaultRequestHeaders` не потокобезопасен | Настройка при регистрации, не использовании |

## Три типа клиентов

```csharp
// Basic
services.AddHttpClient();
var client = factory.CreateClient(); // ❌ настройка при использовании

// Named
services.AddHttpClient("orders", c => { c.BaseAddress = new Uri("..."); });
var client = factory.CreateClient("orders");

// Typed ✅ рекомендуется
public class OrdersClient(HttpClient client) { ... }
services.AddHttpClient<OrdersClient>(c => { c.BaseAddress = new Uri("..."); });
// DI инжектит автоматически
```

## Polly — порядок политик

```csharp
services.AddHttpClient<OrdersClient>()
    .AddTransientHttpErrorPolicy(p => p.CircuitBreakerAsync(
        handledEventsAllowedBeforeBreaking: 5,  // 5 подряд провалов → Open
        durationOfBreak: TimeSpan.FromSeconds(30))) // 30с пауза → Half-Open
    .AddTransientHttpErrorPolicy(p => p.WaitAndRetryAsync(
        retryCount: 3,
        sleepDurationProvider: attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt))))
    .AddPolicyHandler(Policy.TimeoutAsync<HttpResponseMessage>(10)); // per-request
```

Порядок выполнения (снаружи → внутрь):
```
CircuitBreaker → Retry → Timeout(10s) → HTTP запрос
```

## Circuit Breaker — состояния

```
Closed → (5 ошибок подряд) → Open → (30с) → Half-Open → (успех) → Closed
                                              ↓ (ошибка) → Open
```
В Open state: `BrokenCircuitException`, запрос НЕ уходит на сервер.

## Тестирование

```csharp
var mockHttp = new MockHttpMessageHandler();
mockHttp.When("/orders/42").Respond(HttpStatusCode.OK, "application/json", """{"id":42}""");

// Простой тест
var client = mockHttp.ToHttpClient();
client.BaseAddress = new Uri("https://api.com");

// С IHttpClientFactory + Polly
services.AddHttpClient<OrdersClient>(c => c.BaseAddress = new Uri("https://api.com"))
    .AddTransientHttpErrorPolicy(p => p.WaitAndRetryAsync(3, _ => TimeSpan.Zero))
    .ConfigurePrimaryHttpMessageHandler(() => mockHttp);
```

## Антипаттерны

```csharp
// ❌ static HttpClient — DNS не обновляется + race condition
private static readonly HttpClient _client = new HttpClient();

// ❌ new HttpClient() per request — port exhaustion
using var client = new HttpClient();

// ❌ AddSingleton<TypedClient> — перезаписывает transient, handler не ротируется
services.AddSingleton<OrdersClient>();

// ❌ Настройка при использовании
_client.BaseAddress = new Uri("..."); // race condition!

// ❌ Секрет в коде
client.DefaultRequestHeaders.Add("X-Api-Key", "hardcoded-secret");
```

## Retry для критических операций

Retry **только на сетевые ошибки** (connection refused, DNS), **не на таймаут** — операция могла частично выполниться.
`Idempotency-Key` → retry безопасен на всё если сервис поддерживает.
