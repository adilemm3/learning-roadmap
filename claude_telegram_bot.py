#!/usr/bin/env python3
"""
Claude Code CLI — Telegram Bot (Interactive PTY)
===================================================
Управляет интерактивным Claude Code через Telegram.
Один долгоживущий процесс — все команды работают: /compact, /clear, quit.

Установка:
  pip3 install python-telegram-bot --break-system-packages

Запуск:
  python3 claude_telegram_bot.py

Переменные окружения (задай в .env):
  TELEGRAM_TOKEN   — токен бота от @BotFather
  ALLOWED_USER_ID  — числовой Telegram user ID
  CLAUDE_PATH      — путь к claude (по умолчанию: claude)
"""

import os
from pathlib import Path
import asyncio
import pty
import fcntl
import select
import re
import logging
import sys
import time
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from telegram.constants import ChatAction

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

TELEGRAM_TOKEN  = os.getenv("TELEGRAM_TOKEN", "")
ALLOWED_USER_ID = os.getenv("ALLOWED_USER_ID", "")
CLAUDE_PATH     = os.getenv("CLAUDE_PATH", "claude")
PROJECT_DIR     = str(Path(__file__).parent)

# Секунды тишины перед отправкой буфера в Telegram
OUTPUT_IDLE_SEC = 5.0

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)

# ─────────────────────────────────────────
#  Очистка terminal output
# ─────────────────────────────────────────
ANSI_RE = re.compile(
    r'\x1b'
    r'(?:'
    r'\[[0-9;?]*[a-zA-Z~]'
    r'|\][^\x07\x1b]*(?:\x07|\x1b\\)'
    r'|\([B0UK]'
    r'|[>=][0-9]*'
    r'|[78DEHM]'
    r')'
)
CONTROL_RE = re.compile(r'[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]')


def clean_output(text: str) -> str:
    text = ANSI_RE.sub('', text)
    text = CONTROL_RE.sub('', text)

    lines = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            lines.append('')
            continue
        # Пропускаем UI-мусор Claude TUI
        if any(s in stripped for s in [
            'bypass permissions',
            'shift+tab to cycle',
            'Checking for updates',
            '⏵⏵',
            'ClaudeCode',
            'Claude Code v',
        ]):
            continue
        # Пропускаем строки состоящие только из box-drawing символов
        if all(c in '╭╮╰╯│─┌┐└┘├┤┬┴┼═║╔╗╚╝╠╣╦╩╬▪▐▛▜▝▘█▌▀▄⧉⏵ ' for c in stripped):
            continue
        lines.append(stripped)

    text = '\n'.join(lines)
    text = re.sub(r'\n{3,}', '\n\n', text)
    return text.strip()


def split_text(text: str, max_len: int = 4000) -> list[str]:
    if len(text) <= max_len:
        return [text]
    chunks = []
    while text:
        chunks.append(text[:max_len])
        text = text[max_len:]
    return chunks


