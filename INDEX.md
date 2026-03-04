# Индекс проекта

> Карта всех файлов проекта. Claude читает этот файл для навигации вместо сканирования директорий.
> Обновляется автоматически при создании/удалении тем (скилл `/create-topic`, `/rebalance`).

## Корневые файлы

| Файл | Назначение |
|------|-----------|
| `CLAUDE.md` | Инструкции для Claude — режимы, команды, правила |
| `INDEX.md` | Этот файл — карта проекта |
| `SETUP.md` | Как воспроизвести систему |
| `learner-profile.md` | Профиль ученика — стиль, предпочтения, фидбек |
| `weak-spots.md` | Пробелы и слабые места (кросс-трековые) |
| `improvements.md` | Идеи по улучшению системы (заполняется Claude) |

## Скиллы

| Скилл | Путь | Триггеры |
|-------|------|----------|
| learn | `.claude/skills/learn/SKILL.md` | `учим`, `продолжить`, `дальше` |
| save-session | `.claude/skills/save-session/SKILL.md` | `сохрани`, `стоп` |
| create-topic | `.claude/skills/create-topic/SKILL.md` | `добавь тему`, `новая тема` |
| rebalance | `.claude/skills/rebalance/SKILL.md` | `разбей тему` |
| assess | `.claude/skills/assess/SKILL.md` | `оцени меня` |
| verify | `.claude/skills/verify/SKILL.md` | `проверь`, после `/save-session` |

## Шаблоны

| Шаблон | Путь | Для чего |
|--------|------|----------|
| Подтема (листовой узел) | `templates/topic/` | 9 файлов: summary, cheatsheet, interview-questions, practice, cases, diagram, resources, learning-plan, session |
| Раздел (родительский узел) | `templates/section/` | 4 файла: overview, cheatsheet, progress, section-exam |

## Трек: dotnet

**Путь:** `tracks/dotnet/`

### Мета-файлы трека

| Файл | Путь |
|------|------|
| Roadmap | `tracks/dotnet/roadmap.md` |
| Progress | `tracks/dotnet/progress.md` |
| Dependency Graph | `tracks/dotnet/dependency-graph.md` |

### Разделы и подтемы

#### 01-csharp-fundamentals (7 подтем, Junior)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/01-csharp-fundamentals/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/01-csharp-fundamentals/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/01-csharp-fundamentals/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/01-csharp-fundamentals/section-exam.md` |

| # | Подтема | Путь |
|---|---------|------|
| 1 | Type System | `tracks/dotnet/topics/01-csharp-fundamentals/01-type-system/` |
| 2 | Value vs Reference | `tracks/dotnet/topics/01-csharp-fundamentals/02-value-vs-reference/` |
| 3 | Memory: Stack & Heap | `tracks/dotnet/topics/01-csharp-fundamentals/03-memory-stack-heap/` |
| 4 | Garbage Collector | `tracks/dotnet/topics/01-csharp-fundamentals/04-garbage-collector/` |
| 5 | Strings & Immutability | `tracks/dotnet/topics/01-csharp-fundamentals/05-strings-immutability/` |
| 6 | Exceptions | `tracks/dotnet/topics/01-csharp-fundamentals/06-exceptions/` |
| 7 | Nullable | `tracks/dotnet/topics/01-csharp-fundamentals/07-nullable/` |

#### 02-oop-and-language (7 подтем, Junior → Middle)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/02-oop-and-language/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/02-oop-and-language/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/02-oop-and-language/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/02-oop-and-language/section-exam.md` |

| # | Подтема | Путь |
|---|---------|------|
| 8 | Inheritance & Polymorphism | `tracks/dotnet/topics/02-oop-and-language/01-inheritance-polymorphism/` |
| 9 | Interfaces & Abstract | `tracks/dotnet/topics/02-oop-and-language/02-interfaces-abstract/` |
| 10 | Generics | `tracks/dotnet/topics/02-oop-and-language/03-generics/` |
| 11 | Delegates & Events | `tracks/dotnet/topics/02-oop-and-language/04-delegates-events/` |
| 12 | LINQ | `tracks/dotnet/topics/02-oop-and-language/05-linq/` |
| 13 | Expression Trees | `tracks/dotnet/topics/02-oop-and-language/06-expression-trees/` |
| 14 | Reflection | `tracks/dotnet/topics/02-oop-and-language/07-reflection/` |

