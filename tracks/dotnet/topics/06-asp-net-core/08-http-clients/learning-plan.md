# HTTP Clients & IHttpClientFactory — План изучения
> Статус: ✅ завершена
> Блок: 5/5 | Последняя сессия: 2026-03-06

## Калибровка
- Базовые концепции: ✅ знает назначение HttpClient
- Средний уровень: ✅ знает socket exhaustion
- Продвинутый: ✅ знает IHttpClientFactory в общих чертах, детали handler pool не раскрыты
→ Начинаем с блока: 1 (Middle-, углубляем механизм)

## Блоки

- [x] **Блок 1: HttpClient под капотом**
  Socket exhaustion, HttpMessageHandler lifecycle, TIME_WAIT, ротация handler-ов, DNS.
  Проверка: 2 вопроса

- [x] **Блок 2: IHttpClientFactory — типы клиентов**
  Basic / Named / Typed clients, DI-интеграция, настройка при регистрации.
  Связь: Dependency Injection (02-asp-net-core).
  Проверка: 2 вопроса

- [x] **Блок 3: Polly & Resilience**
  Retry, Circuit Breaker, Timeout, AddPolicyHandler, резильентность в продакшне.
  Проверка: 2 вопроса

- [x] **Блок 4: Тестирование HTTP клиентов**
  MockHttpMessageHandler, фейковые ответы, тестирование typed clients.
  Связь: Unit Testing (11-testing).
  Проверка: 2 вопроса

- [x] **Блок 5: Практика + итоговая проверка**
  Задачи на все блоки, 5 вопросов возрастающей сложности.
