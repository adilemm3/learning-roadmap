# ASP.NET Core — Обзор

## Что это
Веб-фреймворк — middleware, DI, маршрутизация, аутентификация, real-time коммуникация. Основной инструмент для построения веб-приложений и API на .NET.

## Подтемы
| # | Подтема | Описание |
|---|---------|----------|
| 1 | Middleware Pipeline | Конвейер middleware, RequestDelegate, Use/Map/Run |
| 2 | Dependency Injection | Встроенный DI-контейнер, время жизни, Scrutor |
| 3 | Routing & Controllers | Маршрутизация, контроллеры, модель MVC |
| 4 | Authentication & Authorization | Identity, JWT, Policy-based authorization |
| 5 | Filters & Model Binding | Фильтры, model binding, валидация |
| 6 | Minimal API | Minimal API, endpoint routing, AOT support |
| 7 | SignalR & gRPC | Real-time с SignalR, gRPC для inter-service |

## Порядок изучения
Middleware Pipeline → Routing & Controllers → Authentication & Authorization
Middleware Pipeline → Filters & Model Binding
Routing & Controllers + Dependency Injection → Minimal API
Task & async/await + Middleware Pipeline → SignalR & gRPC

## Связи с другими разделами
Зависит от Async, Delegates, Interfaces. Является основой для Data Access, Security, DevOps.
