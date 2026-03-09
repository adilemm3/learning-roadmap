---
# HTTP Clients & IHttpClientFactory — Сессии

## Сессия 1 — 2026-03-05

### Калибровка

**Claude:** Зачем вообще нужен `HttpClient`? Что он делает и когда ты его используешь?

**Адиль:** он нужен для работы с запросами к удаленным ресурсам по http https протоколу. По сути обертка для работы с запросами

→ ✅

**Claude:** Есть известная проблема с `HttpClient` — если создавать его через `new HttpClient()` на каждый запрос, возникает серьёзная проблема. Что это за проблема?

**Адиль:** исчерпания пула конекшенов?

→ ✅ (socket exhaustion — верно)

**Claude:** `IHttpClientFactory` решает эту проблему. Как именно — знаешь механизм? Что у него «под капотом»?

**Адиль:** у него есть пул конекшенов, при завершения запроса конекшен возвращается в пул и может быть переиспользован

→ ✅ частично (знает про переиспользование, не знал деталей про HttpMessageHandler)

**Результат калибровки:** Middle-, знает проблему, детали механизма не раскрыты

---

### Блок 1: HttpClient под капотом

**Claude:**

Аналогия: Представь `HttpClient` как таксиста, а `HttpMessageHandler` — как автомобиль. Таксисты приходят и уходят, но машины дорогие — их держат в парке и переиспользуют. Создавать новую машину на каждую поездку — расточительство.

Техническая картина:

```
HttpClient
    └── HttpMessageHandler (держит TCP-соединение)
            └── SocketsHttpHandler (реальная работа с сокетами)
```

Когда ты делаешь `new HttpClient()`:
- создаётся новый `HttpMessageHandler`
- а значит новое TCP-соединение
- после `Dispose()` сокет уходит в `TIME_WAIT` (~4 минуты)
- при высокой нагрузке — port exhaustion

Что делает `IHttpClientFactory`:

```csharp
// Регистрация в DI
services.AddHttpClient();

// Использование
public class MyService
{
    private readonly HttpClient _client;

    public MyService(IHttpClientFactory factory)
    {
        _client = factory.CreateClient();
    }
}
```

Фабрика держит **пул `HttpMessageHandler`-ов**. Каждый `CreateClient()` создаёт новый лёгкий `HttpClient`, но **переиспользует handler** из пула. Handlers ротируются каждые **2 минуты** — так DNS-изменения подхватываются без потери производительности.

```
IHttpClientFactory
    ├── HttpClient (новый каждый раз — лёгкий, без состояния)
    └── HttpMessageHandler Pool
            ├── Handler A (активен, создан 1 мин назад)
            ├── Handler B (активен, создан 30 сек назад)
            └── Handler C (истёк, ждёт завершения запросов)
```

★ Insight:
- **Связь:** `HttpMessageHandler` — это Chain of Responsibility из паттернов (блок 03-behavioral). `DelegatingHandler` — middleware для HTTP-запросов, точно как ASP.NET Middleware Pipeline
- **Нюанс:** `HttpClient` потокобезопасен для отправки запросов, но `BaseAddress` и `DefaultRequestHeaders` — нет. Поэтому typed clients настраиваются **при регистрации**, а не при использовании
- **Собес:** «Почему нельзя делать `new HttpClient()` на каждый запрос?» — классический вопрос на Middle. Правильный ответ: socket exhaustion через `TIME_WAIT`, решение — `IHttpClientFactory` с пулом handler-ов

#### Проверка Блока 1

**Claude:** Q1: `IHttpClientFactory` ротирует handlers каждые 2 минуты. Зачем? Что плохого в том, чтобы держать один handler вечно?

**Адиль:** чтоб сбросить сокет?

→ ❌

**Claude:** Не совсем — сокет тут не главная причина. Подумай вот о чём: `HttpMessageHandler` держит соединение открытым и кэширует DNS-резолюцию. Что произойдёт, если IP-адрес сервиса изменится (например, при failover или ротации load balancer), а handler живёт вечно?