# ─────────────────────────────────────────
#  Интерактивный процесс Claude
# ─────────────────────────────────────────
class ClaudeProcess:

    def __init__(self):
        self.process: asyncio.subprocess.Process | None = None
        self.master_fd: int | None = None
        self._reader_task: asyncio.Task | None = None
        self._flusher_task: asyncio.Task | None = None
        self._buffer: str = ""
        self._last_data_time: float = 0
        self._chat_id: int | None = None
        self._bot = None

    @property
    def is_running(self) -> bool:
        return self.process is not None and self.process.returncode is None

    async def start(self, bot, chat_id: int) -> str:
        if self.is_running:
            return "Claude уже запущен. /kill для перезапуска."

        self._bot = bot
        self._chat_id = chat_id
        self._buffer = ""

        master_fd, slave_fd = pty.openpty()
        self.master_fd = master_fd

        # Устанавливаем размер терминала (широкий, чтобы не было переносов)
        import struct
        import termios
        winsize = struct.pack('HHHH', 50, 200, 0, 0)
        fcntl.ioctl(slave_fd, termios.TIOCSWINSZ, winsize)

        self.process = await asyncio.create_subprocess_exec(
            CLAUDE_PATH,
            stdin=slave_fd,
            stdout=slave_fd,
            stderr=slave_fd,
            cwd=PROJECT_DIR,
            env={**os.environ, "TERM": "dumb", "NO_COLOR": "1"},
        )
        os.close(slave_fd)

        self._reader_task = asyncio.create_task(self._read_loop())
        self._flusher_task = asyncio.create_task(self._flush_loop())

        log.info("Claude started pid=%s in %s", self.process.pid, PROJECT_DIR)
        return f"Claude запущен (pid={self.process.pid})"

    async def _read_loop(self):
        loop = asyncio.get_event_loop()
        while self.is_running:
            try:
                data = await loop.run_in_executor(None, self._read_chunk)
                if data:
                    self._buffer += data
                    self._last_data_time = time.monotonic()
            except OSError:
                break
            await asyncio.sleep(0.05)

        # Процесс завершился — отправить остаток буфера
        if self._buffer:
            await self._flush()
        if self._bot and self._chat_id:
            try:
                await self._bot.send_message(
                    chat_id=self._chat_id,
                    text="Claude процесс завершился.",
                )
            except Exception:
                pass

    def _read_chunk(self) -> str:
        try:
            ready, _, _ = select.select([self.master_fd], [], [], 0.5)
            if ready:
                raw = os.read(self.master_fd, 8192)
                if not raw:
                    return ""
                return raw.decode("utf-8", errors="replace")
            return ""
        except (OSError, ValueError):
            return ""

    async def _flush_loop(self):
        while self.is_running:
            await asyncio.sleep(1.0)
            if (
                self._buffer
                and self._last_data_time > 0
                and time.monotonic() - self._last_data_time >= OUTPUT_IDLE_SEC
            ):
                await self._flush()

    async def _flush(self):
        if not self._buffer:
            return
        text = clean_output(self._buffer)
        self._buffer = ""
        self._last_data_time = 0
        if not text or not self._bot or not self._chat_id:
            return
        for chunk in split_text(text):
            try:
                await self._bot.send_message(chat_id=self._chat_id, text=chunk)
            except Exception as e:
                log.error("Send error: %s", e)

    async def send(self, text: str) -> None:
        if not self.is_running or self.master_fd is None:
            return
        os.write(self.master_fd, (text + "\n").encode())

    async def stop(self) -> str:
        if not self.is_running:
            return "Claude не запущен."
        self.process.terminate()
        try:
            await asyncio.wait_for(self.process.wait(), timeout=10)
        except asyncio.TimeoutError:
            self.process.kill()
        await self._cleanup()
        return "Claude остановлен."

    async def kill(self) -> str:
        if not self.is_running:
            return "Claude не запущен."
        self.process.kill()
        await self._cleanup()
        return "Claude убит."

    async def _cleanup(self):
        for task in (self._reader_task, self._flusher_task):
            if task:
                task.cancel()
        if self.master_fd is not None:
            try:
                os.close(self.master_fd)
            except OSError:
                pass
            self.master_fd = None
        self.process = None
        self._buffer = ""


claude_proc = ClaudeProcess()


# ─────────────────────────────────────────
#  Проверка доступа
# ─────────────────────────────────────────
def is_allowed(update: Update) -> bool:
    uid = str(update.effective_user.id)
    if ALLOWED_USER_ID and uid != ALLOWED_USER_ID:
        log.warning("Access denied: user_id=%s", uid)
        return False
    return True


# ─────────────────────────────────────────
#  Telegram handlers
# ─────────────────────────────────────────
async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    await update.message.reply_text(
        "Claude Code — Telegram Remote\n\n"
        "Управление:\n"
        "/run — запустить Claude\n"
        "/quit — завершить (сохранит сессию)\n"
        "/kill — принудительно убить\n"
        "/compact — сжать контекст\n"
        "/clear — очистить контекст\n"
        "/status — статус процесса\n\n"
        "Обучение:\n"
        "/learn — продолжить обучение\n"
        "/next, /yes, /practice, /deep, /skip\n"
        "/save, /stop, /progress\n\n"
        "Обычные сообщения передаются в Claude."
    )


