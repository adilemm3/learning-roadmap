# Design Patterns — Обзор

## Что это
Паттерны проектирования GoF и их применение в .NET экосистеме. Понимание паттернов позволяет писать гибкий, расширяемый код и говорить на одном языке с другими разработчиками.

## Подтемы
| # | Подтема | Описание |
|---|---------|----------|
| 1 | Creational | Factory, Abstract Factory, Builder, Singleton, Prototype |
| 2 | Structural | Adapter, Decorator, Proxy, Facade, Composite |
| 3 | Behavioral | Strategy, Observer, Command, Template Method, Chain of Responsibility |
| 4 | Patterns in .NET | Паттерны в .NET: Options, IHostedService, Middleware, DI |
| 5 | Concurrency Patterns | Producer-Consumer, Bulkhead, throttling паттерны |

## Порядок изучения
Interfaces + Dependency Injection → Creational
Interfaces + Generics → Structural
Delegates + Interfaces → Behavioral
Creational + Structural + Behavioral → Patterns in .NET
Behavioral + Task & async/await → Concurrency Patterns

## Связи с другими разделами
Зависит от OOP. Используется в Architecture, ASP.NET Core. Patterns in .NET связывает теорию с практикой.