**Адиль:** будет пытаться отправить запрос и упадет так как адрес изменился

→ ✅ Ротация каждые 2 минуты — компромисс: достаточно редко чтобы переиспользовать соединения, достаточно часто чтобы подхватывать DNS-изменения.

**Claude:** Q2: У тебя есть сервис `OrderService`, который делает запросы к внешнему API. Почему плохая идея хранить `HttpClient` как `static` поле класса?

**Адиль:** связано с временем жизни сервиса?

→ ❌ (направление верное, но не конкретно)

**Claude:** Близко — направление верное. Конкретизируй: что именно сломается если `HttpClient` статический? Вспомни про `BaseAddress` и `DefaultRequestHeaders` — они потокобезопасны?

**Адиль:** изза этого не получится обновить ip адрес при смене

→ ❌ (это тоже проблема, но другая)

**Claude:** Это тоже проблема (та же DNS-история), но есть ещё одна — про потокобезопасность. `BaseAddress` и `DefaultRequestHeaders` не потокобезопасны. Если два потока одновременно захотят изменить заголовки на статическом клиенте — что произойдёт?

**Адиль:** рейс кондишн

→ ✅ Именно — race condition. Два потока одновременно меняют `DefaultRequestHeaders` → непредсказуемое поведение или исключение.

Вот почему правило: **`HttpClient` настраивай при регистрации в DI, а не при использовании.**

```csharp
// ✅ Правильно — настройка при регистрации
services.AddHttpClient<OrderService>(client =>
{
    client.BaseAddress = new Uri("https://api.example.com");
    client.DefaultRequestHeaders.Add("X-Api-Key", "secret");
});

// ❌ Неправильно — настройка при использовании
public async Task GetOrder()
{
    _client.BaseAddress = new Uri("https://api.example.com"); // race condition!
}
```

**Микрофидбек:** частично → после доп. объяснения понял ✅

#### ↳ Углубление: port exhaustion (тип: уточнение)

**Адиль:** port exhaustion — хочу понять подробнее

**Claude:**

Как работают TCP-соединения: Когда ты делаешь HTTP-запрос, ОС открывает сокет — это пара `(локальный_порт, удалённый_адрес)`. Локальных портов у ОС около **65 000**, и они не бесконечны.

```
Запрос 1: localhost:51234 → api.example.com:443
Запрос 2: localhost:51235 → api.example.com:443
Запрос 3: localhost:51236 → api.example.com:443
...
```

Проблема с `new HttpClient()` на каждый запрос:

```csharp
// Это делается 1000 раз в секунду
using var client = new HttpClient();
await client.GetAsync("https://api.example.com/orders");
// Dispose() закрывает HttpClient, но сокет НЕ освобождается сразу
```

После `Dispose()` сокет уходит в состояние `TIME_WAIT` — ОС держит его ещё ~4 минуты, ожидая «запоздавших» пакетов. За это время порт **занят и недоступен**.

```
Порт 51234 → TIME_WAIT (занят 4 мин)
Порт 51235 → TIME_WAIT (занят 4 мин)
...
Порт 65000 → TIME_WAIT (занят 4 мин)
❌ Новых портов нет → SocketException: "Only one usage of each socket address is permitted"
```

Решение — переиспользовать handler:

```
IHttpClientFactory
    └── Handler (одно соединение, живёт 2 мин)
            ├── Запрос 1  ↗
            ├── Запрос 2  ↗  // все через одно соединение (HTTP/2 multiplexing)
            └── Запрос 3  ↗
```

Один handler → одно TCP-соединение → один порт на все запросы к одному хосту.

**Адиль:** а когда проходит две минуты что происходит?

**Claude:**

Ротация происходит аккуратно, не обрывая активные запросы:

```
t=0:00  Handler A создан, активен
t=2:00  Handler A помечается как "истёкший" (expired)
        Handler B создан — новые запросы идут через него
t=2:00+ Handler A ещё жив — доделывает текущие запросы
t=2:xx  Handler A завершил все запросы → Dispose() → порт освобождён
```

