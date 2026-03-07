#!/usr/bin/env python3
"""
Claude Code CLI — Telegram Bot
================================
Проксирует сообщения из Telegram в Claude CLI и обратно.

Установка:
  pip install python-telegram-bot

Запуск:
  python claude_telegram_bot.py

Переменные окружения (задай в .env или экспортируй):
  TELEGRAM_TOKEN   — токен бота от @BotFather
  ALLOWED_USER_ID  — числовой Telegram user ID
  CLAUDE_PATH      — путь к claude (по умолчанию: claude)
"""

import os
from pathlib import Path
import asyncio
import subprocess
import logging
import signal
import sys
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.constants import ParseMode, ChatAction

# ─────────────────────────────────────────
#  Загрузка .env
# ─────────────────────────────────────────
_env_path = Path(__file__).parent / ".env"
if _env_path.exists():
    for line in _env_path.read_text().splitlines():
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            key, _, value = line.partition("=")
            os.environ.setdefault(key.strip(), value.strip())

# ─────────────────────────────────────────
#  НАСТРОЙКИ
# ─────────────────────────────────────────
TELEGRAM_TOKEN  = os.getenv("TELEGRAM_TOKEN",  "")
ALLOWED_USER_ID = os.getenv("ALLOWED_USER_ID", "")
CLAUDE_PATH     = os.getenv("CLAUDE_PATH",     "claude")

# Таймаут ожидания ответа от Claude (секунды)
CLAUDE_TIMEOUT = 120

# ─────────────────────────────────────────
#  Логгирование
# ─────────────────────────────────────────
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
log = logging.getLogger(__name__)


# ─────────────────────────────────────────
#  Хранение сессии на пользователя
# ─────────────────────────────────────────
class ClaudeSession:
    """Одна Claude-сессия = один непрерывный диалог."""

    def __init__(self):
        self.history: list[dict] = []   # {"role": "user"|"assistant", "content": str}

    def reset(self):
        self.history = []

    def add(self, role: str, content: str):
        self.history.append({"role": role, "content": content})

    def build_prompt(self, user_msg: str) -> str:
        """Формирует текст, который передаётся в claude --print."""
        self.add("user", user_msg)
        parts = []
        for turn in self.history:
            prefix = "Human:" if turn["role"] == "user" else "Assistant:"
            parts.append(f"{prefix} {turn['content']}")
        parts.append("Assistant:")
        return "\n\n".join(parts)


sessions: dict[int, ClaudeSession] = {}

def get_session(user_id: int) -> ClaudeSession:
    if user_id not in sessions:
        sessions[user_id] = ClaudeSession()
    return sessions[user_id]


# ─────────────────────────────────────────
#  Проверка доступа
# ─────────────────────────────────────────
def is_allowed(update: Update) -> bool:
    uid = str(update.effective_user.id)
    allowed = ALLOWED_USER_ID.strip()
    if allowed and allowed != "ВСТАВЬ_СВОЙ_USER_ID" and uid != allowed:
        log.warning("Отказ в доступе: user_id=%s", uid)
        return False
    return True


