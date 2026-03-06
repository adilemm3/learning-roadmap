# HTTP Clients & IHttpClientFactory — Конспект

## Блок 1: HttpClient под капотом

**Ключевая проблема:** `new HttpClient()` на каждый запрос → socket exhaustion
- После `Dispose()` сокет остаётся в `TIME_WAIT` ~4 минуты
- При высокой нагрузке 65 000 портов заканчиваются → `SocketException`

**`IHttpClientFactory` — решение:**
- Держит пул `HttpMessageHandler`-ов (не соединений)
- `HttpClient` создаётся новый каждый раз (лёгкий, без состояния)
- Handlers ротируются каждые **2 минуты** → DNS-изменения подхватываются
- Ротация graceful: expire → новые запросы на новый handler, старые доделываются

**static HttpClient — антипаттерн:**
- `DefaultRequestHeaders` не потокобезопасны → race condition
- DNS не обновляется
- Настраивать клиент нужно при регистрации в DI, не при использовании

## Блок 2: IHttpClientFactory — типы клиентов

**Три типа клиентов:**

| Тип | Регистрация | Когда использовать |
|-----|------------|-------------------|
| Basic | `AddHttpClient()` | Редко, разовые запросы |
| Named | `AddHttpClient("name", ...)` | Один клиент нужен в нескольких местах |
| Typed | `AddHttpClient<TClient>(...)` | ✅ Рекомендуется всегда |

**Typed client:**
- `AddHttpClient<T>` регистрирует T как transient + создаёт фабрику с настроенным HttpClient
- Нельзя переопределять через `AddSingleton<T>` — перезапишет transient, handler не будет ротироваться
- `AddTransient<T>` без `AddHttpClient` — HttpClient инжектится без настроек фабрики

**DI под капотом:**
- `IServiceCollection` = `List<ServiceDescriptor>`
- При дублирующей регистрации побеждает последний дескриптор

## Блок 3: Polly & Resilience

**Три политики и их назначение:**

| Политика | Назначение | Когда срабатывает |
|----------|-----------|-------------------|
| Retry | Повторить при временной ошибке | 5xx, HttpRequestException, таймаут |
| Circuit Breaker | Отключиться когда сервис системно недоступен | После N подряд провалов |
| Timeout | Не ждать вечно | Каждый отдельный запрос |

**Правильный порядок (снаружи → внутрь):**
```
CircuitBreaker → Retry → Timeout → HTTP запрос
```
CB снаружи видит итоги retry-серий. Если retry справился — CB не считает ошибкой.

**Ключевые параметры:**
- `retryCount` — количество повторов (не считая первый запрос)
- `sleepDurationProvider` — пауза между попытками (exponential backoff: `Math.Pow(2, attempt)`)
- `handledEventsAllowedBeforeBreaking` — порог ошибок подряд для открытия CB
- `durationOfBreak` — время в Open state до Half-Open пробы

**Состояния CB:** Closed → Open (после N ошибок) → Half-Open (через durationOfBreak) → Closed/Open

## Блок 4: Тестирование HTTP клиентов

**Инструменты по уровню тестирования:**

| Инструмент | Уровень | Скорость | Реализм |
|-----------|---------|----------|---------|
| MockHttpMessageHandler | Unit | ⚡ | Низкий |
| Mountebank | Integration | 🐢 | Средний |
| TestContainers | E2E | 🐢🐢 | Высокий |

**Почему не Moq для HttpClient:** не интерфейс, методы не виртуальные → нельзя создать прокси.

**MockHttpMessageHandler:** подменяет HttpMessageHandler в цепочке → HttpClient ходит в mock.

**С IHttpClientFactory + Polly:**
```csharp
.ConfigurePrimaryHttpMessageHandler(() => mockHttp) // подменяет handler в фабрике
// TimeSpan.Zero в retry — убирает паузы в тестах
```

## Блок 5: Практика + итоговая проверка

**Типичные ошибки в коде:**
- `static HttpClient` → race condition на DefaultRequestHeaders + DNS не обновляется
- `new HttpClient()` per request → port exhaustion
- Секреты в коде → вынести в конфигурацию

**Правильная структура:**
- Typed client — только HTTP-коммуникация
- Service — бизнес-логика, использует typed client
- Регистрация через `AddHttpClient<T>` с конфигурацией из `configuration["key"]`

**Retry для критических операций:**
- Retry только на сетевые ошибки, не на таймаут (операция могла частично выполниться)
- `Idempotency-Key` → retry безопасен даже при таймауте если сервис поддерживает

**Итоговая оценка: Middle**