Два шага:
1. **Expire** — handler перестаёт принимать новые запросы
2. **Dispose** — handler уничтожается когда завершил все текущие

Никаких обрывов — graceful shutdown на уровне соединений.

**Адиль:** он диспоузится изза днс? тут сокет сразу закрывается?

**Claude:** Да, handler диспоузится в том числе из-за DNS-причин (ротация каждые 2 мин). Но вот ключевое отличие:

```
new HttpClient() на каждый запрос:
  Запрос → новый сокет → TIME_WAIT → занят 4 мин
  (происходит 1000 раз/сек → port exhaustion)

IHttpClientFactory:
  Handler живёт 2 мин → обрабатывает 1000 запросов через ОДИН сокет
  Handler истёк → Dispose() → сокет закрывается (TIME_WAIT)
  (происходит раз в 2 мин → 1 сокет в TIME_WAIT вместо 1000)
```

Сокет всё равно идёт в `TIME_WAIT` при Dispose — но **раз в 2 минуты**, а не на каждый запрос. Разница в частоте — вот почему проблема исчезает.

---

### Блок 2: IHttpClientFactory — типы клиентов

**Claude:**

Аналогия: Представь три способа заказать такси. **Basic** — вызываешь диспетчера каждый раз и говоришь куда ехать. **Named** — у диспетчера есть список настроенных маршрутов по имени («повези меня как обычно в аэропорт»). **Typed** — у тебя есть персональный водитель с уже прописанным маршрутом, которого тебе даёт DI-контейнер.

**Basic client:**

```csharp
// Регистрация
services.AddHttpClient();

// Использование — каждый раз создаёшь вручную
public class OrderService(IHttpClientFactory factory)
{
    public async Task<string> GetOrder(int id)
    {
        var client = factory.CreateClient();
        client.BaseAddress = new Uri("https://api.example.com"); // ❌ небезопасно
        return await client.GetStringAsync($"/orders/{id}");
    }
}
```

Проблема: настройка при использовании — race condition если кто-то шарит клиент.

**Named client:**

```csharp
// Регистрация — настройка один раз
services.AddHttpClient("orders", client =>
{
    client.BaseAddress = new Uri("https://orders.api.com");
    client.DefaultRequestHeaders.Add("X-Api-Key", "secret");
    client.Timeout = TimeSpan.FromSeconds(30);
});

// Использование
var client = factory.CreateClient("orders"); // по имени
```

Удобно когда один клиент нужен в нескольких местах. Минус: строковые ключи — опечатки не поймает компилятор.

**Typed client ✅ (рекомендуемый подход):**

```csharp
// Типизированный клиент — отдельный класс
public class OrdersClient(HttpClient client)
{
    public async Task<Order> GetOrder(int id) =>
        await client.GetFromJsonAsync<Order>($"/orders/{id}");
}

// Регистрация
services.AddHttpClient<OrdersClient>(client =>
{
    client.BaseAddress = new Uri("https://orders.api.com");
    client.Timeout = TimeSpan.FromSeconds(30);
});

// Использование — DI сам инжектит
public class OrderService(OrdersClient ordersClient) { ... }
```

Typed client регистрируется как **transient** — каждый раз новый экземпляр, но handler переиспользуется из пула (блок 1).

★ Insight:
- **Связь:** Typed client — это применение принципа Single Responsibility из SOLID: отдельный класс отвечает только за HTTP-коммуникацию с конкретным сервисом. Named client нарушает это — логика размазана по потребителям
- **Нюанс:** Typed client нельзя регистрировать как singleton — тогда `HttpClient` внутри него тоже станет singleton, а handler не будет ротироваться (DNS-проблема из блока 1). Всегда transient или scoped
- **Собес:** «Какие типы HTTP-клиентов есть в .NET и когда что выбрать?» — ожидают что назовёшь все три и объяснишь trade-off

#### Проверка Блока 2

**Claude:** Q1: Typed client регистрируется как transient. Что будет если зарегистрировать его как singleton?

**Адиль:** handler не будет ротироваться, DNS не обновится, упадёт

→ ✅

