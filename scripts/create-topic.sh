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
> Краткая и ёмкая выжимка для быстрого повторения

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

> Ответы → \`interview-answers.md\`

## Junior
1. <!-- TODO -->

## Middle
1. <!-- TODO -->

## Senior
1. <!-- TODO -->

## Architect
1. <!-- TODO -->
EOF

cat > "$BASE/interview-answers.md" << EOF
# ${TOPIC_NAME} — Ответы на вопросы

## Junior

**1. <!-- вопрос -->**
<details><summary>Ответ</summary>

<!-- ответ -->

</details>

## Middle

**1. <!-- вопрос -->**
<details><summary>Ответ</summary>

<!-- ответ -->

</details>

## Senior

**1. <!-- вопрос -->**
<details><summary>Ответ</summary>

<!-- ответ -->

</details>

## Architect

**1. <!-- вопрос -->**
<details><summary>Ответ</summary>

<!-- ответ -->

</details>
EOF

cat > "$BASE/practice.md" << EOF
# ${TOPIC_NAME} — Практика

> Подсказки и решения → \`practice-solutions.md\`

<!-- 5 задач: 2 Easy + 2 Medium + 1 Hard -->
<!-- Типы: код-ревью / реализация / рефакторинг / дебаг / архитектура -->

## Задача 1: <!-- название -->
> Сложность: Easy | Тип: <!-- тип -->

<!-- условие -->

## Задача 2: <!-- название -->
> Сложность: Easy | Тип: <!-- тип -->

<!-- условие -->

## Задача 3: <!-- название -->
> Сложность: Medium | Тип: <!-- тип -->

<!-- условие -->

## Задача 4: <!-- название -->
> Сложность: Medium | Тип: <!-- тип -->

<!-- условие -->

## Задача 5: <!-- название -->
> Сложность: Hard | Тип: <!-- тип -->

<!-- условие -->
EOF

cat > "$BASE/practice-solutions.md" << 'SOLUTIONS_EOF'
# TOPIC_PLACEHOLDER — Подсказки и решения

<!-- Каждое решение с кодом должно содержать:
     1. Общую концепцию — какую проблему решаем и какой подход
     2. Комментарии к каждой значимой строке — что делает и почему
     3. Пояснения после кода — ключевые решения и альтернативы -->

## Задача 1: <!-- название -->

<details><summary>Подсказка</summary>

<!-- наводящая мысль, не ответ -->

</details>

<details><summary>Решение</summary>

<!-- концепция -->

```csharp
// TODO — код с пояснениями каждой строки
```

<!-- ключевые решения и альтернативы -->

</details>

## Задача 2: <!-- название -->

<details><summary>Подсказка</summary>

<!-- наводящая мысль, не ответ -->

</details>

<details><summary>Решение</summary>

<!-- концепция -->

```csharp
// TODO — код с пояснениями каждой строки
```

<!-- ключевые решения и альтернативы -->

</details>

## Задача 3: <!-- название -->

<details><summary>Подсказка</summary>

<!-- наводящая мысль, не ответ -->

</details>

<details><summary>Решение</summary>

<!-- концепция -->

```csharp
// TODO — код с пояснениями каждой строки
```

<!-- ключевые решения и альтернативы -->

</details>

## Задача 4: <!-- название -->

<details><summary>Подсказка</summary>

<!-- наводящая мысль, не ответ -->

</details>

<details><summary>Решение</summary>

<!-- концепция -->

```csharp
// TODO — код с пояснениями каждой строки
```

<!-- ключевые решения и альтернативы -->

</details>

## Задача 5: <!-- название -->

<details><summary>Подсказка</summary>

<!-- наводящая мысль, не ответ -->

</details>

<details><summary>Решение</summary>

<!-- концепция -->

```csharp
// TODO — код с пояснениями каждой строки
```

<!-- ключевые решения и альтернативы -->

</details>
SOLUTIONS_EOF
sed -i '' "s/TOPIC_PLACEHOLDER/${TOPIC_NAME}/g" "$BASE/practice-solutions.md"

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

echo "Created ${BASE}/ with 11 files and staged in git"
