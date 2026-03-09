# Индекс проекта

> Карта всех файлов проекта. Claude читает этот файл для навигации вместо сканирования директорий.
> Обновляется автоматически при создании/удалении тем (скилл `/create-topic`, `/rebalance`).

## Корневые файлы

| Файл | Назначение |
|------|-----------|
| `CLAUDE.md` | Инструкции для Claude — режимы, команды, правила |
| `INDEX.md` | Этот файл — карта проекта |
| `MEMORY.md` | Персистентная память Claude между сессиями |
| `learner-profile.md` | Профиль ученика — стиль, предпочтения, фидбек |
| `tracks/dotnet/weak-spots.md` | Пробелы и слабые места (.NET трек) |
| `improvements.md` | Идеи по улучшению системы (заполняется Claude) |

## Скиллы

| Скилл | Путь | Триггеры |
|-------|------|----------|
| learn | `.claude/skills/learn/SKILL.md` | `да`/`давай`/`продолжим`, `учим [тема]` |
| save-session | `.claude/skills/save-session/SKILL.md` | `сохрани`, `стоп` |
| create-topic | `.claude/skills/create-topic/SKILL.md` | `добавь тему`, `новая тема` |
| rebalance | `.claude/skills/rebalance/SKILL.md` | `разбей тему` |
| assess | `.claude/skills/assess/SKILL.md` | `оцени меня` |
| verify | `.claude/skills/verify/SKILL.md` | `проверь`, после `/save-session` |

## Шаблоны

| Шаблон | Путь | Для чего |
|--------|------|----------|
| Подтема (листовой узел) | `templates/topic/` | 11 файлов: summary, cheatsheet, interview-questions, interview-answers, practice, practice-solutions, cases, diagram, resources, learning-plan, session |
| Раздел (родительский узел) | `templates/section/` | 4 файла: overview, cheatsheet, progress, section-exam |

## Трек: dotnet

**Путь:** `tracks/dotnet/`

### Мета-файлы трека

| Файл | Путь |
|------|------|
| Roadmap | `tracks/dotnet/roadmap.md` |
| Progress | `tracks/dotnet/progress.md` |
| Dependency Graph | `tracks/dotnet/dependency-graph.md` |
| Glossary | `tracks/dotnet/glossary.md` |
| Repetition Log | `tracks/dotnet/repetition-log.md` |

### Разделы и подтемы

#### 01-csharp-fundamentals (10 подтем, Junior)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/01-csharp-fundamentals/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/01-csharp-fundamentals/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/01-csharp-fundamentals/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/01-csharp-fundamentals/section-exam.md` |

| Подтема | Путь |
|---------|------|
| Type System | `tracks/dotnet/topics/01-csharp-fundamentals/01-type-system/` |
| Value vs Reference | `tracks/dotnet/topics/01-csharp-fundamentals/02-value-vs-reference/` |
| Memory: Stack & Heap | `tracks/dotnet/topics/01-csharp-fundamentals/03-memory-stack-heap/` |
| Garbage Collector | `tracks/dotnet/topics/01-csharp-fundamentals/04-garbage-collector/` |
| Strings & Immutability | `tracks/dotnet/topics/01-csharp-fundamentals/05-strings-immutability/` |
| Exceptions | `tracks/dotnet/topics/01-csharp-fundamentals/06-exceptions/` |
| Nullable | `tracks/dotnet/topics/01-csharp-fundamentals/07-nullable/` |
| Extension Methods | `tracks/dotnet/topics/01-csharp-fundamentals/08-extension-methods/` |
| Pattern Matching | `tracks/dotnet/topics/01-csharp-fundamentals/09-pattern-matching/` |
| Records & Structs | `tracks/dotnet/topics/01-csharp-fundamentals/10-records-structs/` |

#### 02-oop-and-language (9 подтем, Junior → Middle)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/02-oop-and-language/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/02-oop-and-language/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/02-oop-and-language/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/02-oop-and-language/section-exam.md` |

| Подтема | Путь |
|---------|------|
| Inheritance & Polymorphism | `tracks/dotnet/topics/02-oop-and-language/01-inheritance-polymorphism/` |
| Interfaces & Abstract | `tracks/dotnet/topics/02-oop-and-language/02-interfaces-abstract/` |
| Generics | `tracks/dotnet/topics/02-oop-and-language/03-generics/` |
| Delegates & Events | `tracks/dotnet/topics/02-oop-and-language/04-delegates-events/` |
| LINQ | `tracks/dotnet/topics/02-oop-and-language/05-linq/` |
| Expression Trees | `tracks/dotnet/topics/02-oop-and-language/06-expression-trees/` |
| Reflection | `tracks/dotnet/topics/02-oop-and-language/07-reflection/` |
| Iterators & yield | `tracks/dotnet/topics/02-oop-and-language/08-iterators-yield/` |
| Covariance & Contravariance | `tracks/dotnet/topics/02-oop-and-language/09-covariance-contravariance/` |