**Claude:** Что именно подхватывается из DNS?

**Адиль:** будет идти по старому айпи, будет падать. какие данные подхватываются с днс?

**Claude:** Подхватывается одно главное: **IP-адрес хоста**. DNS резолвит доменное имя → IP. Если сервис переехал на новый IP (failover, ротация в load balancer, Kubernetes перезапустил pod) — старый handler будет стучаться на мёртвый адрес.

**Claude:** Q2: Посмотри на этот код — найди проблему:

```csharp
services.AddHttpClient<PaymentClient>(client =>
{
    client.BaseAddress = new Uri("https://payments.api.com");
});

services.AddSingleton<PaymentClient>();
```

**Адиль:** синглтон зарезолвлен не проставлен таймаут

→ ❌ (таймаут не проблема)

**Claude:** `AddHttpClient<PaymentClient>` уже регистрирует `PaymentClient` как **transient**. Что делает вторая строка `AddSingleton<PaymentClient>()`?

**Адиль:** регистрирует контейнер как синглтон

→ ✅ перезаписывает transient → handler не ротируется → DNS-проблема

**Claude:** Правильно так:

```csharp
// Достаточно одной строки — AddHttpClient сам регистрирует как transient
services.AddHttpClient<PaymentClient>(client =>
{
    client.BaseAddress = new Uri("https://payments.api.com");
});
```

**Микрофидбек:** да ✅

#### ↳ Углубления (уточнения в рамках блока)

**Адиль:** это два способа регистрации? если написать addTransient? также как происходит перезапись регистрации под капотом?

**Claude — AddTransient vs AddHttpClient:**

`AddTransient<PaymentClient>()` — просто регистрирует класс. При резолве DI попытается найти `HttpClient` в контейнере — а там либо ненастроенный дефолтный, либо вообще ничего. `AddHttpClient<T>` делает три вещи:
1. Регистрирует T как transient
2. Регистрирует **фабрику** — при создании T DI вызывает `IHttpClientFactory.CreateClient("PaymentClient")` и инжектит настроенный `HttpClient`
3. Привязывает конфигурацию (`BaseAddress`, заголовки) к этому имени

**Claude — перезапись под капотом:**

DI-контейнер хранит список `ServiceDescriptor`-ов:

```csharp
// IServiceCollection — это просто List<ServiceDescriptor>
[
  ServiceDescriptor { ServiceType = PaymentClient, Lifetime = Transient, ... }, // AddHttpClient
  ServiceDescriptor { ServiceType = PaymentClient, Lifetime = Singleton, ... }, // AddSingleton
]
```

При резолве берётся **последний** дескриптор для типа. Первый остаётся в списке, но игнорируется. Никакого merge — просто приоритет последнего.

```csharp
var descriptors = services.Where(d => d.ServiceType == typeof(PaymentClient));
// Вернёт оба, но реально используется последний
```

**Адиль:** мне кажется ты делаешь блоки маленькими? каким образом ты определяешь что блок нужно завершать?

**Claude:** Блок заканчивается когда: объяснение дано, 2-3 проверочных вопроса пройдены, микрофидбек получен. Структура фиксированная. Твоё замечание справедливо — блок 1 получился узким. Оставили 5 блоков как есть.

**Адиль:** а где ты хранишь эти блоки?

**Claude:** В `learning-plan.md`. Plan был сгенерирован в голове, но в файл не записан сразу — пробел исправлен: сохранили план через агента, и обновили SKILL.md чтобы план записывался немедленно при генерации.

**Адиль:** думаю план обучения должен быть изменен фоново сразу при генерации

**Claude:** Ты прав — исправил: план сохраняется через фонового агента сразу после генерации, до начала блока 1. Зафиксировано в SKILL.md.

---

### Блок 3: Polly & Resilience

**Claude:**

Аналогия: Представь курьера который доставляет посылки. **Retry** — если дверь закрыта, подожди и попробуй снова. **Circuit Breaker** — если курьер три раза подряд получил отказ, он не едет туда час — чтобы не тратить бензин впустую. **Timeout** — курьер не ждёт у двери вечно, максимум 30 секунд.