#### 03-collections-data-structures (5 подтем, Junior → Middle)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/03-collections-data-structures/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/03-collections-data-structures/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/03-collections-data-structures/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/03-collections-data-structures/section-exam.md` |

| # | Подтема | Путь |
|---|---------|------|
| 15 | Arrays & Lists | `tracks/dotnet/topics/03-collections-data-structures/01-arrays-lists/` |
| 16 | Dictionary & HashSet | `tracks/dotnet/topics/03-collections-data-structures/02-dictionary-hashset/` |
| 17 | Concurrent Collections | `tracks/dotnet/topics/03-collections-data-structures/03-concurrent-collections/` |
| 18 | Span & Memory | `tracks/dotnet/topics/03-collections-data-structures/04-span-memory/` |
| 19 | Custom Collections | `tracks/dotnet/topics/03-collections-data-structures/05-custom-collections/` |

#### 04-async-multithreading (6 подтем, Middle)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/04-async-multithreading/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/04-async-multithreading/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/04-async-multithreading/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/04-async-multithreading/section-exam.md` |

| # | Подтема | Путь |
|---|---------|------|
| 20 | Threads & ThreadPool | `tracks/dotnet/topics/04-async-multithreading/01-threads-threadpool/` |
| 21 | Task & async/await | `tracks/dotnet/topics/04-async-multithreading/02-task-async-await/` |
| 22 | Synchronization Primitives | `tracks/dotnet/topics/04-async-multithreading/03-synchronization-primitives/` |
| 23 | Parallel & PLINQ | `tracks/dotnet/topics/04-async-multithreading/04-parallel-plinq/` |
| 24 | Channels | `tracks/dotnet/topics/04-async-multithreading/05-channels/` |
| 25 | Cancellation Patterns | `tracks/dotnet/topics/04-async-multithreading/06-cancellation-patterns/` |

#### 05-dotnet-internals (5 подтем, Senior)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/05-dotnet-internals/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/05-dotnet-internals/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/05-dotnet-internals/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/05-dotnet-internals/section-exam.md` |

| # | Подтема | Путь |
|---|---------|------|
| 26 | CLR & JIT | `tracks/dotnet/topics/05-dotnet-internals/01-clr-jit/` |
| 27 | Assembly Loading | `tracks/dotnet/topics/05-dotnet-internals/02-assembly-loading/` |
| 28 | GC Internals | `tracks/dotnet/topics/05-dotnet-internals/03-gc-internals/` |
| 29 | Threading Model | `tracks/dotnet/topics/05-dotnet-internals/04-threading-model/` |
| 30 | Performance Diagnostics | `tracks/dotnet/topics/05-dotnet-internals/05-performance-diagnostics/` |

#### 06-asp-net-core (7 подтем, Middle)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/06-asp-net-core/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/06-asp-net-core/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/06-asp-net-core/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/06-asp-net-core/section-exam.md` |

| # | Подтема | Путь |
|---|---------|------|
| 31 | Middleware Pipeline | `tracks/dotnet/topics/06-asp-net-core/01-middleware-pipeline/` |
| 32 | Dependency Injection | `tracks/dotnet/topics/06-asp-net-core/02-dependency-injection/` |
| 33 | Routing & Controllers | `tracks/dotnet/topics/06-asp-net-core/03-routing-controllers/` |
| 34 | Authentication & Authorization | `tracks/dotnet/topics/06-asp-net-core/04-authentication-authorization/` |
| 35 | Filters & Model Binding | `tracks/dotnet/topics/06-asp-net-core/05-filters-model-binding/` |
| 36 | Minimal API | `tracks/dotnet/topics/06-asp-net-core/06-minimal-api/` |
| 37 | SignalR & gRPC | `tracks/dotnet/topics/06-asp-net-core/07-signalr-grpc/` |