#### 03-collections-data-structures (7 подтем, Junior → Middle)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/03-collections-data-structures/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/03-collections-data-structures/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/03-collections-data-structures/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/03-collections-data-structures/section-exam.md` |

| Подтема | Путь |
|---------|------|
| Arrays & Lists | `tracks/dotnet/topics/03-collections-data-structures/01-arrays-lists/` |
| Dictionary & HashSet | `tracks/dotnet/topics/03-collections-data-structures/02-dictionary-hashset/` |
| Concurrent Collections | `tracks/dotnet/topics/03-collections-data-structures/03-concurrent-collections/` |
| Span & Memory | `tracks/dotnet/topics/03-collections-data-structures/04-span-memory/` |
| Custom Collections | `tracks/dotnet/topics/03-collections-data-structures/05-custom-collections/` |
| Immutable Collections | `tracks/dotnet/topics/03-collections-data-structures/06-immutable-collections/` |
| Stack, Queue & PriorityQueue | `tracks/dotnet/topics/03-collections-data-structures/07-stack-queue-priorityqueue/` |

#### 04-async-multithreading (8 подтем, Middle)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/04-async-multithreading/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/04-async-multithreading/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/04-async-multithreading/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/04-async-multithreading/section-exam.md` |

| Подтема | Путь |
|---------|------|
| Threads & ThreadPool | `tracks/dotnet/topics/04-async-multithreading/01-threads-threadpool/` |
| Task & async/await | `tracks/dotnet/topics/04-async-multithreading/02-task-async-await/` |
| Synchronization Primitives | `tracks/dotnet/topics/04-async-multithreading/03-synchronization-primitives/` |
| Parallel & PLINQ | `tracks/dotnet/topics/04-async-multithreading/04-parallel-plinq/` |
| Channels | `tracks/dotnet/topics/04-async-multithreading/05-channels/` |
| Cancellation Patterns | `tracks/dotnet/topics/04-async-multithreading/06-cancellation-patterns/` |
| Async Streams (IAsyncEnumerable) | `tracks/dotnet/topics/04-async-multithreading/07-async-streams/` |
| ValueTask | `tracks/dotnet/topics/04-async-multithreading/08-valuetask/` |

#### 05-dotnet-internals (5 подтем, Senior)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/05-dotnet-internals/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/05-dotnet-internals/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/05-dotnet-internals/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/05-dotnet-internals/section-exam.md` |

| Подтема | Путь |
|---------|------|
| CLR & JIT | `tracks/dotnet/topics/05-dotnet-internals/01-clr-jit/` |
| Assembly Loading | `tracks/dotnet/topics/05-dotnet-internals/02-assembly-loading/` |
| GC Internals | `tracks/dotnet/topics/05-dotnet-internals/03-gc-internals/` |
| Threading Model | `tracks/dotnet/topics/05-dotnet-internals/04-threading-model/` |
| Performance Diagnostics | `tracks/dotnet/topics/05-dotnet-internals/05-performance-diagnostics/` |

#### 06-asp-net-core (13 подтем, Middle)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/06-asp-net-core/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/06-asp-net-core/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/06-asp-net-core/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/06-asp-net-core/section-exam.md` |

| Подтема | Путь |
|---------|------|
| Middleware Pipeline | `tracks/dotnet/topics/06-asp-net-core/01-middleware-pipeline/` |
| Dependency Injection | `tracks/dotnet/topics/06-asp-net-core/02-dependency-injection/` |
| Routing & Controllers | `tracks/dotnet/topics/06-asp-net-core/03-routing-controllers/` |
| Authentication & Authorization | `tracks/dotnet/topics/06-asp-net-core/04-authentication-authorization/` |
| Filters & Model Binding | `tracks/dotnet/topics/06-asp-net-core/05-filters-model-binding/` |
| Minimal API | `tracks/dotnet/topics/06-asp-net-core/06-minimal-api/` |
| SignalR & gRPC | `tracks/dotnet/topics/06-asp-net-core/07-signalr-grpc/` |
| HTTP Clients & IHttpClientFactory | `tracks/dotnet/topics/06-asp-net-core/08-http-clients/` |
| Configuration & Options Pattern | `tracks/dotnet/topics/06-asp-net-core/09-configuration-options/` |
| Logging & Structured Logs | `tracks/dotnet/topics/06-asp-net-core/10-logging-structured/` |
| Background Services (IHostedService) | `tracks/dotnet/topics/06-asp-net-core/11-background-services/` |
| Health Checks | `tracks/dotnet/topics/06-asp-net-core/12-health-checks/` |
| API Versioning | `tracks/dotnet/topics/06-asp-net-core/13-api-versioning/` |

