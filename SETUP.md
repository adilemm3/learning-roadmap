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
├── INDEX.md                     # карта проекта — Claude читает для навигации
├── MEMORY.md                    # персистентная память Claude между сессиями
├── learner-profile.md           # профиль ученика — стиль, предпочтения, фидбек
├── weak-spots.md                # общие пробелы (кросс-трековые)
├── improvements.md              # идеи по улучшению системы (заполняется Claude)
├── scripts/
│   └── create-topic.sh          # создание темы (9 файлов за 1 вызов)
├── .claude/
│   ├── settings.json            # разрешения и хуки
│   └── skills/                  # скиллы автоматизации
│       ├── learn/SKILL.md       # Learn Mode — управляемый автопилот
│       ├── save-session/SKILL.md # сохранение прогресса (чеклист 7 шагов)
│       ├── create-topic/SKILL.md # создание новых тем
│       ├── rebalance/SKILL.md   # балансировка дерева тем
│       ├── assess/SKILL.md      # оценка уровня
│       └── verify/SKILL.md      # валидация и верификация файлов
├── templates/
│   ├── topic/                   # 9 файлов листового узла
│   └── section/                 # 4 файла родительского узла
├── tracks/
│   └── <track-name>/
│       ├── roadmap.md
│       ├── progress.md
│       ├── dependency-graph.md
│       └── topics/
│           ├── 01-section-name/
│           │   ├── overview.md          # описание раздела
│           │   ├── cheatsheet.md        # сводная шпаргалка (агрегация подтем)
│           │   ├── progress.md          # прогресс по подтемам раздела
│           │   ├── section-exam.md      # экзамен по разделу
│           │   ├── 01-topic-name/
│           │   │   ├── summary.md
│           │   │   ├── cheatsheet.md
│           │   │   ├── interview-questions.md
│           │   │   ├── practice.md
│           │   │   ├── cases.md
│           │   │   ├── diagram.md
│           │   │   ├── resources.md
│           │   │   ├── learning-plan.md # план изучения с блоками
│           │   │   └── session.md       # полный диалог всех сессий
│           │   └── 02-topic-name/
│           └── 02-section-name/
├── mock-interviews/
│   ├── template.md
│   └── log/
├── flashcards/
└── docs/
    ├── designs/
    └── plans/
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

### 4. Файлы каждой подтемы (9 штук)

Каждая подтема содержит 9 файлов со скелетной структурой:

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

**learning-plan.md:**
```markdown
# [Название] — План изучения
> Статус: ⬜ не начата
> Блок: 0/N | Последняя сессия: —

## Калибровка
- Базовые концепции: ⬜
- Средний уровень: ⬜
- Продвинутый: ⬜
→ Начинаем с блока: —

## Блоки
<!-- Claude генерирует блоки при первом входе в тему на основе калибровки -->
```

**session.md:**
```markdown
# [Название] — Сессии

<!-- Полный диалог всех учебных сессий по этой теме -->
```

### 5. Файлы родительского узла (раздела — 4 штуки)

Каждый раздел (`01-csharp-fundamentals/` и т.д.) содержит 4 файла:

**overview.md:**
```markdown
# [Раздел] — Обзор

## Описание
## Подтемы и порядок изучения
## Связи с другими разделами
## Пререквизиты
```

**cheatsheet.md:**
```markdown
# [Раздел] — Сводная шпаргалка

<!-- Агрегация из cheatsheet.md завершённых подтем -->
```

**progress.md:**
```markdown
# [Раздел] — Прогресс по разделу

| Подтема | Статус | Уверенность (1-5) | Последняя сессия |
|---------|--------|--------------------|------------------|
```

**section-exam.md:**
```markdown
# [Раздел] — Экзамен по разделу

<!-- Адаптивный экзамен после завершения всех подтем -->
## Формат
- Теория, код, кросс-темные, trade-off вопросы
- Минимум 5 вопросов
## Результат
<!-- Заполняется после проведения -->
```

### 6. roadmap.md

Создай полный роадмап с порядком изучения, разбитый на 4 уровня (Junior → Middle → Senior → Architect). Для каждой темы укажи зависимости.

### 7. dependency-graph.md

Создай граф зависимостей в формате mermaid. Покрой все ключевые связи. Стилизуй ноды по уровням (цвета: зелёный=Junior, жёлтый=Middle, красный=Senior, фиолетовый=Architect).

### 8. progress.md

Таблица всех подтем: `Раздел | Тема | Уровень | Статус | Уверенность (1-5) | Последняя сессия`. Без колонки `#` — вставка новых тем не требует перенумерации. Все статусы — `⬜ не начата`, уверенность — `0`. В конце — сводная таблица по уровням.

### 9. INDEX.md

Карта всех файлов проекта. Claude читает этот файл для навигации вместо сканирования директорий. Содержит:
- Корневые файлы (CLAUDE.md, INDEX.md, SETUP.md, MEMORY.md, learner-profile.md, weak-spots.md, improvements.md)
- Таблица скиллов с путями и триггерами
- Таблица шаблонов
- Для каждого раздела трека: родительские файлы + таблица подтем с путями

### 10. MEMORY.md

```markdown
# Learning Roadmap — Memory

> Персистентная память Claude между сессиями. Обновляется автоматически.

## Активный трек
[track-name]

## Активная тема
Тема: —
Блок: —
Путь: —

## Стиль ученика (кэш из learner-profile.md)
- Порядок: аналогия → теория → код
- Темп: не определён
- Глубина: не определена

## UX-правила
- Все файловые операции — через фоновых агентов, ученик не видит diff-ы
- Startup Protocol — через foreground-агента (один вызов)
- bypassPermissions включён — никаких системных промптов
- Коммиты только по команде ученика

## Заметки
```

