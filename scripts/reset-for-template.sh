#!/usr/bin/env bash
# Сбрасывает личные данные для создания template ветки.
# Запускать из корня репозитория: bash scripts/reset-for-template.sh
set -euo pipefail

TRACK="dotnet"
TOPICS_DIR="tracks/${TRACK}/topics"

echo "Сброс личных данных для template..."

# ── session.md ─────────────────────────────────────────────────────────────
find "$TOPICS_DIR" -name "session.md" | while read -r f; do
  title=$(head -1 "$f")
  printf '%s\n\n<!-- Полный диалог всех учебных сессий по этой теме -->\n' "$title" > "$f"
done

# ── learning-plan.md ────────────────────────────────────────────────────────
find "$TOPICS_DIR" -name "learning-plan.md" | while read -r f; do
  title=$(head -1 "$f")
  cat > "$f" << 'TMPL'
TITLE_PLACEHOLDER
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
TMPL
  sed -i '' "s|TITLE_PLACEHOLDER|${title}|" "$f"
done

# ── summary.md ──────────────────────────────────────────────────────────────
find "$TOPICS_DIR" -name "summary.md" | while read -r f; do
  header=$(head -3 "$f")
  cat > "$f" << 'TMPL'
HEADER_PLACEHOLDER

## Ключевые концепции
<!-- bullet points с основными идеями -->

## Объяснение простыми словами
<!-- аналогия из жизни -->

## Примеры кода
```csharp
// TODO: добавить примеры
```

## Частые вопросы на собесе
<!-- Q&A формат -->

## Подводные камни и нюансы
<!-- на что обращать внимание -->

## Связь с другими темами
<!-- как эта тема связана с остальными -->
TMPL
  # Заменяем плейсхолдер на реальный заголовок (три строки)
  python3 -c "
import sys
content = open('$f').read()
content = content.replace('HEADER_PLACEHOLDER', '''${header}''', 1)
open('$f', 'w').write(content)
"
done

# ── Файлы трека ─────────────────────────────────────────────────────────────
# weak-spots.md
cat > "tracks/${TRACK}/weak-spots.md" << 'EOF'
# Слабые места и пробелы

## Активные
<!-- формат: - [ ] [Тема] описание пробела (дата выявления) -->

## Закрытые
<!-- формат: - [x] [Тема] описание (закрыто: дата) -->
EOF

# repetition-log.md
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

# glossary.md — оставить только заголовок таблицы
head -4 "tracks/${TRACK}/glossary.md" > /tmp/glossary_header.md
mv /tmp/glossary_header.md "tracks/${TRACK}/glossary.md"

# progress.md — сбросить статусы и уверенность
python3 - << 'PYEOF'
import re
with open("tracks/dotnet/progress.md") as f:
    content = f.read()
# Заменить статусы в таблице: 🟡/✅ → ⬜, уверенность → 0, дату → —
content = re.sub(r'\| (🟡 в процессе|✅ завершена)', '| ⬜ не начата', content)
content = re.sub(r'\| (\d) \|', '| 0 |', content)
content = re.sub(r'\| (\d{4}-\d{2}-\d{2}) \|', '| — |', content)
# Сводная таблица
content = re.sub(r'(\| 🟢 Junior \| \d+ \| )\d+( \| )\d+(%)', r'\g<1>0\g<2>0\g<3>', content)
content = re.sub(r'(\| 🟡 Middle \| \d+ \| )\d+( \| )\d+(%)', r'\g<1>0\g<2>0\g<3>', content)
content = re.sub(r'(\| 🔴 Senior \| \d+ \| )\d+( \| )\d+(%)', r'\g<1>0\g<2>0\g<3>', content)
content = re.sub(r'(\| 🏛 Architect \| \d+ \| )\d+( \| )\d+(%)', r'\g<1>0\g<2>0\g<3>', content)
content = re.sub(r'(\| \*\*Итого\*\* \| \*\*\d+\*\* \| \*\*)\d+(\*\* \| )\d+(%)', r'\g<1>0\g<2>0\g<3>', content)
with open("tracks/dotnet/progress.md", "w") as f:
    f.write(content)
PYEOF

# ── Корневые файлы ──────────────────────────────────────────────────────────
# MEMORY.md
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

# learner-profile.md
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

# improvements.md
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

# Заменить "Адиль" → [YOUR_NAME] в CLAUDE.md
sed -i '' \
  -e 's/Адиль/[YOUR_NAME]/g' \
  -e 's/adilemm3/[GITHUB_USERNAME]/g' \
  CLAUDE.md

echo ""
echo "✓ Сброс завершён. Теперь:"
echo "  git checkout -b template"
echo "  git add -A && git commit -m 'chore: template — чистое состояние для новых пользователей'"
echo "  git push -u origin template"
echo ""
echo "  Затем на GitHub: Settings → репозиторий → ✓ Template repository"
