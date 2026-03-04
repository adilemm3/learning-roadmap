# Data Access — Обзор

## Что это
Доступ к данным — EF Core, Dapper, SQL оптимизация, миграции, NoSQL. Охватывает все аспекты работы с базами данных в .NET-приложениях, от простого CRUD до продвинутой оптимизации запросов.

## Подтемы
| # | Подтема | Описание |
|---|---------|----------|
| 1 | EF Core Basics | DbContext, модели, CRUD, отложенная загрузка |
| 2 | EF Core Advanced | Query splitting, compiled queries, interceptors, change tracker |
| 3 | Dapper | Micro-ORM, маппинг, производительность vs EF Core |
| 4 | SQL Optimization | Индексы, планы выполнения, N+1, batching |
| 5 | Migrations Strategies | Стратегии миграций, FluentMigrator, blue-green |
| 6 | NoSQL: Redis & MongoDB | Redis (кэш, pub/sub), MongoDB (документы) |

## Порядок изучения
LINQ + Dependency Injection → EF Core Basics → EF Core Advanced
Task & async/await → Dapper
EF Core Basics + Big O → SQL Optimization
EF Core Advanced → Migrations Strategies
Task & async/await + SQL Optimization → NoSQL: Redis & MongoDB

## Связи с другими разделами
Зависит от LINQ, Async, DI. Связан с Architecture (Repository pattern), System Design (caching, sharding).
