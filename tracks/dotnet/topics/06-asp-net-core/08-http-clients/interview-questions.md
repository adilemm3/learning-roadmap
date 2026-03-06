# HTTP Clients & IHttpClientFactory — Вопросы для собеседования

## Junior

**Q: Зачем нужен HttpClient?**
A: Для отправки HTTP-запросов к внешним сервисам. Обёртка над TCP-соединением.

**Q: Что такое IHttpClientFactory?**
A: Фабрика которая управляет пулом HttpMessageHandler-ов. Решает проблему socket exhaustion и DNS-устаревания.

**Q: Почему нельзя делать `new HttpClient()` на каждый запрос?**
A: После Dispose() сокет остаётся в TIME_WAIT ~4 минуты. При высокой нагрузке заканчиваются порты (65К) → SocketException. Решение: IHttpClientFactory с пулом handler-ов.

## Middle

**Q: Какие типы HTTP-клиентов есть в .NET и когда что выбрать?**
A: Basic (ручное создание, редко), Named (по строковому ключу, несколько мест), Typed (отдельный класс, DI инжектит — рекомендуется всегда). Typed даёт типобезопасность и Single Responsibility.

**Q: Почему нельзя регистрировать Typed client как Singleton?**
A: AddSingleton перезаписывает transient регистрацию от AddHttpClient. HttpMessageHandler внутри не ротируется → DNS-проблема.

**Q: Что такое AddTransientHttpErrorPolicy?**
A: Shortcut для политик которые срабатывают только на временные ошибки (5xx, HttpRequestException, таймаут). 400/401/404 — постоянные ошибки, retry не поможет.

**Q: Как правильно комбинировать Polly политики?**
A: CB снаружи → Retry → Timeout innermost. CB видит итоги retry-серий — если retry справился, CB не считает ошибкой. CB внутри считал бы каждую отдельную попытку включая успешно отретрайенные.

**Q: Как тестировать код с HttpClient?**
A: MockHttpMessageHandler (RichardSzalay.MockHttp) — подменяет handler в цепочке. Нельзя мокать HttpClient через Moq — не интерфейс, методы не виртуальные.

## Senior

**Q: Что такое retry storm и как его предотвратить?**
A: При падении сервиса каждый клиент делает N retry → нагрузка умножается на N×кол-во клиентов. Предотвращение: Circuit Breaker (отключается когда сервис недоступен) + exponential backoff (уменьшает частоту запросов).

**Q: Как тестировать Polly retry с IHttpClientFactory?**
A: `.ConfigurePrimaryHttpMessageHandler(() => mockHttp)` — подменяет handler в фабрике. Полная цепочка Polly работает с mock-транспортом. `TimeSpan.Zero` в retry убирает паузы в тестах.

**Q: Когда НЕ стоит делать retry?**
A: Для неидемпотентных операций (платежи, списания) при таймауте — операция могла частично выполниться. Решение: Idempotency-Key если сервис поддерживает, или retry только на сетевые ошибки (connection refused, DNS).

**Q: Чем client.Timeout отличается от Policy.TimeoutAsync?**
A: `client.Timeout` — общий таймаут на весь запрос включая все retry. `Policy.TimeoutAsync(N)` — таймаут на каждую отдельную попытку внутри retry-цикла.

## Architect

**Q: Как спроектировать resilience-стратегию для платёжного шлюза с учётом идемпотентности?**
A: Retry только на сетевые ошибки (connection refused, DNS). Таймаут — не retry, потому что операция могла выполниться. Добавить Idempotency-Key заголовок — шлюз дедуплицирует повторные запросы. Circuit Breaker снаружи: при системном падении шлюза — fast fail вместо retry storm. Fallback: поставить платёж в очередь для повторной обработки.

**Q: В микросервисной архитектуре 20 сервисов используют HTTP-клиенты. Как стандартизировать resilience-политики не дублируя конфигурацию?**
A: Централизованный extension method (`AddResilientHttpClient<T>`) с дефолтными политиками (CB + Retry + Timeout). Параметры через `IConfiguration` — каждый сервис переопределяет только то что нужно. Общий NuGet-пакет с инфраструктурой. Мониторинг: Polly events → метрики (Prometheus) → алерты на CB Open state.

**Q: HttpClient в Kubernetes: какие проблемы с DNS и service mesh, как решить?**
A: В K8s IP подов меняются при каждом деплое (rolling update). Static HttpClient кэширует старый IP → connection refused. Решение: IHttpClientFactory с ротацией handler (2 мин). С service mesh (Istio): sidecar proxy перехватывает трафик — можно делегировать retry/CB на уровень mesh, убрав Polly. Trade-off: Polly даёт контроль на уровне кода (разные политики для разных эндпоинтов), mesh — единообразие без изменения кода.