#### 07-data-access (6 подтем, Middle → Senior)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/07-data-access/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/07-data-access/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/07-data-access/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/07-data-access/section-exam.md` |

| Подтема | Путь |
|---------|------|
| EF Core Basics | `tracks/dotnet/topics/07-data-access/01-ef-core-basics/` |
| EF Core Advanced | `tracks/dotnet/topics/07-data-access/02-ef-core-advanced/` |
| Dapper | `tracks/dotnet/topics/07-data-access/03-dapper/` |
| SQL Optimization | `tracks/dotnet/topics/07-data-access/04-sql-optimization/` |
| Migrations Strategies | `tracks/dotnet/topics/07-data-access/05-migrations-strategies/` |
| NoSQL: Redis & MongoDB | `tracks/dotnet/topics/07-data-access/06-nosql-redis-mongo/` |

#### 08-design-patterns (5 подтем, Middle)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/08-design-patterns/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/08-design-patterns/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/08-design-patterns/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/08-design-patterns/section-exam.md` |

| Подтема | Путь |
|---------|------|
| Creational | `tracks/dotnet/topics/08-design-patterns/01-creational/` |
| Structural | `tracks/dotnet/topics/08-design-patterns/02-structural/` |
| Behavioral | `tracks/dotnet/topics/08-design-patterns/03-behavioral/` |
| Patterns in .NET | `tracks/dotnet/topics/08-design-patterns/04-patterns-in-dotnet/` |
| Concurrency Patterns | `tracks/dotnet/topics/08-design-patterns/05-concurrency-patterns/` |

#### 09-architecture (9 подтем, Senior → Architect)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/09-architecture/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/09-architecture/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/09-architecture/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/09-architecture/section-exam.md` |

| Подтема | Путь |
|---------|------|
| SOLID | `tracks/dotnet/topics/09-architecture/01-solid/` |
| Clean Architecture | `tracks/dotnet/topics/09-architecture/02-clean-architecture/` |
| DDD | `tracks/dotnet/topics/09-architecture/03-ddd/` |
| CQRS & Event Sourcing | `tracks/dotnet/topics/09-architecture/04-cqrs-event-sourcing/` |
| Microservices | `tracks/dotnet/topics/09-architecture/05-microservices/` |
| Modular Monolith | `tracks/dotnet/topics/09-architecture/06-modular-monolith/` |
| Hexagonal / Ports & Adapters | `tracks/dotnet/topics/09-architecture/07-hexagonal-ports-adapters/` |
| Saga Pattern | `tracks/dotnet/topics/09-architecture/08-saga-pattern/` |
| Outbox Pattern | `tracks/dotnet/topics/09-architecture/09-outbox-pattern/` |

#### 10-system-design (9 подтем, Senior → Architect)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/10-system-design/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/10-system-design/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/10-system-design/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/10-system-design/section-exam.md` |

| Подтема | Путь |
|---------|------|
| Fundamentals | `tracks/dotnet/topics/10-system-design/01-fundamentals/` |
| Messaging & Queues | `tracks/dotnet/topics/10-system-design/02-messaging-queues/` |
| Caching Strategies | `tracks/dotnet/topics/10-system-design/03-caching-strategies/` |
| API Design | `tracks/dotnet/topics/10-system-design/04-api-design/` |
| Load Balancing & Scaling | `tracks/dotnet/topics/10-system-design/05-load-balancing-scaling/` |
| Database Sharding & Replication | `tracks/dotnet/topics/10-system-design/06-database-sharding-replication/` |
| Real-World Systems | `tracks/dotnet/topics/10-system-design/07-real-world-systems/` |
| CAP Theorem | `tracks/dotnet/topics/10-system-design/08-cap-theorem/` |
| Circuit Breaker & Resilience | `tracks/dotnet/topics/10-system-design/09-circuit-breaker-resilience/` |