async def cmd_run(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    log.info("/run — запуск Claude")
    result = await claude_proc.start(ctx.bot, update.effective_chat.id)
    await update.message.reply_text(result)


async def cmd_quit(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    if not claude_proc.is_running:
        await update.message.reply_text("Claude не запущен.")
        return
    log.info("/quit — завершение Claude")
    await claude_proc.send("quit")
    await update.message.reply_text("Отправлено quit...")
    await asyncio.sleep(8)
    if claude_proc.is_running:
        await claude_proc.stop()


async def cmd_kill(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    log.info("/kill — принудительная остановка")
    result = await claude_proc.kill()
    await update.message.reply_text(result)


async def cmd_compact(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    if not claude_proc.is_running:
        await update.message.reply_text("Claude не запущен. /run")
        return
    log.info("/compact")
    await claude_proc.send("/compact")


async def cmd_clear(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    if not claude_proc.is_running:
        await update.message.reply_text("Claude не запущен. /run")
        return
    log.info("/clear")
    await claude_proc.send("/clear")


async def cmd_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    if claude_proc.is_running:
        await update.message.reply_text(
            f"Claude работает (pid={claude_proc.process.pid})\n{PROJECT_DIR}"
        )
    else:
        await update.message.reply_text("Claude не запущен. /run для запуска.")


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    await update.message.reply_text(
        "Управление Claude:\n"
        "  /run — запустить\n"
        "  /quit — сохранить и выйти\n"
        "  /kill — принудительно убить\n"
        "  /compact — сжать контекст\n"
        "  /clear — очистить контекст\n"
        "  /status — статус процесса\n\n"
        "Обучение (отправляются как текст):\n"
        "  /learn [тема] — учим / продолжить\n"
        "  /next — дальше\n"
        "  /yes — да\n"
        "  /practice — практика\n"
        "  /deep — углубись\n"
        "  /skip — пропусти\n"
        "  /save — сохрани\n"
        "  /stop — стоп\n"
        "  /progress — прогресс\n\n"
        "Обычные сообщения передаются как есть."
    )


# ─────────────────────────────────────────
#  Shortcut-команды проекта
# ─────────────────────────────────────────
SHORTCUT_COMMANDS = {
    "learn":    "давай",
    "next":     "дальше",
    "yes":      "да",
    "practice": "практика",
    "deep":     "углубись",
    "skip":     "пропусти",
    "save":     "сохрани",
    "stop":     "стоп",
    "progress": "прогресс",
}


async def cmd_shortcut(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    if not claude_proc.is_running:
        await update.message.reply_text("Claude не запущен. /run для запуска.")
        return

    command = update.message.text.split()[0].lstrip("/").split("@")[0]
    text = SHORTCUT_COMMANDS.get(command, command)
    args = update.message.text.split(maxsplit=1)
    if len(args) > 1:
        text = f"учим {args[1]}" if command == "learn" else f"{text} {args[1]}"

    log.info("/%s -> Claude: %s", command, text)
    await claude_proc.send(text)


async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    text = update.message.text.strip()
    if not text:
        return
    if not claude_proc.is_running:
        await update.message.reply_text("Claude не запущен. /run для запуска.")
        return
    log.info("-> Claude: %s", text[:80])
    await claude_proc.send(text)


# ─────────────────────────────────────────
#  Запуск
# ─────────────────────────────────────────
async def post_init(app: Application):
    await app.bot.set_my_commands([
        BotCommand("run",      "Запустить Claude"),
        BotCommand("learn",    "Учим [тема] — напр. /learn gc"),
        BotCommand("next",     "Следующий блок"),
        BotCommand("yes",      "Да / подтвердить"),
        BotCommand("practice", "Задачи"),
        BotCommand("deep",     "Углубиться"),
        BotCommand("skip",     "Пропустить блок"),
        BotCommand("save",     "Сохранить прогресс"),
        BotCommand("stop",     "Сохранить и завершить"),
        BotCommand("progress", "Показать прогресс"),
        BotCommand("compact",  "Сжать контекст"),
        BotCommand("clear",    "Очистить контекст"),
        BotCommand("quit",     "Завершить Claude"),
        BotCommand("kill",     "Убить процесс"),
        BotCommand("status",   "Статус"),
        BotCommand("help",     "Справка"),
    ])


def main():
    if not TELEGRAM_TOKEN:
        print("TELEGRAM_TOKEN not set. Create .env or export TELEGRAM_TOKEN.")
        sys.exit(1)
    if not ALLOWED_USER_ID:
        print("ALLOWED_USER_ID not set. Create .env or export ALLOWED_USER_ID.")
        sys.exit(1)

    log.info("Starting bot (user: %s, project: %s)", ALLOWED_USER_ID, PROJECT_DIR)

    app = (
        Application.builder()
        .token(TELEGRAM_TOKEN)
        .post_init(post_init)
        .build()
    )

    app.add_handler(CommandHandler("start",   cmd_start))
    app.add_handler(CommandHandler("run",     cmd_run))
    app.add_handler(CommandHandler("quit",    cmd_quit))
    app.add_handler(CommandHandler("kill",    cmd_kill))
    app.add_handler(CommandHandler("compact", cmd_compact))
    app.add_handler(CommandHandler("clear",   cmd_clear))
    app.add_handler(CommandHandler("status",  cmd_status))
    app.add_handler(CommandHandler("help",    cmd_help))
    for cmd in SHORTCUT_COMMANDS:
        app.add_handler(CommandHandler(cmd, cmd_shortcut))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    log.info("Bot started.")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
