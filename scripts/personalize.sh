#!/usr/bin/env bash
# Персонализация после клонирования template репозитория.
# Запускать из корня репозитория: bash scripts/personalize.sh
set -euo pipefail

echo "=== Настройка Learning Roadmap под тебя ==="
echo ""

# Имя
read -r -p "Твоё имя (как Claude будет к тебе обращаться): " NAME
if [ -z "$NAME" ]; then
  echo "Имя не может быть пустым."
  exit 1
fi

# GitHub username
read -r -p "GitHub username (для README): " GITHUB_USER
GITHUB_USER="${GITHUB_USER:-your-username}"

echo ""
echo "Применяю настройки..."

# Заменить [YOUR_NAME] во всех ключевых файлах
for file in CLAUDE.md MEMORY.md learner-profile.md; do
  if [ -f "$file" ]; then
    sed -i '' "s/\[YOUR_NAME\]/${NAME}/g" "$file"
  fi
done

# Обновить поле Имя в learner-profile.md (на случай если уже было заменено выше)
if [ -f "learner-profile.md" ]; then
  sed -i '' "s/^Имя: .*/Имя: ${NAME}/" "learner-profile.md"
fi

# GitHub username в README
if [ -f "README.md" ] && [ -n "$GITHUB_USER" ]; then
  sed -i '' "s/\[GITHUB_USERNAME\]/${GITHUB_USER}/g" README.md
  sed -i '' "s|github.com/[^/]*/learning-roadmap|github.com/${GITHUB_USER}/learning-roadmap|g" README.md
fi

# Обновить MEMORY.md — активная тема пуста
cat > "MEMORY.md" << MEMEOF
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
- **ЛЮБЫЕ Write/Edit/Bash операции с файлами проекта — ТОЛЬКО через фонового агента** (\`Agent\` с \`run_in_background: true\`). Без исключений. В основном чате ученик видит только текстовый итог
- Startup Protocol — чтение файлов допускается в основном потоке (нужно для контекста)
- bypassPermissions включён в проектных settings.json — никаких системных промптов
- Коммиты только по команде пользователя (без автохука)

## Заметки
- Проект создан $(date +%Y-%m-%d)
- Структура: tracks/ с треками по технологиям
- .NET трек: 15 разделов, 85 подтем
- Скиллы: learn, save-session, create-topic, rebalance, assess, verify
MEMEOF

echo ""
echo "✓ Готово! Система настроена для ${NAME}."
echo ""
echo "Следующий шаг:"
echo "  cd $(pwd)"
echo "  claude"
echo ""
echo "Claude поприветствует тебя и предложит начать обучение."