**Retry:**

```csharp
services.AddHttpClient<OrdersClient>()
    .AddTransientHttpErrorPolicy(policy =>
        policy.WaitAndRetryAsync(
            retryCount: 3,
            sleepDurationProvider: attempt => TimeSpan.FromSeconds(Math.Pow(2, attempt))
            // attempt=1 → 2сек, attempt=2 → 4сек, attempt=3 → 8сек
        ));
```

`AddTransientHttpErrorPolicy` — добавляет политику только для временных ошибок (transient). «Transient error» = временная ошибка которая может пройти сама: 5xx, HttpRequestException, таймауты. 400/401/404 не retried — это постоянные ошибки.

`WaitAndRetryAsync` параметры:
- `retryCount: 3` — сколько раз повторить (не считая первый запрос). Итого: 1 + 3 = 4 попытки максимум
- `sleepDurationProvider` — функция: номер попытки → сколько ждать перед ней
- `Math.Pow(2, attempt)` — exponential backoff: каждый retry ждёт вдвое дольше. Смысл — дать сервису время восстановиться, не бомбардируя его каждую секунду

**Circuit Breaker:**

```csharp
services.AddHttpClient<OrdersClient>()
    .AddTransientHttpErrorPolicy(policy =>
        policy.WaitAndRetryAsync(3, _ => TimeSpan.FromSeconds(2)))
    .AddTransientHttpErrorPolicy(policy =>
        policy.CircuitBreakerAsync(
            handledEventsAllowedBeforeBreaking: 5,
            durationOfBreak: TimeSpan.FromSeconds(30)
        ));
```

`CircuitBreakerAsync` параметры:
- `handledEventsAllowedBeforeBreaking: 5` — порог: после 5 ошибок подряд разомкнуть цепь. Только подряд — если иногда 200, иногда 500, CB не срабатывает
- `durationOfBreak: TimeSpan.FromSeconds(30)` — держать разомкнутой 30 сек. За это время сервис должен восстановиться

Три состояния:
```
Closed (работает нормально)
    ↓ 5 ошибок подряд
Open (отклоняет все запросы, BrokenCircuitException — НЕ идёт на сервер)
    ↓ через 30 сек
Half-Open (пропускает один пробный запрос)
    ↓ успех → Closed | ошибка → Open снова
```

**Timeout:**

```csharp
services.AddHttpClient<OrdersClient>(client =>
{
    client.Timeout = TimeSpan.FromSeconds(30); // глобальный таймаут клиента
})
.AddPolicyHandler(Policy.TimeoutAsync<HttpResponseMessage>(10)); // Polly timeout per-request
```

- `client.Timeout` — общий таймаут включая все retry
- `Policy.TimeoutAsync<HttpResponseMessage>(10)` — таймаут на каждый отдельный запрос (включая retry-попытки)

`AddPolicyHandler` vs `AddTransientHttpErrorPolicy`:
- `AddTransientHttpErrorPolicy` — shortcut, автоматически фильтрует transient ошибки
- `AddPolicyHandler` — полный контроль, явно указываешь какие исключения и статусы обрабатывать

**Порядок регистрации политик (важно):**

```csharp
services.AddHttpClient<OrdersClient>()
    .AddTransientHttpErrorPolicy(p => p.CircuitBreakerAsync(5, TimeSpan.FromSeconds(30)))
    .AddTransientHttpErrorPolicy(p => p.WaitAndRetryAsync(3, _ => TimeSpan.FromSeconds(2)))
    .AddPolicyHandler(Policy.TimeoutAsync<HttpResponseMessage>(10));
// Выполнение: Timeout(внутри) → Retry → CircuitBreaker(снаружи)
```

Последняя зарегистрированная = внешняя (выполняется первой). Цепочка снаружи → внутрь: CB → Retry → Timeout → HTTP запрос.

