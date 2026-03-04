# Architecture — Обзор

## Что это
Архитектурные подходы — от SOLID до микросервисов и модульного монолита. Раздел для Senior и Architect уровней, охватывающий принципы построения масштабируемых и поддерживаемых систем.

## Подтемы
| # | Подтема | Описание |
|---|---------|----------|
| 1 | SOLID | Принципы SOLID с примерами на C# |
| 2 | Clean Architecture | Слои, зависимости, Use Cases, порты и адаптеры |
| 3 | DDD | Domain-Driven Design, агрегаты, value objects, bounded contexts |
| 4 | CQRS & Event Sourcing | Разделение команд и запросов, event store |
| 5 | Microservices | Декомпозиция, коммуникация, saga, outbox |
| 6 | Modular Monolith | Модули, границы, миграция в микросервисы |
| 7 | Hexagonal / Ports & Adapters | Гексагональная архитектура, порты, адаптеры |

## Порядок изучения
Interfaces + Design Patterns → SOLID → Clean Architecture → DDD
DDD + Messaging → CQRS & Event Sourcing
DDD + Messaging + Docker → Microservices
Clean Architecture + DDD → Modular Monolith
Clean Architecture + SOLID → Hexagonal / Ports & Adapters

## Связи с другими разделами
Зависит от OOP, Design Patterns, DI. Связан с System Design, Testing (testability).
