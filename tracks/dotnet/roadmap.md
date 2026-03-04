# .NET/C# Roadmap: Junior → Architect

## 🟢 Junior Level (Фундамент)

### 1. C# Fundamentals
- [ ] 01-type-system — _нет зависимостей_
- [ ] 02-value-vs-reference — зависит от: type-system
- [ ] 03-memory-stack-heap — зависит от: value-vs-reference
- [ ] 04-garbage-collector — зависит от: memory-stack-heap
- [ ] 05-strings-immutability — зависит от: value-vs-reference
- [ ] 06-exceptions — зависит от: type-system
- [ ] 07-nullable — зависит от: value-vs-reference

### 2. OOP & Language (базовые)
- [ ] 01-inheritance-polymorphism — зависит от: type-system
- [ ] 02-interfaces-abstract — зависит от: inheritance-polymorphism
- [ ] 03-generics — зависит от: type-system, interfaces-abstract
- [ ] 04-delegates-events — зависит от: type-system
- [ ] 05-linq — зависит от: delegates-events, generics

### 3. Collections (базовые)
- [ ] 01-arrays-lists — зависит от: generics
- [ ] 02-dictionary-hashset — зависит от: arrays-lists, value-vs-reference

### 4. Algorithms (базовые)
- [ ] 01-complexity-big-o — _нет зависимостей_
- [ ] 02-sorting-searching — зависит от: complexity-big-o, arrays-lists

---

## 🟡 Middle Level (Углубление)

### 5. OOP & Language (продвинутые)
- [ ] 06-expression-trees — зависит от: linq, delegates-events
- [ ] 07-reflection — зависит от: type-system, generics

### 6. Collections (продвинутые)
- [ ] 03-concurrent-collections — зависит от: dictionary-hashset, threads-threadpool
- [ ] 04-span-memory — зависит от: memory-stack-heap, arrays-lists
- [ ] 05-custom-collections — зависит от: generics, interfaces-abstract

### 7. Async & Multithreading
- [ ] 01-threads-threadpool — зависит от: memory-stack-heap, delegates-events
- [ ] 02-task-async-await — зависит от: threads-threadpool, exceptions
- [ ] 03-synchronization-primitives — зависит от: threads-threadpool
- [ ] 04-parallel-plinq — зависит от: task-async-await, linq
- [ ] 05-channels — зависит от: task-async-await
- [ ] 06-cancellation-patterns — зависит от: task-async-await

### 8. ASP.NET Core
- [ ] 01-middleware-pipeline — зависит от: delegates-events, task-async-await
- [ ] 02-dependency-injection — зависит от: interfaces-abstract, generics
- [ ] 03-routing-controllers — зависит от: middleware-pipeline
- [ ] 04-authentication-authorization — зависит от: middleware-pipeline, routing-controllers
- [ ] 05-filters-model-binding — зависит от: routing-controllers
- [ ] 06-minimal-api — зависит от: routing-controllers, dependency-injection
- [ ] 07-signalr-grpc — зависит от: task-async-await, middleware-pipeline

### 9. Data Access (базовые)
- [ ] 01-ef-core-basics — зависит от: linq, dependency-injection
- [ ] 02-ef-core-advanced — зависит от: ef-core-basics, expression-trees
- [ ] 03-dapper — зависит от: task-async-await
- [ ] 04-sql-optimization — зависит от: ef-core-basics, complexity-big-o

### 10. Design Patterns
- [ ] 01-creational — зависит от: interfaces-abstract, dependency-injection
- [ ] 02-structural — зависит от: interfaces-abstract, generics
- [ ] 03-behavioral — зависит от: delegates-events, interfaces-abstract
- [ ] 04-patterns-in-dotnet — зависит от: creational, structural, behavioral

### 11. Testing (базовые)
- [ ] 01-unit-testing — зависит от: dependency-injection, interfaces-abstract
- [ ] 02-integration-testing — зависит от: unit-testing, ef-core-basics
- [ ] 03-mocking-strategies — зависит от: unit-testing, interfaces-abstract

