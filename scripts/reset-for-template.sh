#!/usr/bin/env bash
# Сбрасывает личные данные для создания template ветки.
# Запускать из корня репозитория: bash scripts/reset-for-template.sh
set -euo pipefail

TRACK="dotnet"
TOPICS_DIR="tracks/${TRACK}/topics"
TOPIC_TEMPLATES="templates/topic"
SECTION_TEMPLATES="templates/section"

echo "Сброс личных данных для template..."

# ── 1. Все 11 файлов каждой подтемы ────────────────────────────────────────
# Для каждой директории подтемы: читаем название из summary.md, сбрасываем все файлы
find "$TOPICS_DIR" -mindepth 2 -maxdepth 2 -type d | while read -r topic_dir; do
  summary="$topic_dir/summary.md"
  [ -f "$summary" ] || continue

  # Извлечь название темы из первой строки summary.md: "# Type System" → "Type System"
  topic_name=$(head -1 "$summary" | sed 's/^# //')
  # Извлечь уровень и зависимости из строк 2-3
  level=$(sed -n '2p' "$summary" | sed 's/^> Уровень: //')
  deps=$(sed -n '3p' "$summary" | sed 's/^> Зависимости: //')

  # Сбросить каждый файл шаблоном из templates/topic/
  for tmpl in "$TOPIC_TEMPLATES"/*.md; do
    filename=$(basename "$tmpl")
    target="$topic_dir/$filename"
    content=$(cat "$tmpl")
    # Заменить плейсхолдеры
    content="${content//\{\{TOPIC_NAME\}\}/$topic_name}"
    content="${content//\{\{LEVEL\}\}/$level}"
    content="${content//\{\{DEPENDENCIES\}\}/$deps}"
    printf '%s\n' "$content" > "$target"
  done
done

# ── 2. Section-level progress.md ────────────────────────────────────────────
find "$TOPICS_DIR" -mindepth 1 -maxdepth 1 -type d | while read -r section_dir; do
  prog="$section_dir/progress.md"
  [ -f "$prog" ] || continue

  # Извлечь название раздела из первой строки
  section_name=$(head -1 "$prog" | sed 's/^# //' | sed 's/ — Прогресс.*//')

  # Сбросить статусы: оставить строки с подтемами, обнулить данные
  python3 - "$prog" "$section_name" << 'PYEOF'
import sys, re
path, section_name = sys.argv[1], sys.argv[2]
with open(path) as f:
    lines = f.readlines()

result = []
for line in lines:
    # Строка таблицы с данными (содержит |): сбросить статус, уверенность, дату
    if re.match(r'^\|\s*\d+\s*\|', line):
        parts = line.split('|')
        if len(parts) >= 6:
            parts[3] = ' ⬜ '         # статус
            parts[4] = ' — '           # уверенность
            parts[5] = ' — '           # дата
            line = '|'.join(parts)
    result.append(line)

with open(path, 'w') as f:
    f.writelines(result)
PYEOF
done

# ── 3. Track-level progress.md ──────────────────────────────────────────────
python3 - << 'PYEOF'
import re
path = "tracks/dotnet/progress.md"
with open(path) as f:
    content = f.read()
content = re.sub(r'\| (🟡 в процессе|✅ завершена)', '| ⬜ не начата', content)
content = re.sub(r'\| \d (\|.*?Последняя сессия)', r'| 0 \1', content)  # уверенность
content = re.sub(r'(?<=\| 0 \| )\d{4}-\d{2}-\d{2}', '—', content)
content = re.sub(r'(\| (?:🟢 Junior|🟡 Middle|🔴 Senior|🏛 Architect) \| \d+ \| )\d+( \| )\d+%', r'\g<1>0\g<2>0%', content)
content = re.sub(r'(\| \*\*Итого\*\* \| \*\*\d+\*\* \| \*\*)\d+(\*\* \| )\d+%', r'\g<1>0\g<2>0%', content)
with open(path, 'w') as f:
    f.write(content)
PYEOF

# ── 4. Трековые файлы ───────────────────────────────────────────────────────
cat > "tracks/${TRACK}/weak-spots.md" << 'EOF'
# Слабые места и пробелы