#### 11-testing (5 подтем, Middle → Senior)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/11-testing/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/11-testing/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/11-testing/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/11-testing/section-exam.md` |

| Подтема | Путь |
|---------|------|
| Unit Testing | `tracks/dotnet/topics/11-testing/01-unit-testing/` |
| Integration Testing | `tracks/dotnet/topics/11-testing/02-integration-testing/` |
| Mocking Strategies | `tracks/dotnet/topics/11-testing/03-mocking-strategies/` |
| TDD & BDD | `tracks/dotnet/topics/11-testing/04-tdd-bdd/` |
| Load Testing | `tracks/dotnet/topics/11-testing/05-load-testing/` |

#### 12-devops-infrastructure (5 подтем, Senior → Architect)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/12-devops-infrastructure/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/12-devops-infrastructure/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/12-devops-infrastructure/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/12-devops-infrastructure/section-exam.md` |

| Подтема | Путь |
|---------|------|
| Docker & Containers | `tracks/dotnet/topics/12-devops-infrastructure/01-docker-containers/` |
| CI/CD | `tracks/dotnet/topics/12-devops-infrastructure/02-ci-cd/` |
| Kubernetes Basics | `tracks/dotnet/topics/12-devops-infrastructure/03-kubernetes-basics/` |
| Monitoring & Logging | `tracks/dotnet/topics/12-devops-infrastructure/04-monitoring-logging/` |
| Cloud: Azure & AWS | `tracks/dotnet/topics/12-devops-infrastructure/05-cloud-azure-aws/` |

#### 13-algorithms (7 подтем, Junior → Middle)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/13-algorithms/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/13-algorithms/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/13-algorithms/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/13-algorithms/section-exam.md` |

| Подтема | Путь |
|---------|------|
| Complexity & Big O | `tracks/dotnet/topics/13-algorithms/01-complexity-big-o/` |
| Sorting & Searching | `tracks/dotnet/topics/13-algorithms/02-sorting-searching/` |
| Trees & Graphs | `tracks/dotnet/topics/13-algorithms/03-trees-graphs/` |
| Dynamic Programming | `tracks/dotnet/topics/13-algorithms/04-dynamic-programming/` |
| Common Interview Problems | `tracks/dotnet/topics/13-algorithms/05-common-interview-problems/` |
| String Algorithms | `tracks/dotnet/topics/13-algorithms/06-string-algorithms/` |
| Greedy Algorithms | `tracks/dotnet/topics/13-algorithms/07-greedy-algorithms/` |

#### 14-security (6 подтем, Senior)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/14-security/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/14-security/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/14-security/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/14-security/section-exam.md` |

| Подтема | Путь |
|---------|------|
| OWASP Top 10 | `tracks/dotnet/topics/14-security/01-owasp-top10/` |
| Cryptography Basics | `tracks/dotnet/topics/14-security/02-cryptography-basics/` |
| Auth Patterns | `tracks/dotnet/topics/14-security/03-auth-patterns/` |
| Secure Coding | `tracks/dotnet/topics/14-security/04-secure-coding/` |
| Data Protection API | `tracks/dotnet/topics/14-security/05-data-protection-api/` |
| Secret Management | `tracks/dotnet/topics/14-security/06-secret-management/` |

#### 15-leadership-soft-skills (5 подтем, Architect)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/15-leadership-soft-skills/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/15-leadership-soft-skills/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/15-leadership-soft-skills/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/15-leadership-soft-skills/section-exam.md` |

| Подтема | Путь |
|---------|------|
| Code Review Culture | `tracks/dotnet/topics/15-leadership-soft-skills/01-code-review-culture/` |
| Technical Decisions | `tracks/dotnet/topics/15-leadership-soft-skills/02-technical-decisions/` |
| Mentoring | `tracks/dotnet/topics/15-leadership-soft-skills/03-mentoring/` |
| Architecture Review | `tracks/dotnet/topics/15-leadership-soft-skills/04-architecture-review/` |
| Behavioral Interview | `tracks/dotnet/topics/15-leadership-soft-skills/05-behavioral-interview/` |

## Другие директории

| Путь | Назначение |
|------|-----------|
| `mock-interviews/template.md` | Шаблон mock-интервью |
| `mock-interviews/log/` | Логи проведённых интервью |
| `flashcards/` | Флэш-карточки по темам |
| `docs/designs/` | Дизайн-документы |
| `docs/plans/` | Планы реализации |
