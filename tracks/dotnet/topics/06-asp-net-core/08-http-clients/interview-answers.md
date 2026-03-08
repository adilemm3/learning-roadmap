# HTTP Clients & IHttpClientFactory — Ответы на вопросы

## Junior

**1. Зачем нужен HttpClient?**
<details><summary>Ответ</summary>

Для отправки HTTP-запросов к внешним сервисам. Обёртка над TCP-соединением.

</details>

**2. Что такое IHttpClientFactory?**
<details><summary>Ответ</summary>

Фабрика которая управляет пулом HttpMessageHandler-ов. Решает проблему socket exhaustion и DNS-устаревания.

</details>

**3. Почему нельзя делать `new HttpClient()` на каждый запрос?**
<details><summary>Ответ</summary>

После Dispose() сокет остаётся в TIME_WAIT ~4 минуты. При высокой нагрузке заканчиваются порты (65К) → SocketException. Решение: IHttpClientFactory с пулом handler-ов.

</details>

## Middle

**4. Какие типы HTTP-клиентов есть в .NET и когда что выбрать?**
<details><summary>Ответ</summary>

Basic (ручное создание, редко), Named (по строковому ключу, несколько мест), Typed (отдельный класс, DI инжектит — рекомендуется всегда). Typed даёт типобезопасность и Single Responsibility.

</details>

**5. Почему нельзя регистрировать Typed client как Singleton?**
<details><summary>Ответ</summary>

AddSingleton перезаписывает transient регистрацию от AddHttpClient. HttpMessageHandler внутри не ротируется → DNS-проблема.

</details>

**6. Что такое AddTransientHttpErrorPolicy?**
<details><summary>Ответ</summary>

Shortcut для политик которые срабатывают только на временные ошибки (5xx, HttpRequestException, таймаут). 400/401/404 — постоянные ошибки, retry не поможет.

</details>

**7. Как правильно комбинировать Polly политики?**
<details><summary>Ответ</summary>

CB снаружи → Retry → Timeout innermost. CB видит итоги retry-серий — если retry справился, CB не считает ошибкой. CB внутри считал бы каждую отдельную попытку включая успешно отретрайенные.

</details>

**8. Как тестировать код с HttpClient?**
<details><summary>Ответ</summary>

MockHttpMessageHandler (RichardSzalay.MockHttp) — подменяет handler в цепочке. Нельзя мокать HttpClient через Moq — не интерфейс, методы не виртуальные.

</details>

## Senior

**9. Что такое retry storm и как его предотвратить?**
<details><summary>Ответ</summary>

При падении сервиса каждый клиент делает N retry → нагрузка умножается на N×кол-во клиентов. Предотвращение: Circuit Breaker (отключается когда сервис недоступен) + exponential backoff (уменьшает частоту запросов).

</details>

**10. Как тестировать Polly retry с IHttpClientFactory?**
<details><summary>Ответ</summary>

`.ConfigurePrimaryHttpMessageHandler(() => mockHttp)` — подменяет handler в фабрике. Полная цепочка Polly работает с mock-транспортом. `TimeSpan.Zero` в retry убирает паузы в тестах.

</details>

**11. Когда НЕ стоит делать retry?**
<details><summary>Ответ</summary>

Для неидемпотентных операций (платежи, списания) при таймауте — операция могла частично выполниться. Решение: Idempotency-Key если сервис поддерживает, или retry только на сетевые ошибки (connection refused, DNS).

</details>

**12. Чем client.Timeout отличается от Policy.TimeoutAsync?**
<details><summary>Ответ</summary>

`client.Timeout` — общий таймаут на весь запрос включая все retry. `Policy.TimeoutAsync(N)` — таймаут на каждую отдельную попытку внутри retry-цикла.

</details>

## Architect

**13. Как спроектировать resilience-стратегию для платёжного шлюза с учётом идемпотентности?**
<details><summary>Ответ</summary>

Retry только на сетевые ошибки (connection refused, DNS). Таймаут — не retry, потому что операция могла выполниться. Добавить Idempotency-Key заголовок — шлюз дедуплицирует повторные запросы. Circuit Breaker снаружи: при системном падении шлюза — fast fail вместо retry storm. Fallback: поставить платёж в очередь для повторной обработки.

</details>

**14. В микросервисной архитектуре 20 сервисов используют HTTP-клиенты. Как стандартизировать resilience-политики не дублируя конфигурацию?**
<details><summary>Ответ</summary>

Централизованный extension method (`AddResilientHttpClient<T>`) с дефолтными политиками (CB + Retry + Timeout). Параметры через `IConfiguration` — каждый сервис переопределяет только то что нужно. Общий NuGet-пакет с инфраструктурой. Мониторинг: Polly events → метрики (Prometheus) → алерты на CB Open state.

</details>

**15. HttpClient в Kubernetes: какие проблемы с DNS и service mesh, как решить?**
<details><summary>Ответ</summary>

В K8s IP подов меняются при каждом деплое (rolling update). Static HttpClient кэширует старый IP → connection refused. Решение: IHttpClientFactory с ротацией handler (2 мин). С service mesh (Istio): sidecar proxy перехватывает трафик — можно делегировать retry/CB на уровень mesh, убрав Polly. Trade-off: Polly даёт контроль на уровне кода (разные политики для разных эндпоинтов), mesh — единообразие без изменения кода.

</details>
