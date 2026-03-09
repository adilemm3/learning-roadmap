# Claude Code через Telegram-бот (macOS)
> Управляй обучением с телефона через Telegram — без SSH и терминала

**Схема:** Телефон (Telegram) → Бот (`claude_telegram_bot.py`) → Claude CLI → Learning Roadmap

---

## Что это и зачем

Альтернатива Termius+SSH. Бот запускается на Mac, принимает сообщения из Telegram и передаёт их в Claude Code. Ответы возвращаются обратно в чат. Преимущество: не нужно держать SSH-соединение открытым — бот работает в фоне, сессия сохраняется между сообщениями.

---

## Что понадобится

| Что | Где взять |
|-----|-----------|
| Python 3.8+ | уже есть на macOS или `brew install python` |
| `python-telegram-bot` | `pip install python-telegram-bot` |
| Telegram-аккаунт | telegram.org |
| Claude CLI | уже настроен |

---

## Настройка (один раз)

### 1. Создать бота в Telegram

1. Открой Telegram → найди **@BotFather**
2. Отправь `/newbot`
3. Введи имя бота (например: `My Claude Bot`)
4. Введи username (должен заканчиваться на `bot`, например: `my_claude_bot`)
5. BotFather отправит токен вида `1234567890:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`

Сохрани токен — это `TELEGRAM_TOKEN`.

### 2. Узнать свой Telegram user ID

1. Найди в Telegram **@userinfobot**
2. Отправь `/start`
3. Бот ответит твоим числовым ID вида `123456789`

Это `ALLOWED_USER_ID` — только ты сможешь обращаться к боту.

### 3. Создать файл `.env`

В папке проекта `learning-roadmap/` создай файл `.env`:

```bash
cd ~/Documents/myProjects/learning-roadmap
```

```env
TELEGRAM_TOKEN=1234567890:AAFxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
ALLOWED_USER_ID=123456789
CLAUDE_PATH=claude
```

> `CLAUDE_PATH` — путь к Claude CLI. Если `claude` не в PATH, укажи полный путь: `/usr/local/bin/claude`

### 4. Установить зависимость

```bash
pip install python-telegram-bot
```

### 5. Запустить бота

```bash
cd ~/Documents/myProjects/learning-roadmap
python claude_telegram_bot.py
```

Открой Telegram → найди своего бота → отправь `/start`. Бот должен ответить.

---

## Запуск в фоне

### Вариант 1 — nohup (просто)

```bash
cd ~/Documents/myProjects/learning-roadmap
nohup python claude_telegram_bot.py > bot.log 2>&1 &
echo $! > bot.pid
```

Проверить что работает:
```bash
tail -f bot.log
```

Остановить:
```bash
kill $(cat bot.pid)
```

### Вариант 2 — launchd (автозапуск при старте Mac)

Создай файл `~/Library/LaunchAgents/com.claude.telegrambot.plist`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN"
  "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>com.claude.telegrambot</string>
    <key>ProgramArguments</key>
    <array>
        <string>/usr/bin/python3</string>
        <string>/Users/YOUR_USERNAME/Documents/myProjects/learning-roadmap/claude_telegram_bot.py</string>
    </array>
    <key>WorkingDirectory</key>
    <string>/Users/YOUR_USERNAME/Documents/myProjects/learning-roadmap</string>
    <key>RunAtLoad</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/tmp/claude-bot.log</string>
    <key>StandardErrorPath</key>
    <string>/tmp/claude-bot-error.log</string>
    <key>KeepAlive</key>
    <true/>
</dict>
</plist>
```

Замени `YOUR_USERNAME` на свой логин (`whoami`).

Загрузить:
```bash
launchctl load ~/Library/LaunchAgents/com.claude.telegrambot.plist
```

Остановить/перезапустить:
```bash
launchctl unload ~/Library/LaunchAgents/com.claude.telegrambot.plist
launchctl load ~/Library/LaunchAgents/com.claude.telegrambot.plist
```

---

## Ежедневное использование

Открой Telegram → свой бот → пиши как обычно. Для стандартных действий есть команды:

| Команда | Что делает |
|---------|-----------|
| `/learn [тема]` | Начать изучение темы |
| `/next` | Перейти к следующему блоку |
| `/yes` | Подтвердить / ответить «да» |
| `/practice` | Перейти к практике |
| `/deep` | Углубиться в тему |
| `/skip` | Пропустить блок |
| `/save` | Сохранить прогресс, продолжить |
| `/stop` | Сохранить и завершить сессию |
| `/progress` | Показать прогресс |
| `/cancel` | Отменить текущий запрос |
| `/status` | Статус бота (занят / свободен, ID сессии) |
| `/clear` | Новый диалог (сброс контекста) |
| `/compact` | Сохранить прогресс + сбросить контекст |
| `/help` | Справка по командам |

---

## Справочник: /clear vs /compact

| | `/clear` | `/compact` |
|--|----------|------------|
| **Что делает** | Сбрасывает контекст без сохранения | Сначала сохраняет прогресс, затем сбрасывает контекст |
| **Когда использовать** | Начать разговор заново, сессия не нужна | Контекст заполнился, хочешь продолжить с чистого листа |
| **Прогресс сохранится?** | Нет | Да |

Бот автоматически предупреждает о заполнении контекста:
- **70%+** — автосохранение прогресса
- **85%+** — автоматический reset (как `/compact`)
