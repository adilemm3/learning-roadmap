# HTTP Clients & IHttpClientFactory — Ресурсы

## Официальная документация

- [IHttpClientFactory в ASP.NET Core](https://learn.microsoft.com/en-us/aspnet/core/fundamentals/http-requests) — Microsoft Docs, основной источник
- [Polly документация](https://www.thepollyproject.org/) — официальный сайт библиотеки
- [HttpClient Guidelines](https://learn.microsoft.com/en-us/dotnet/fundamentals/networking/http/httpclient-guidelines) — Microsoft, когда что использовать

## Статьи

- [You're using HttpClient wrong](https://josefottosson.se/you-are-probably-still-using-httpclient-wrong-and-it-is-destabilizing-your-software/) — Josef Ottosson, классика про socket exhaustion
- [Polly and HttpClientFactory](https://learn.microsoft.com/en-us/dotnet/architecture/microservices/implement-resilient-applications/implement-http-call-retries-exponential-backoff-polly) — Microsoft, resilience паттерны

## NuGet пакеты

- `Microsoft.Extensions.Http` — IHttpClientFactory (встроен в ASP.NET Core)
- `Microsoft.Extensions.Http.Polly` — интеграция Polly с IHttpClientFactory
- `RichardSzalay.MockHttp` — MockHttpMessageHandler для тестов
- `Polly` — retry, circuit breaker, timeout политики
