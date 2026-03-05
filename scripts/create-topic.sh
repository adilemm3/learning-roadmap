#!/usr/bin/env bash
set -euo pipefail

# Usage: ./scripts/create-topic.sh <section> <topic-dir> <topic-name> <level> [dependencies]
# Example: ./scripts/create-topic.sh "06-asp-net-core" "08-api-clients-http" "API Clients & HTTP" "Middle" "Dependency Injection, Middleware Pipeline"

SECTION="${1:?Usage: create-topic.sh <section> <topic-dir> <topic-name> <level> [dependencies]}"
TOPIC_DIR="${2:?Missing topic directory name}"
TOPIC_NAME="${3:?Missing topic display name}"
LEVEL="${4:?Missing level (Junior/Middle/Senior/Architect)}"
DEPS="${5:-нет зависимостей}"

BASE="tracks/dotnet/topics/${SECTION}/${TOPIC_DIR}"

if [ -d "$BASE" ]; then
  echo "ERROR: Directory $BASE already exists"
  exit 1
fi

mkdir -p "$BASE"

cat > "$BASE/summary.md" << EOF
# ${TOPIC_NAME}
> Уровень: ${LEVEL}
> Зависимости: ${DEPS}

## Ключевые концепции
<!-- bullet points с основными идеями -->

## Объяснение простыми словами
<!-- аналогия из жизни -->

## Примеры кода
\`\`\`csharp
// TODO: добавить примеры
\`\`\`

## Частые вопросы на собесе
<!-- Q&A формат -->

## Подводные камни и нюансы
<!-- на что обращать внимание -->

## Связь с другими темами
<!-- как эта тема связана с остальными -->
EOF

cat > "$BASE/learning-plan.md" << EOF
# ${TOPIC_NAME} — План изучения
> Статус: ⬜ не начата
> Блок: 0/N | Последняя сессия: —

## Калибровка
<!-- Заполняется при первом входе в тему -->
- Базовые концепции: ⬜
- Средний уровень: ⬜
- Продвинутый: ⬜
→ Начинаем с блока: —

## Блоки

<!-- Claude генерирует блоки при первом входе в тему на основе калибровки -->
EOF

cat > "$BASE/session.md" << EOF
# ${TOPIC_NAME} — Сессии

<!-- Полный диалог всех учебных сессий по этой теме -->
EOF

cat > "$BASE/cheatsheet.md" << EOF
# ${TOPIC_NAME} — Шпаргалка
> Время чтения: ~2 мин | Формат: для просмотра с телефона

## Краткая суть
<!-- 2-3 предложения -->

## Ключевые моменты
<!-- короткие bullet points -->

## Сравнительная таблица
<!-- если применимо -->

## Код в одну строку
\`\`\`csharp
// минимальные примеры
\`\`\`

## Запомни
<!-- мнемоники, правила -->
EOF

cat > "$BASE/interview-questions.md" << EOF
# ${TOPIC_NAME} — Вопросы для собеседования

## 🟢 Junior
1. <!-- TODO -->

## 🟡 Middle
1. <!-- TODO -->

## 🔴 Senior
1. <!-- TODO -->

## 🏛 Architect
1. <!-- TODO -->

---
<details><summary>Ответы</summary>

<!-- ответы на все вопросы -->

</details>
EOF

cat > "$BASE/practice.md" << EOF
# ${TOPIC_NAME} — Практика

## Мини-задачи

### 🟢 Easy: <!-- название -->
<!-- условие -->
<details><summary>Решение</summary>

\`\`\`csharp
// TODO
\`\`\`

</details>

### 🟡 Medium: <!-- название -->
<!-- условие -->
<details><summary>Решение</summary>

\`\`\`csharp
// TODO
\`\`\`

</details>

### 🔴 Hard: <!-- название -->
<!-- условие -->
<details><summary>Решение</summary>

\`\`\`csharp
// TODO
\`\`\`

</details>

## Код-ревью
Найди проблемы в этом коде:
\`\`\`csharp
// TODO: добавить код с проблемами
\`\`\`

## Рефакторинг
Улучши этот код:
\`\`\`csharp
// TODO: добавить код для рефакторинга
\`\`\`
EOF

cat > "$BASE/cases.md" << EOF
# ${TOPIC_NAME} — Реальные кейсы

## Кейс 1: <!-- название -->
**Контекст:** ...
**Проблема:** ...
**Решение:** ...
**Выводы:** ...

## Постмортем
**Что произошло:** ...
**Причина:** ...
**Как починили:** ...
**Как предотвратить:** ...

## Trade-off анализ
**Вопрос:** ...
**Вариант A:** ...
**Вариант B:** ...
**Рекомендация:** ...
EOF

cat > "$BASE/diagram.md" << EOF
# ${TOPIC_NAME} — Схемы и диаграммы

## Концептуальная схема
\`\`\`
<!-- ASCII-диаграмма -->
\`\`\`

## Sequence Diagram
\`\`\`mermaid
sequenceDiagram
    participant A
    participant B
    A->>B: TODO
\`\`\`

## Компонентная диаграмма
<!-- архитектурная схема -->
EOF

cat > "$BASE/resources.md" << EOF
# ${TOPIC_NAME} — Источники

## Документация
- [ ] [Microsoft Docs: ${TOPIC_NAME}](https://learn.microsoft.com)

## Книги
- [ ] <!-- TODO -->

## Статьи и блоги
- [ ] <!-- TODO -->

## Видео и доклады
- [ ] <!-- TODO -->

## Практика
- [ ] <!-- TODO -->
EOF

git add "$BASE"

echo "Created ${BASE}/ with 9 files and staged in git"