★ Insight:
- Circuit Breaker — это State Machine паттерн (Closed/Open/Half-Open)
- Retry без CB опасен: retry storm — при падении сервиса каждый клиент делает N retry → нагрузка умножается
- CB снаружи считает итоги retry-серий. CB внутри считает каждую попытку — включая те от которых retry уже оправился

#### Проверка Блока 3

**Claude:** Q1: Circuit Breaker открылся (Open state) — что происходит с запросами в этот момент? Они уходят на сервер или нет?
**Адиль:** они прерываются, он отклоняет все запросы
→ ✅ В Open state Polly не отправляет запрос на сервер вообще, сразу бросает BrokenCircuitException

**Claude:** Q2: Retry зарегистрирован первым, Circuit Breaker — вторым. В каком порядке они реально выполнятся и почему это важно?
**Адиль:** сначала CircuitBreakerAsync потом WaitAndRetryAsync. тут позволит выполнить 4 запроса, так как ретраев 3 и не дойдет до статуса open до прерывания. Почему они в таком порядке я не знаю. Почему важно — потому что разработчик должен иметь возможность настроить. Что будет если в обратном порядке?
→ ✅ (порядок верный, объяснение через семантику потребовалось)

**Claude:** Объяснил через матрёшку: последняя зарегистрированная = внешняя. CB снаружи видит итоги retry-серий — если retry справился, CB это воспринимает как успех. CB внутри видит каждую попытку включая успешно отретрайенные.

**Уточнение: зачем контролировать порог?**
**Адиль:** и зачем нам контролировать порог?
**Claude:** Реальная причина — семантика: CB должен отвечать «сервис недоступен?», а не «был ли один запрос неудачным?». CB снаружи считает только случаи когда retry не помог. CB внутри считает все попытки включая временные сбои от которых retry оправился.

**Уточнение: что значит «retry оправился»?**
**Адиль:** CB внутри считает все попытки включая те когда retry справился — почему? что значит оправился?
**Claude:** «Retry справился» = первая попытка → 500, retry → вторая попытка → 200, итог успех. CB не знает что снаружи есть Retry — он видит только то что приходит к нему. Каждый 500 для CB = ошибка, независимо от финального результата. CB снаружи видит только финальный итог цепочки.

**Микрофидбек:** да ✅

---

### Блок 4: Тестирование HTTP клиентов

**Claude:**

Аналогия: Ты тестируешь службу доставки, но не хочешь каждый раз реально отправлять курьера. Вместо этого ставишь на место курьера «актёра» — он делает вид что едет и возвращает нужный тебе результат. `MockHttpMessageHandler` — это и есть такой актёр вместо реального HTTP-соединения.

Проблема: в тесте нельзя поднять реальный сервер на каждый запуск. Нужно подменить `HttpClient` так чтобы он возвращал заготовленный ответ.

Решение — подменить `HttpMessageHandler` (из блока 1: `HttpClient` — обёртка над handler):

```csharp
// Пакет: RichardSzalay.MockHttp
public class OrdersClientTests
{
    [Fact]
    public async Task GetOrder_ReturnsOrder_WhenApiResponds200()
    {
        var mockHttp = new MockHttpMessageHandler();

        mockHttp
            .When("/orders/42")
            .Respond(
                HttpStatusCode.OK,
                "application/json",
                """{"id": 42, "name": "Test Order"}"""
            );

        var client = mockHttp.ToHttpClient();
        client.BaseAddress = new Uri("https://orders.api.com");
        var ordersClient = new OrdersClient(client);

        var order = await ordersClient.GetOrder(42);

        order.Should().NotBeNull();
        order!.Id.Should().Be(42);
    }
}
```

Что делает каждая часть:
- `MockHttpMessageHandler` — перехватчик запросов, вместо реального сокета возвращает заготовку
- `.When("/orders/42")` — правило: перехватывать запросы на этот URL
- `.Respond(...)` — что вернуть: статус, content-type, тело
- `mockHttp.ToHttpClient()` — создаёт HttpClient с подменённым handler

Тестирование с Polly через IHttpClientFactory:

```csharp
[Fact]
public async Task GetOrder_Retries_On500()
{
    var mockHttp = new MockHttpMessageHandler();
    var callCount = 0;

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

    var services = new ServiceCollection();
    services.AddHttpClient<OrdersClient>(c =>
        c.BaseAddress = new Uri("https://orders.api.com"))
        .AddTransientHttpErrorPolicy(p => p.WaitAndRetryAsync(3, _ => TimeSpan.Zero))
        .ConfigurePrimaryHttpMessageHandler(() => mockHttp);

    var provider = services.BuildServiceProvider();
    var ordersClient = provider.GetRequiredService<OrdersClient>();

    var order = await ordersClient.GetOrder(42);

    order.Should().NotBeNull();
    callCount.Should().Be(3);
}
```

`.ConfigurePrimaryHttpMessageHandler(() => mockHttp)` — говорит фабрике использовать mock вместо реального SocketsHttpHandler. Вся цепочка Polly работает с подменённым транспортом.
`TimeSpan.Zero` в retry — убирает реальные паузы между попытками в тестах.

★ Insight:
- MockHttpMessageHandler использует тот же механизм DelegatingHandler что и Polly
- TimeSpan.Zero в retry при тестировании — убирает реальные паузы
- Собес: «Как тестировать код с HttpClient?» → MockHttpMessageHandler. «Мокаем HttpClient через Moq» — неверный ответ

#### Проверка Блока 4

**Claude:** Q1: Почему нельзя просто замокать `HttpClient` через Moq напрямую?
**Адиль:** потому что это не интерфейс, плохо мокируется, придется все зависимости мокать
→ ✅ HttpClient не интерфейс, методы не виртуальные — Moq не может создать прокси и перехватить вызовы

**Claude:** Q2: Что будет если убрать `.ConfigurePrimaryHttpMessageHandler` и передать mockHttp напрямую в HttpClient?
**Адиль:** тогда не сможем протестить retry так как он должен по мокируемому запросу работать
→ ✅ Без ConfigurePrimaryHttpMessageHandler фабрика создаст реальный SocketsHttpHandler. Polly будет делать retry на реальный сервер которого нет → падение

**Микрофидбек:** да ✅

#### ↳ Углубление: Mountebank и TestContainers (тип: уточнение)

**Адиль:** а я могу ведь mountebank использовать или testContainers?

**Claude:** Да, оба рабочие:
- `MockHttpMessageHandler` — in-process, unit тесты, мгновенно, низкий реализм
- `Mountebank` — внешний HTTP-сервер, integration тесты, средний реализм (используется в проекте)
- `TestContainers` — реальный сервис в Docker, E2E, высокий реализм

В реальном проекте используют все три на разных уровнях пирамиды тестирования.

---

## Сессия 2 — 2026-03-06

### Блок 5: Практика + итоговая проверка

#### Задача 1 — найди проблемы в коде

**Claude:**
```csharp
public class PaymentService
{
    private static readonly HttpClient _client = new HttpClient();

    public async Task<PaymentResult> ProcessPayment(PaymentRequest request)
    {
        _client.BaseAddress = new Uri("https://payments.api.com");
        _client.DefaultRequestHeaders.Add("X-Api-Key", "secret-key");

        var response = await _client.PostAsJsonAsync("/payments", request);
        return await response.Content.ReadFromJsonAsync<PaymentResult>();
    }
}
```

**Адиль:** статик клиент резолвится внутри — может быть рейз кондишн, указан секрет в коде а не в юзер секретах
→ ✅ (2 из 4 найдено)

**Claude:** Ещё две проблемы — подсказка: static readonly HttpClient и DNS/handler ротация.

**Адиль:** может быть исчерпание портов, также при изменении ip в клиенте значение не поменяется и будет падать. Хотел спросить что значит ротируются особенно в рамках хэндлера
→ ✅ все 4 нашёл: 1) race condition на DefaultRequestHeaders, 2) DNS не обновляется, 3) port exhaustion при new HttpClient(), 4) секрет захардкожен