## Активные
<!-- формат: - [ ] [Тема] описание пробела (дата выявления) -->

## Закрытые
<!-- формат: - [x] [Тема] описание (закрыто: дата) -->
EOF

cat > "tracks/${TRACK}/repetition-log.md" << 'EOF'
# Повторения — .NET/C#

> Лог spaced repetition сессий. Claude генерирует уникальные вопросы по завершённым темам при startup.
> Интервалы: 7 → 14 → 30 дней. При ❌ — сброс интервала до 7 дней.

<!-- формат:
## YYYY-MM-DD — [Тема]
**Вопросы:** ...
**Результаты:** ✅/❌
**Следующее повторение:** через N дней (YYYY-MM-DD)
-->
EOF

# glossary — только заголовок таблицы
python3 - << 'PYEOF'
with open("tracks/dotnet/glossary.md") as f:
    lines = f.readlines()
# Оставить заголовок и строку-разделитель таблицы
header = [l for l in lines[:6] if l.strip()][:4]
with open("tracks/dotnet/glossary.md", 'w') as f:
    f.writelines(header)
    f.write('\n')
PYEOF

# ── 5. Корневые файлы ────────────────────────────────────────────────────────
cat > "MEMORY.md" << 'EOF'
# Learning Roadmap — Memory

> Персистентная память Claude между сессиями. Обновляется автоматически.

## Активный трек
dotnet

## Активная тема
Тема: —
Блок: —
Путь: —

## Стиль ученика (кэш из learner-profile.md)
- Порядок: аналогия → теория → код
- Темп: не определён
- Глубина: не определена

## UX-правила
- **ЛЮБЫЕ Write/Edit/Bash операции с файлами проекта — ТОЛЬКО через фонового агента** (`Agent` с `run_in_background: true`). Без исключений. В основном чате ученик видит только текстовый итог
- Startup Protocol — чтение файлов допускается в основном потоке (нужно для контекста)
- bypassPermissions включён в проектных settings.json — никаких системных промптов
- Коммиты только по команде пользователя (без автохука)

## Заметки
- Структура: tracks/ с треками по технологиям
- .NET трек: 15 разделов, 85 подтем
- Скиллы: learn, save-session, create-topic, rebalance, assess, verify
EOF

cat > "learner-profile.md" << 'EOF'
# Профиль ученика

## Основное
Имя: [YOUR_NAME]
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
EOF

cat > "improvements.md" << 'EOF'
# Идеи по улучшению системы обучения

> Этот файл заполняется Claude автоматически в процессе учебных сессий.
> Идеи добавляются через субагента в фоне, не прерывая обучение.

## Новые
<!-- Формат: - YYYY-MM-DD HH:MM | [контекст] описание идеи -->

## Применённые
<!-- Формат: - YYYY-MM-DD | описание (применено: YYYY-MM-DD) -->

## Отклонённые
<!-- Формат: - YYYY-MM-DD | описание (причина отклонения) -->
EOF

# ── 6. Имена в CLAUDE.md и скиллах ──────────────────────────────────────────
# CLAUDE.md
sed -i '' \
  -e 's/Адиль/[YOUR_NAME]/g' \
  -e 's/adilemm3/[GITHUB_USERNAME]/g' \
  CLAUDE.md

# SKILL.md файлы — заменить имя в приветствиях и примерах диалогов
find .claude/skills -name "*.md" | while read -r skill; do
  sed -i '' 's/Адиль/[YOUR_NAME]/g' "$skill"
done

echo ""
echo "✓ Сброс завершён. Файлы затронуты:"
echo "  - Все 11 файлов каждой подтемы → шаблоны"
echo "  - Section progress.md → ⬜"
echo "  - Track progress.md → ⬜"
echo "  - weak-spots, repetition-log, glossary → пустые"
echo "  - MEMORY.md, learner-profile.md, improvements.md → чистые"
echo "  - CLAUDE.md + skills/*.md → [YOUR_NAME]"
echo ""
echo "Следующий шаг:"
echo "  git add -A && git commit -m 'chore: template — чистое состояние'"
echo "  git push origin template"
