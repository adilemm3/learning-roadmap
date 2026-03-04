# Как воспроизвести эту систему обучения

> Скопируй этот файл, отправь в Claude Code, и он создаст тебе такую же систему с нуля.
> Перед запуском отредактируй секцию **«Настройки»** под себя.

---

## Настройки

Перед отправкой Claude — заполни эти поля:

```yaml
Имя: Адиль                          # ← замени на своё
GitHub username: adilemm3            # ← замени на свой
Название проекта: learning-roadmap   # ← можешь изменить
Директория: ~/learning-roadmap       # ← где создать
GitHub: public                       # public или private
Первый трек: dotnet                  # название трека (dotnet, golang, python, etc.)
Описание трека: ".NET/C# — от Junior до Architect"
```

---

## Инструкция для Claude Code

> **Скопируй всё ниже и отправь в Claude Code одним сообщением.**

---

Создай персональную систему обучения. Выполни всё за один проход.

### 1. Инициализация

Создай директорию `~/learning-roadmap`, инициализируй git, создай `.gitignore` (игнорируй `.DS_Store`, `*.swp`, `tmp/`, `.obsidian/`).

### 2. Структура директорий

```
learning-roadmap/
├── CLAUDE.md                    # инструкции для Claude — режимы работы, команды
├── SETUP.md                     # этот файл — как воспроизвести систему
├── .claude/
│   └── settings.json            # хуки для авто-коммитов
├── weak-spots.md                # общие пробелы (кросс-трековые)
├── tracks/
│   └── <track-name>/            # например: dotnet, golang, python
│       ├── roadmap.md           # дерево тем с порядком изучения и зависимостями
│       ├── progress.md          # таблица прогресса по всем темам
│       ├── dependency-graph.md  # граф зависимостей между темами (mermaid)
│       └── topics/
│           ├── 01-section-name/
│           │   ├── 01-topic-name/
│           │   │   ├── summary.md
│           │   │   ├── cheatsheet.md
│           │   │   ├── interview-questions.md
│           │   │   ├── practice.md
│           │   │   ├── cases.md
│           │   │   ├── diagram.md
│           │   │   └── resources.md
│           │   ├── 02-topic-name/
│           │   └── ...
│           ├── 02-section-name/
│           └── ...
├── mock-interviews/
│   ├── template.md
│   └── log/
└── flashcards/
    └── README.md
```

### 3. Темы трека

Раздели темы на 4 уровня: Junior, Middle, Senior, Architect. Каждый уровень строится на предыдущем. Количество разделов и подтем зависит от технологии, но ориентируйся на 10-15 разделов по 3-7 подтем.

**Для .NET/C# трека используй эту структуру:**

```
01-csharp-fundamentals/
    01-type-system, 02-value-vs-reference, 03-memory-stack-heap,
    04-garbage-collector, 05-strings-immutability, 06-exceptions, 07-nullable
02-oop-and-language/
    01-inheritance-polymorphism, 02-interfaces-abstract, 03-generics,
    04-delegates-events, 05-linq, 06-expression-trees, 07-reflection
03-collections-data-structures/
    01-arrays-lists, 02-dictionary-hashset, 03-concurrent-collections,
    04-span-memory, 05-custom-collections
04-async-multithreading/
    01-threads-threadpool, 02-task-async-await, 03-synchronization-primitives,
    04-parallel-plinq, 05-channels, 06-cancellation-patterns
05-dotnet-internals/
    01-clr-jit, 02-assembly-loading, 03-gc-internals,
    04-threading-model, 05-performance-diagnostics
06-asp-net-core/
    01-middleware-pipeline, 02-dependency-injection, 03-routing-controllers,
    04-authentication-authorization, 05-filters-model-binding, 06-minimal-api,
    07-signalr-grpc
07-data-access/
    01-ef-core-basics, 02-ef-core-advanced, 03-dapper,
    04-sql-optimization, 05-migrations-strategies, 06-nosql-redis-mongo
08-design-patterns/
    01-creational, 02-structural, 03-behavioral, 04-patterns-in-dotnet
09-architecture/
    01-solid, 02-clean-architecture, 03-ddd, 04-cqrs-event-sourcing,
    05-microservices, 06-modular-monolith, 07-hexagonal-ports-adapters
10-system-design/
    01-fundamentals, 02-messaging-queues, 03-caching-strategies,
    04-api-design, 05-load-balancing-scaling, 06-database-sharding-replication,
    07-real-world-systems
11-testing/
    01-unit-testing, 02-integration-testing, 03-mocking-strategies,
    04-tdd-bdd, 05-load-testing
12-devops-infrastructure/
    01-docker-containers, 02-ci-cd, 03-kubernetes-basics,
    04-monitoring-logging, 05-cloud-azure-aws
13-algorithms/
    01-complexity-big-o, 02-sorting-searching, 03-trees-graphs,
    04-dynamic-programming, 05-common-interview-problems
14-security/
    01-owasp-top10, 02-cryptography-basics, 03-auth-patterns, 04-secure-coding
15-leadership-soft-skills/
    01-code-review-culture, 02-technical-decisions, 03-mentoring,
    04-architecture-review, 05-behavioral-interview
```

