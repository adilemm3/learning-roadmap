# HTTP Clients & IHttpClientFactory — Вопросы для собеседования

> Ответы → `interview-answers.md`

## Junior

1. Зачем нужен HttpClient?
2. Что такое IHttpClientFactory?
3. Почему нельзя делать `new HttpClient()` на каждый запрос?

## Middle

4. Какие типы HTTP-клиентов есть в .NET и когда что выбрать?
5. Почему нельзя регистрировать Typed client как Singleton?
6. Что такое AddTransientHttpErrorPolicy?
7. Как правильно комбинировать Polly политики?
8. Как тестировать код с HttpClient?

## Senior

9. Что такое retry storm и как его предотвратить?
10. Как тестировать Polly retry с IHttpClientFactory?
11. Когда НЕ стоит делать retry?
12. Чем client.Timeout отличается от Policy.TimeoutAsync?

## Architect

13. Как спроектировать resilience-стратегию для платёжного шлюза с учётом идемпотентности?
14. В микросервисной архитектуре 20 сервисов используют HTTP-клиенты. Как стандартизировать resilience-политики не дублируя конфигурацию?
15. HttpClient в Kubernetes: какие проблемы с DNS и service mesh, как решить?