#### 07-data-access (6 подтем, Middle → Senior)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/07-data-access/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/07-data-access/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/07-data-access/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/07-data-access/section-exam.md` |

| # | Подтема | Путь |
|---|---------|------|
| 38 | EF Core Basics | `tracks/dotnet/topics/07-data-access/01-ef-core-basics/` |
| 39 | EF Core Advanced | `tracks/dotnet/topics/07-data-access/02-ef-core-advanced/` |
| 40 | Dapper | `tracks/dotnet/topics/07-data-access/03-dapper/` |
| 41 | SQL Optimization | `tracks/dotnet/topics/07-data-access/04-sql-optimization/` |
| 42 | Migrations Strategies | `tracks/dotnet/topics/07-data-access/05-migrations-strategies/` |
| 43 | NoSQL: Redis & MongoDB | `tracks/dotnet/topics/07-data-access/06-nosql-redis-mongo/` |

#### 08-design-patterns (4 подтемы, Middle)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/08-design-patterns/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/08-design-patterns/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/08-design-patterns/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/08-design-patterns/section-exam.md` |

| # | Подтема | Путь |
|---|---------|------|
| 44 | Creational | `tracks/dotnet/topics/08-design-patterns/01-creational/` |
| 45 | Structural | `tracks/dotnet/topics/08-design-patterns/02-structural/` |
| 46 | Behavioral | `tracks/dotnet/topics/08-design-patterns/03-behavioral/` |
| 47 | Patterns in .NET | `tracks/dotnet/topics/08-design-patterns/04-patterns-in-dotnet/` |

#### 09-architecture (7 подтем, Senior → Architect)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/09-architecture/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/09-architecture/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/09-architecture/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/09-architecture/section-exam.md` |

| # | Подтема | Путь |
|---|---------|------|
| 48 | SOLID | `tracks/dotnet/topics/09-architecture/01-solid/` |
| 49 | Clean Architecture | `tracks/dotnet/topics/09-architecture/02-clean-architecture/` |
| 50 | DDD | `tracks/dotnet/topics/09-architecture/03-ddd/` |
| 51 | CQRS & Event Sourcing | `tracks/dotnet/topics/09-architecture/04-cqrs-event-sourcing/` |
| 52 | Microservices | `tracks/dotnet/topics/09-architecture/05-microservices/` |
| 53 | Modular Monolith | `tracks/dotnet/topics/09-architecture/06-modular-monolith/` |
| 54 | Hexagonal / Ports & Adapters | `tracks/dotnet/topics/09-architecture/07-hexagonal-ports-adapters/` |

#### 10-system-design (7 подтем, Senior → Architect)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/10-system-design/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/10-system-design/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/10-system-design/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/10-system-design/section-exam.md` |

| # | Подтема | Путь |
|---|---------|------|
| 55 | Fundamentals | `tracks/dotnet/topics/10-system-design/01-fundamentals/` |
| 56 | Messaging & Queues | `tracks/dotnet/topics/10-system-design/02-messaging-queues/` |
| 57 | Caching Strategies | `tracks/dotnet/topics/10-system-design/03-caching-strategies/` |
| 58 | API Design | `tracks/dotnet/topics/10-system-design/04-api-design/` |
| 59 | Load Balancing & Scaling | `tracks/dotnet/topics/10-system-design/05-load-balancing-scaling/` |
| 60 | Database Sharding & Replication | `tracks/dotnet/topics/10-system-design/06-database-sharding-replication/` |
| 61 | Real-World Systems | `tracks/dotnet/topics/10-system-design/07-real-world-systems/` |

#### 11-testing (5 подтем, Middle → Senior)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/11-testing/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/11-testing/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/11-testing/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/11-testing/section-exam.md` |

| # | Подтема | Путь |
|---|---------|------|
| 62 | Unit Testing | `tracks/dotnet/topics/11-testing/01-unit-testing/` |
| 63 | Integration Testing | `tracks/dotnet/topics/11-testing/02-integration-testing/` |
| 64 | Mocking Strategies | `tracks/dotnet/topics/11-testing/03-mocking-strategies/` |
| 65 | TDD & BDD | `tracks/dotnet/topics/11-testing/04-tdd-bdd/` |
| 66 | Load Testing | `tracks/dotnet/topics/11-testing/05-load-testing/` |