**Claude:** Ротация = IHttpClientFactory создаёт новый handler через 2 мин (expire → новые запросы идут через новый), старый доделывает текущие → Dispose() → GC. static HttpClient — handler один на весь lifetime приложения, никогда не ротируется.

#### Задача 2 — перепиши правильно

**Адиль:**
```csharp
public class PaymentService(HttpClient client)
{
    public async Task<PaymentResult> GetPayments(PaymentRequest request){
        var response = await _client.PostAsJsonAsync("/payments", request);
        return await response.Content.ReadFromJsonAsync<PaymentResult>();
    }
}

var cfg = configuration.GetSection("secret-key").Get<SecretKey>();
services.AddHttpClient<PaymentClient>(client =>
{
    client.BaseAddress = new Uri("https://payments.api.com");
    client.DefaultRequestHeaders.Add("X-Api-Key", cfg.Key);
});
```
→ ✅ структура верная. Замечания: опечатка `_client` вместо `client`, смешение PaymentService/PaymentClient

#### Итоговая проверка

**Q1:** Что такое HttpMessageHandler и почему IHttpClientFactory управляет именно им?
**Адиль:** обёртка над запросом который держит tcp соединение. у фабрики есть пул этих хэндлеров, каждый живёт ограниченное время, после expire создаётся новый handler, старый завершает запросы и очищается. Замена хэндлера позволяет держать актуальный IP при смене DNS. А handler очищается коллектором или возвращается в пул?
→ ✅ + уточнение: handler Dispose() → удаляется из пула, GC собирает объект. Не возвращается в пул — уничтожается.

**Q2:** Разница Named vs Typed client?
**Адиль:** нэймед — именованный, тайпед — по типу. Нэймед нужно создавать во всех сервисах через factory.CreateClient("name"), для тайпед достаточно инжектировать
→ ✅

**Q3:** Порядок политик Polly — почему CB снаружи, Retry внутри, Timeout innermost?
**Адиль:** потому что CB точно знает что блок запросов retry выполнился успешно или упал. Если наоборот — непонятно когда именно сработает. Больше контроля. Таймаут — на каждый отдельный HTTP запрос внутри retry или на все 5 retry например?
→ ✅ + уточнение: Policy.TimeoutAsync(10) — таймаут на каждую попытку. client.Timeout — на весь цикл включая все retry.

**Q4:** Как протестировать что retry срабатывает 3 раза?
**Адиль:** через юнит тест замокать хэндлер, внутри сделать счётчик
→ ✅

**Q5 (trade-off):** Retry для платёжного шлюза — стоит ли? Если да — с какими ограничениями?
**Адиль:** ограничить ошибки — например потеря соединения, но не таймаут, так как внутри сервиса могла быть выполнена часть операции
→ ✅ Senior-мышление. Дополнение: Idempotency-Key позволяет retry даже при таймауте если шлюз поддерживает.

**Итоговая оценка: Middle** — тема усвоена уверенно.

---

## Сессия 3 — 2026-03-09
> Тип: практика

### Практика — Задача 1: Выбери тип клиента

**Claude:** У тебя есть `NotificationService`, который отправляет push-уведомления через внешний API (`https://push.api.com`). Сервис используется в 3 контроллерах. Какой тип HTTP-клиента выбрать и почему? Напиши регистрацию в DI.

**Адиль:** typed,
services.AddHttpCleint<PushHttpClient>client =>
{
    client.BaseAddress = new Uri("https://push.api.com");
    client.Timeout = TimeSpan.FromSeconds(30);
});

**Claude:** Правильный выбор — Typed client ✅. По коду — логика верная, но есть нюансы:
- Опечатка: `AddHttpCleint` → `AddHttpClient`
- `client.Timeout` — это таймаут **всей операции включая все retry**. Если 30 сек + 3 retry по 10 сек → на третьей попытке уже `TaskCanceledException`
- Для per-attempt таймаута нужен Polly: `.AddPolicyHandler(Policy.TimeoutAsync<HttpResponseMessage>(10))`
- `client.Timeout` лучше использовать как аварийный потолок (60 сек), а не per-attempt

*Сессия прервана на задаче 1/5.*
