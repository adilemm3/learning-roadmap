# ASP.NET Core — Обзор

## Что это
Веб-фреймворк — middleware, DI, маршрутизация, аутентификация, real-time коммуникация. Основной инструмент для построения веб-приложений и API на .NET.

## Подтемы

| # | Подтема | Описание | Статус | Последняя сессия |
|---|---------|----------|--------|-----------------|
| 1 | Middleware Pipeline | Конвейер middleware, RequestDelegate, Use/Map/Run | ⬜ | — |
| 2 | Dependency Injection | Встроенный DI-контейнер, время жизни, Scrutor | ⬜ | — |
| 3 | Routing & Controllers | Маршрутизация, контроллеры, модель MVC | ⬜ | — |
| 4 | Authentication & Authorization | Identity, JWT, Policy-based authorization | ⬜ | — |
| 5 | Filters & Model Binding | Фильтры, model binding, валидация | ⬜ | — |
| 6 | Minimal API | Minimal API, endpoint routing, AOT support | ⬜ | — |
| 7 | SignalR & gRPC | Real-time с SignalR, gRPC для inter-service | ⬜ | — |
| 8 | HTTP Clients & IHttpClientFactory | IHttpClientFactory, typed/named clients, Polly, тестирование | ✅ | 2026-03-06 |

## Порядок изучения и зависимости

| Подтема | Зависит от (изучи сначала) |
|---------|---------------------------|
| Middleware Pipeline | — (первая тема раздела) |
| Dependency Injection | — (первая тема раздела) |
| Routing & Controllers | Middleware Pipeline |
| Authentication & Authorization | Routing & Controllers, Dependency Injection |
| Filters & Model Binding | Middleware Pipeline, Routing & Controllers |
| Minimal API | Routing & Controllers, Dependency Injection |
| SignalR & gRPC | Task & async/await (04), Middleware Pipeline |
| HTTP Clients & IHttpClientFactory | Dependency Injection, Task & async/await (04) |

Рекомендуемый порядок:
1. Middleware Pipeline + Dependency Injection (параллельно, независимы)
2. Routing & Controllers
3. Authentication & Authorization + Filters & Model Binding
4. Minimal API
5. HTTP Clients & IHttpClientFactory
6. SignalR & gRPC

## Связи с другими разделами
Зависит от Async, Delegates, Interfaces. Является основой для Data Access, Security, DevOps.