#### 12-devops-infrastructure (5 подтем, Senior → Architect)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/12-devops-infrastructure/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/12-devops-infrastructure/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/12-devops-infrastructure/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/12-devops-infrastructure/section-exam.md` |

| # | Подтема | Путь |
|---|---------|------|
| 67 | Docker & Containers | `tracks/dotnet/topics/12-devops-infrastructure/01-docker-containers/` |
| 68 | CI/CD | `tracks/dotnet/topics/12-devops-infrastructure/02-ci-cd/` |
| 69 | Kubernetes Basics | `tracks/dotnet/topics/12-devops-infrastructure/03-kubernetes-basics/` |
| 70 | Monitoring & Logging | `tracks/dotnet/topics/12-devops-infrastructure/04-monitoring-logging/` |
| 71 | Cloud: Azure & AWS | `tracks/dotnet/topics/12-devops-infrastructure/05-cloud-azure-aws/` |

#### 13-algorithms (5 подтем, Junior → Middle)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/13-algorithms/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/13-algorithms/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/13-algorithms/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/13-algorithms/section-exam.md` |

| # | Подтема | Путь |
|---|---------|------|
| 72 | Complexity & Big O | `tracks/dotnet/topics/13-algorithms/01-complexity-big-o/` |
| 73 | Sorting & Searching | `tracks/dotnet/topics/13-algorithms/02-sorting-searching/` |
| 74 | Trees & Graphs | `tracks/dotnet/topics/13-algorithms/03-trees-graphs/` |
| 75 | Dynamic Programming | `tracks/dotnet/topics/13-algorithms/04-dynamic-programming/` |
| 76 | Common Interview Problems | `tracks/dotnet/topics/13-algorithms/05-common-interview-problems/` |

#### 14-security (4 подтемы, Senior)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/14-security/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/14-security/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/14-security/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/14-security/section-exam.md` |

| # | Подтема | Путь |
|---|---------|------|
| 77 | OWASP Top 10 | `tracks/dotnet/topics/14-security/01-owasp-top10/` |
| 78 | Cryptography Basics | `tracks/dotnet/topics/14-security/02-cryptography-basics/` |
| 79 | Auth Patterns | `tracks/dotnet/topics/14-security/03-auth-patterns/` |
| 80 | Secure Coding | `tracks/dotnet/topics/14-security/04-secure-coding/` |

#### 15-leadership-soft-skills (5 подтем, Architect)

Родительские файлы:
| Файл | Путь |
|------|------|
| Обзор | `tracks/dotnet/topics/15-leadership-soft-skills/overview.md` |
| Сводная шпаргалка | `tracks/dotnet/topics/15-leadership-soft-skills/cheatsheet.md` |
| Прогресс по разделу | `tracks/dotnet/topics/15-leadership-soft-skills/progress.md` |
| Экзамен по разделу | `tracks/dotnet/topics/15-leadership-soft-skills/section-exam.md` |

| # | Подтема | Путь |
|---|---------|------|
| 81 | Code Review Culture | `tracks/dotnet/topics/15-leadership-soft-skills/01-code-review-culture/` |
| 82 | Technical Decisions | `tracks/dotnet/topics/15-leadership-soft-skills/02-technical-decisions/` |
| 83 | Mentoring | `tracks/dotnet/topics/15-leadership-soft-skills/03-mentoring/` |
| 84 | Architecture Review | `tracks/dotnet/topics/15-leadership-soft-skills/04-architecture-review/` |
| 85 | Behavioral Interview | `tracks/dotnet/topics/15-leadership-soft-skills/05-behavioral-interview/` |

## Другие директории

| Путь | Назначение |
|------|-----------|
| `mock-interviews/template.md` | Шаблон mock-интервью |
| `mock-interviews/log/` | Логи проведённых интервью |
| `flashcards/` | Флэш-карточки по темам |
| `docs/designs/` | Дизайн-документы |
| `docs/plans/` | Планы реализации |