# ─────────────────────────────────────────
#  Вызов Claude CLI
# ─────────────────────────────────────────
async def ask_claude(prompt: str) -> str:
    """Запускает `claude --print` и возвращает ответ."""
    try:
        proc = await asyncio.create_subprocess_exec(
            CLAUDE_PATH, "--print",
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        stdout, stderr = await asyncio.wait_for(
            proc.communicate(input=prompt.encode()),
            timeout=CLAUDE_TIMEOUT,
        )
        if proc.returncode != 0:
            err = stderr.decode().strip()
            log.error("Claude вернул ошибку: %s", err)
            return f"⚠️ Ошибка Claude:\n```\n{err}\n```"
        return stdout.decode().strip() or "_(пустой ответ)_"

    except asyncio.TimeoutError:
        return f"⏱ Claude не ответил за {CLAUDE_TIMEOUT} секунд. Попробуй ещё раз."
    except FileNotFoundError:
        return (
            "❌ `claude` не найден. Убедись, что Claude Code CLI установлен и "
            f"путь `{CLAUDE_PATH}` верный (или задай переменную CLAUDE_PATH)."
        )
    except Exception as exc:
        log.exception("Неожиданная ошибка при вызове Claude")
        return f"❌ Внутренняя ошибка: {exc}"


# ─────────────────────────────────────────
#  Обработчики команд
# ─────────────────────────────────────────
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        await update.message.reply_text("🚫 Нет доступа.")
        return
    await update.message.reply_text(
        "👋 *Привет! Я — мост между Telegram и Claude Code CLI.*\n\n"
        "Просто пиши сообщения — я передам их Claude на твоём Mac.\n\n"
        "📋 *Команды:*\n"
        "/reset — начать новый диалог\n"
        "/status — проверить соединение с Claude\n"
        "/help — справка",
        parse_mode=ParseMode.MARKDOWN,
    )

async def cmd_reset(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    get_session(update.effective_user.id).reset()
    await update.message.reply_text("🔄 Диалог сброшен. Начнём с чистого листа!")

async def cmd_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    await update.message.reply_text("🔍 Проверяю соединение с Claude...")
    result = await ask_claude("Ответь одним словом: работаешь?")
    await update.message.reply_text(f"✅ Claude отвечает:\n_{result}_", parse_mode=ParseMode.MARKDOWN)

async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    await update.message.reply_text(
        "📖 *Справка*\n\n"
        "• Просто пиши — сообщение уйдёт в Claude\n"
        "• История диалога сохраняется в рамках сессии\n"
        "• `/reset` — очистить историю и начать заново\n"
        "• `/status` — проверить, что Claude доступен\n\n"
        "🔒 Бот принимает сообщения только от тебя (ALLOWED\\_USER\\_ID).",
        parse_mode=ParseMode.MARKDOWN,
    )


# ─────────────────────────────────────────
#  Обработчик обычных сообщений
# ─────────────────────────────────────────
async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        await update.message.reply_text("🚫 Нет доступа.")
        return

    user_text = update.message.text.strip()
    if not user_text:
        return

    session = get_session(update.effective_user.id)

    # Показываем "печатает..."
    await ctx.bot.send_chat_action(
        chat_id=update.effective_chat.id,
        action=ChatAction.TYPING,
    )

    prompt = session.build_prompt(user_text)
    log.info("→ Claude [user=%s]: %s", update.effective_user.id, user_text[:80])

    response = await ask_claude(prompt)
    session.add("assistant", response)

    log.info("← Claude: %s", response[:80])

    # Telegram ограничивает 4096 символов — разбиваем при необходимости
    for chunk in split_text(response, 4000):
        await update.message.reply_text(chunk, parse_mode=ParseMode.MARKDOWN)


def split_text(text: str, max_len: int) -> list[str]:
    if len(text) <= max_len:
        return [text]
    chunks = []
    while text:
        chunks.append(text[:max_len])
        text = text[max_len:]
    return chunks


# ─────────────────────────────────────────
#  Запуск
# ─────────────────────────────────────────
async def post_init(app: Application):
    await app.bot.set_my_commands([
        BotCommand("start",  "Начать работу"),
        BotCommand("reset",  "Новый диалог"),
        BotCommand("status", "Проверить Claude"),
        BotCommand("help",   "Справка"),
    ])

def main():
    if not TELEGRAM_TOKEN:
        print("TELEGRAM_TOKEN not set. Create .env or export TELEGRAM_TOKEN.")
        sys.exit(1)
    if not ALLOWED_USER_ID:
        print("ALLOWED_USER_ID not set. Create .env or export ALLOWED_USER_ID.")
        sys.exit(1)

    log.info("🚀 Запуск бота... (allowed user: %s)", ALLOWED_USER_ID)

    app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start",  cmd_start))
    app.add_handler(CommandHandler("reset",  cmd_reset))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("help",   cmd_help))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    log.info("✅ Бот запущен. Ожидаю сообщения...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