**Для другого трека** — сгенерируй аналогичную структуру, подходящую для выбранной технологии, сохраняя тот же формат (15 разделов, 4 уровня).

### 4. Файлы каждой подтемы (7 штук)

Каждая подтема содержит 7 файлов со скелетной структурой:

**summary.md:**
```markdown
# [Название темы]
> Уровень: Junior / Middle / Senior / Architect
> Зависимости: [список тем-пререквизитов]

## Ключевые концепции
## Объяснение простыми словами
## Примеры кода
## Частые вопросы на собесе
## Подводные камни и нюансы
## Связь с другими темами
```

**cheatsheet.md:**
```markdown
# [Тема] — Шпаргалка
> Время чтения: ~2 мин | Формат: для просмотра с телефона

## Краткая суть
## Ключевые моменты
## Сравнительная таблица
## Код в одну строку
## Запомни
```

**interview-questions.md:**
```markdown
# [Тема] — Вопросы для собеседования

## 🟢 Junior
## 🟡 Middle
## 🔴 Senior
## 🏛 Architect

---
<details><summary>Ответы</summary>
<!-- ответы -->
</details>
```

**practice.md:**
```markdown
# [Тема] — Практика

## Мини-задачи
### 🟢 Easy: [название]
### 🟡 Medium: [название]
### 🔴 Hard: [название]

## Код-ревью
## Рефакторинг
```

**cases.md:**
```markdown
# [Тема] — Реальные кейсы

## Кейс 1: [название]
**Контекст / Проблема / Решение / Выводы**

## Постмортем
## Trade-off анализ
```

**diagram.md:**
```markdown
# [Тема] — Схемы и диаграммы

## Концептуальная схема (ASCII)
## Sequence Diagram (mermaid)
## Компонентная диаграмма
```

**resources.md:**
```markdown
# [Тема] — Источники

## Документация
## Книги
## Статьи и блоги
## Видео и доклады
## Практика
```

### 5. roadmap.md

Создай полный роадмап с порядком изучения, разбитый на 4 уровня (Junior → Middle → Senior → Architect). Для каждой темы укажи зависимости.

### 6. dependency-graph.md

Создай граф зависимостей в формате mermaid. Покрой все ключевые связи. Стилизуй ноды по уровням (цвета: зелёный=Junior, жёлтый=Middle, красный=Senior, фиолетовый=Architect).

### 7. progress.md

Таблица всех подтем: `# | Раздел | Тема | Уровень | Статус | Уверенность (1-5) | Последняя сессия`. Все статусы — `⬜ не начата`, уверенность — `0`. В конце — сводная таблица по уровням.

### 8. weak-spots.md

```markdown
# Слабые места и пробелы
## Активные
## Закрытые
```

### 9. mock-interviews/template.md

Шаблон для mock-интервью: формат, уровень, вопросы с оценками, общая оценка, сильные стороны, что улучшить, план действий.

### 10. flashcards/README.md

Описание формата флэш-карточек (Q/A с `<details>` тегами для ответов).

### 11. CLAUDE.md

Напиши CLAUDE.md с:
- **Назначением** системы (ментор, интервьюер, наставник)
- **Принципами** (русский язык, аналогия → теория → код, контрольные вопросы, мобильный формат)
- **Режимами работы** — все команды:
  - `учим [тема]`, `шпаргалка [тема]`, `вопросы [тема]`, `практика [тема]`
  - `кейс [тема]`, `схема [тема]`, `карточки [тема]`
  - `собес [уровень]`, `собес system-design`
  - `оцени меня [тема]`, `прогресс`, `что дальше`, `слабые места`
  - `сохрани`, `запуши`
- **Оценкой уровня** (3-5 вопросов → определение уровня → обновление progress)
- **Сохранением сессий** (спросить перед выходом, обновить файлы)
- **Навигацией** (полный путь, короткое имя, номер из progress)

### 12. Хуки .claude/settings.json

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "command": "cd ~/learning-roadmap && git add -A && git diff --cached --quiet || git commit -m \"auto: update $(date +%Y-%m-%d_%H:%M)\""
      }
    ]
  }
}
```

### 13. Первый коммит

```bash
git add -A && git commit -m "init: персональная система обучения (junior → architect)"
```

### 14. GitHub

Создай репозиторий на GitHub (public/private по настройке выше) и запуши.

### 15. После создания

Выведи:
- Краткую справку по всем командам
- Статистику: сколько тем, подтем, файлов создано
- Предложи начать с оценки текущего уровня

---

## Как добавить новый трек

1. Скажи Claude: `добавь трек [название]` (например: `добавь трек golang`)
2. Claude создаст `tracks/[название]/` с roadmap, progress, dependency-graph и topics
3. Структура тем будет сгенерирована под выбранную технологию
4. Все команды (`учим`, `собес`, `прогресс` и т.д.) работают с указанием трека: `учим dotnet/linq` или `учим golang/goroutines`