### 11. learner-profile.md

```markdown
# Профиль ученика

## Основное
Имя: [имя]
Текущая роль: —
Опыт: — лет
Цель: Architect

## Стиль обучения
- Предпочитаемый порядок: аналогия → теория → код
- Темп: —
- Глубина: —
- Практика: —

## Что работает
<!-- заполняется по мере обучения -->

## Что НЕ работает
<!-- заполняется по мере обучения -->

## Паттерны обучения
<!-- Claude заполняет на основе микрофидбека -->
```

### 12. weak-spots.md

```markdown
# Слабые места и пробелы
## Активные
## Закрытые
```

### 13. improvements.md

```markdown
# Идеи по улучшению системы обучения

<!-- Claude записывает идеи через субагента в фоне, не прерывая обучение -->
<!-- Формат: - YYYY-MM-DD HH:MM | [контекст] описание -->
```

### 14. mock-interviews/template.md

Шаблон для mock-интервью: формат, уровень, вопросы с оценками, общая оценка, сильные стороны, что улучшить, план действий.

### 15. flashcards/README.md

Описание формата флэш-карточек (Q/A с `<details>` тегами для ответов).

### 16. .claude/settings.json

```json
{
  "model": "claude-sonnet-4-6",
  "permissions": {
    "allow": [
      "Read", "Write", "Edit", "Glob", "Grep",
      "Agent", "Bash(*)", "WebSearch", "WebFetch", "Skill"
    ],
    "deny": [],
    "defaultMode": "bypassPermissions"
  },
  "hooks": {}
}
```

**Ключевое:** `bypassPermissions` — никаких системных подтверждений. Все файловые операции невидимы для ученика (через фоновых агентов).

### 17. CLAUDE.md

Напиши CLAUDE.md с:
- **Назначением** системы (ментор, интервьюер, наставник)
- **Структурой проекта** (полное дерево файлов)
- **Startup Protocol** (5 шагов при каждом входе)
- **Принципами** (русский язык, аналогия → теория → код, контрольные вопросы, мобильный формат, ★ Insight)
- **Learn Mode** (вход, цикл, команды)
- **Другими режимами** (шпаргалка, вопросы, практика, кейс, схема, карточки, собес, аналитика)
- **Оценкой уровня** (3-5 вопросов → определение → обновление)
- **Навигацией** (полный путь, короткое имя)
- **Разрешениями:**
  - Файлы — читать/писать без подтверждения
  - Все файловые операции курса — через фоновых агентов (ученик не видит diff-ы)
  - Git push — ТОЛЬКО по команде
  - Коммиты — ТОЛЬКО по команде
- **Правилами обновления файлов** (таблица: событие → какие файлы обновить)
- **Идеями по улучшению** (improvements.md, фоновая запись)
- **Обязательными скиллами** (learn, save-session, create-topic, rebalance, assess, verify)

### 18. Скиллы автоматизации

Создай `.claude/skills/` с шестью скиллами:
- `learn/SKILL.md` — запуск и ведение обучения (startup через агента, цикл, обновление файлов через фоновых агентов)
- `save-session/SKILL.md` — чеклист 7 шагов (все через фонового агента, ученик видит только итог)
- `create-topic/SKILL.md` — создание новой темы (использует `scripts/create-topic.sh` + точечные правки мета-файлов)
- `rebalance/SKILL.md` — разбиение большой темы на подтемы
- `assess/SKILL.md` — оценка уровня через вопросы
- `verify/SKILL.md` — валидация консистентности между файлами (7 чеклистов)

### 19. Первый коммит

```bash
git add -A && git commit -m "init: персональная система обучения (junior → architect)"
```

### 20. GitHub

Создай репозиторий на GitHub (public/private по настройке выше) и запуши.

### 21. После создания

Выведи:
- Краткую справку по всем командам
- Статистику: сколько тем, подтем, файлов создано
- Предложи начать с оценки текущего уровня

---

## Learn Mode (автоматизированное обучение)

После создания системы доступен **Learn Mode** — управляемый автопилот:

### Как работает
1. Claude приветствует и предлагает продолжить → отвечаешь `да`/`давай`/`продолжим` или называешь тему (`учим [тема]`)
2. Каждая тема разбита на блоки: калибровка → теория → проверка → практика
3. После каждого блока Claude спрашивает «Дальше?» и ждёт подтверждения
4. Можешь вмешаться: `стоп`, `углубись`, `практика`, `пропусти`
5. Полный диалог сохраняется в `session.md` — можно продолжить в новой сессии
6. Все файловые операции происходят в фоне — ты видишь только обучение

### UX-принцип
Ученик видит **только обучение** — объяснения, вопросы, код, инсайты. Вся «бухгалтерия» (обновление progress, session, summary и т.д.) выполняется через фоновых агентов, невидимо.

---

## Как добавить новый трек

1. Скажи Claude: `добавь трек [название]` (например: `добавь трек golang`)
2. Claude создаст `tracks/[название]/` с roadmap, progress, dependency-graph и topics
3. Структура тем будет сгенерирована под выбранную технологию
4. Все команды (`учим`, `собес`, `прогресс` и т.д.) работают с указанием трека: `учим dotnet/linq` или `учим golang/goroutines`