### 12. Algorithms (продвинутые)
- [ ] 03-trees-graphs — зависит от: complexity-big-o, generics
- [ ] 04-dynamic-programming — зависит от: complexity-big-o
- [ ] 05-common-interview-problems — зависит от: trees-graphs, dynamic-programming

---

## 🔴 Senior Level (Экспертиза)

### 13. .NET Internals
- [ ] 01-clr-jit — зависит от: memory-stack-heap, type-system
- [ ] 02-assembly-loading — зависит от: clr-jit, reflection
- [ ] 03-gc-internals — зависит от: garbage-collector, clr-jit
- [ ] 04-threading-model — зависит от: threads-threadpool, clr-jit
- [ ] 05-performance-diagnostics — зависит от: gc-internals, threading-model

### 14. Data Access (продвинутые)
- [ ] 05-migrations-strategies — зависит от: ef-core-advanced
- [ ] 06-nosql-redis-mongo — зависит от: task-async-await, sql-optimization

### 15. Architecture (базовые)
- [ ] 01-solid — зависит от: interfaces-abstract, design-patterns
- [ ] 02-clean-architecture — зависит от: solid, dependency-injection
- [ ] 03-ddd — зависит от: clean-architecture
- [ ] 04-cqrs-event-sourcing — зависит от: ddd, messaging-queues

### 16. System Design (базовые)
- [ ] 01-fundamentals — зависит от: clean-architecture
- [ ] 02-messaging-queues — зависит от: task-async-await, fundamentals
- [ ] 03-caching-strategies — зависит от: nosql-redis-mongo, fundamentals
- [ ] 04-api-design — зависит от: routing-controllers, fundamentals

### 17. Testing (продвинутые)
- [ ] 04-tdd-bdd — зависит от: unit-testing, mocking-strategies
- [ ] 05-load-testing — зависит от: integration-testing, performance-diagnostics

### 18. DevOps (базовые)
- [ ] 01-docker-containers — зависит от: middleware-pipeline
- [ ] 02-ci-cd — зависит от: docker-containers, unit-testing
- [ ] 03-kubernetes-basics — зависит от: docker-containers

### 19. Security
- [ ] 01-owasp-top10 — зависит от: routing-controllers, authentication-authorization
- [ ] 02-cryptography-basics — зависит от: type-system
- [ ] 03-auth-patterns — зависит от: authentication-authorization, owasp-top10
- [ ] 04-secure-coding — зависит от: owasp-top10

---

## 🏛 Architect Level (Стратегия)

### 20. Architecture (продвинутые)
- [ ] 05-microservices — зависит от: ddd, messaging-queues, docker-containers
- [ ] 06-modular-monolith — зависит от: clean-architecture, ddd
- [ ] 07-hexagonal-ports-adapters — зависит от: clean-architecture, solid

### 21. System Design (продвинутые)
- [ ] 05-load-balancing-scaling — зависит от: fundamentals, kubernetes-basics
- [ ] 06-database-sharding-replication — зависит от: sql-optimization, fundamentals
- [ ] 07-real-world-systems — зависит от: все предыдущие system-design темы

### 22. DevOps (продвинутые)
- [ ] 04-monitoring-logging — зависит от: kubernetes-basics, middleware-pipeline
- [ ] 05-cloud-azure-aws — зависит от: kubernetes-basics, ci-cd

### 23. Leadership & Soft Skills
- [ ] 01-code-review-culture — зависит от: solid, design-patterns
- [ ] 02-technical-decisions — зависит от: clean-architecture, system-design-fundamentals
- [ ] 03-mentoring — зависит от: code-review-culture
- [ ] 04-architecture-review — зависит от: microservices, modular-monolith
- [ ] 05-behavioral-interview — _нет зависимостей, можно начинать на любом уровне_
