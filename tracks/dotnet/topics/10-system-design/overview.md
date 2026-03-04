# System Design — Обзор

## Что это
Проектирование распределённых систем — масштабирование, messaging, кэширование, API. Итоговый раздел для Architect уровня, объединяющий знания из всех предыдущих разделов.

## Подтемы
| # | Подтема | Описание |
|---|---------|----------|
| 1 | Fundamentals | CAP теорема, consistency, availability, latency, throughput |
| 2 | Messaging & Queues | RabbitMQ, Kafka, паттерны messaging |
| 3 | Caching Strategies | Стратегии кэширования, Redis, cache invalidation |
| 4 | API Design | REST, GraphQL, версионирование, pagination, HATEOAS |
| 5 | Load Balancing & Scaling | Балансировка, горизонтальное/вертикальное масштабирование |
| 6 | Database Sharding & Replication | Шардирование, репликация, partitioning |
| 7 | Real-World Systems | Разбор реальных архитектур (URL shortener, chat, feed) |

## Порядок изучения
Clean Architecture → Fundamentals → Messaging & Queues
NoSQL + Fundamentals → Caching Strategies
Routing & Controllers + Fundamentals → API Design
Fundamentals + Kubernetes → Load Balancing & Scaling
SQL Optimization + Fundamentals → Database Sharding & Replication
Все подтемы → Real-World Systems

## Связи с другими разделами
Зависит от Architecture, Data Access, DevOps. Итоговый раздел для Architect уровня.
