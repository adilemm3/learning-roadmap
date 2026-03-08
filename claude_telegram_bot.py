#!/usr/bin/env python3
"""
Claude Code CLI — Telegram Bot (Stream JSON)
===================================================
Управляет Claude Code через Telegram.
Каждое сообщение → claude -p --output-format stream-json --verbose.
Контекст сохраняется через --resume <session_id>.

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
import json
import re
import logging
import sys
from telegram import Update, BotCommand
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

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

logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.INFO,
)
logging.getLogger("httpx").setLevel(logging.WARNING)
log = logging.getLogger(__name__)


def md_to_telegram_html(text: str) -> str:
    """Markdown → Telegram HTML. Поддерживает: code blocks, inline code, bold, italic, tables."""
    lines = text.split('\n')
    result = []
    in_code_block = False
    table_rows = []

    for line in lines:
        # Code blocks: ```lang ... ```
        if line.strip().startswith('```'):
            if in_code_block:
                in_code_block = False
                result.append('</pre>')
            else:
                in_code_block = True
                result.append('<pre>')
            continue

        if in_code_block:
            result.append(_escape_html(line))
            continue

        # Tables: | col | col |
        if line.strip().startswith('|') and line.strip().endswith('|'):
            cells = [c.strip() for c in line.strip().strip('|').split('|')]
            if all(set(c) <= {'-', ':', ' '} for c in cells):
                continue
            row = ' | '.join(_inline_format(_escape_html(c)) for c in cells)
            table_rows.append(row)
            continue

        # Flush table
        if table_rows:
            result.append('<pre>' + '\n'.join(table_rows) + '</pre>')
            table_rows = []

        # Headers: ## Title → bold
        header_match = re.match(r'^(#{1,6})\s+(.+)$', line)
        if header_match:
            level = len(header_match.group(1))
            title = _inline_format(_escape_html(header_match.group(2)))
            if level <= 2:
                result.append(f'\n<b>{title}</b>\n')
            else:
                result.append(f'<b>{title}</b>')
            continue

        # Regular line
        escaped = _escape_html(line)
        formatted = _inline_format(escaped)
        result.append(formatted)

    if table_rows:
        result.append('<pre>' + '\n'.join(table_rows) + '</pre>')

    if in_code_block:
        result.append('</pre>')

    return '\n'.join(result)


def _escape_html(text: str) -> str:
    return text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')


def _inline_format(text: str) -> str:
    # inline code: `code`
    text = re.sub(r'`([^`]+)`', r'<code>\1</code>', text)
    # bold: **text** or __text__
    text = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', text)
    text = re.sub(r'__(.+?)__', r'<b>\1</b>', text)
    # italic: *text* or _text_ (но не внутри слов)
    text = re.sub(r'(?<!\w)\*([^*]+?)\*(?!\w)', r'<i>\1</i>', text)
    text = re.sub(r'(?<!\w)_([^_]+?)_(?!\w)', r'<i>\1</i>', text)
    # strikethrough: ~~text~~
    text = re.sub(r'~~(.+?)~~', r'<s>\1</s>', text)
    return text


def split_text(text: str, max_len: int = 4096) -> list[str]:
    if len(text) <= max_len:
        return [text]
    chunks = []
    while text:
        chunks.append(text[:max_len])
        text = text[max_len:]
    return chunks


# ─────────────────────────────────────────
#  Claude Runner (stream-json)
# ─────────────────────────────────────────
class ClaudeRunner:

    CONTEXT_LIMIT = 200_000
    SAVE_THRESHOLD = 0.70   # 70% — сохраняем прогресс
    RESET_THRESHOLD = 0.85  # 85% — принудительный reset

    def __init__(self):
        self.session_id: str | None = None
        self._process: asyncio.subprocess.Process | None = None
        self._busy = False
        self._last_input_tokens = 0
        self._save_pending = False

    @property
    def is_busy(self) -> bool:
        return self._busy

    async def ask(self, text: str, bot, chat_id: int) -> None:
        if self._busy:
            await bot.send_message(chat_id=chat_id, text="⏳ Claude ещё отвечает...")
            return

        self._busy = True
        try:
            usage_pct = self._last_input_tokens / self.CONTEXT_LIMIT if self.session_id else 0

            # 85%+ — принудительный reset (сохранять рискованно, может не влезть)
            if usage_pct >= self.RESET_THRESHOLD:
                log.warning("Force reset: %.0f%% context used", usage_pct * 100)
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"⚠️ Контекст {usage_pct:.0%} — reset без сохранения (не влезет). Прогресс в файлах.",
                )
                self._reset()

            # 70-85% — сохраняем и reset
            elif usage_pct >= self.SAVE_THRESHOLD:
                log.info("Auto-save + reset: %.0f%% context used", usage_pct * 100)
                await bot.send_message(
                    chat_id=chat_id,
                    text=f"🔄 Контекст {usage_pct:.0%} — сохраняю прогресс...",
                )
                await self._run("сохрани", bot, chat_id, silent=True)
                self._reset()

            await self._run(text, bot, chat_id)
        finally:
            self._busy = False

    async def _run(self, text: str, bot, chat_id: int, silent: bool = False) -> None:
        cmd = [
            CLAUDE_PATH, "-p", text,
            "--output-format", "stream-json",
            "--verbose",
        ]
        if self.session_id:
            cmd += ["--resume", self.session_id]

        log.info("-> Claude: %s", text[:80])

        try:
            self._process = await asyncio.create_subprocess_exec(
                *cmd,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                cwd=PROJECT_DIR,
            )
        except Exception as e:
            log.error("Failed to start claude: %s", e)
            await bot.send_message(chat_id=chat_id, text=f"Ошибка запуска: {e}")
            return

        thinking_msg = None
        if not silent:
            thinking_msg = await bot.send_message(chat_id=chat_id, text="⏳ Claude думает...")

        collected_text = ""
        tool_names = []

        async for raw_line in self._process.stdout:
            line = raw_line.decode("utf-8", errors="replace").strip()
            if not line:
                continue

            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                log.warning("Bad JSON: %s", line[:200])
                continue

            etype = event.get("type", "")
            subtype = event.get("subtype", "")

            # init → session_id
            if etype == "system" and subtype == "init":
                self.session_id = event.get("session_id", self.session_id)
                log.info("Session: %s", self.session_id)
                continue

            # assistant → текст ответа и/или tool_use
            if etype == "assistant":
                message = event.get("message", {})
                for block in message.get("content", []):
                    if block.get("type") == "text":
                        collected_text += block.get("text", "")
                    elif block.get("type") == "tool_use":
                        tool_name = block.get("name", "tool")
                        tool_names.append(tool_name)
                        log.info("Tool: %s", tool_name)

                        if thinking_msg:
                            try:
                                await thinking_msg.edit_text(f"🔧 {tool_name}...")
                            except Exception:
                                pass
                continue

            # result → завершение + usage
            if etype == "result":
                sid = event.get("session_id")
                if sid:
                    self.session_id = sid
                cost = event.get("total_cost_usd", 0)
                duration = event.get("duration_ms", 0)

                usage = event.get("usage", {})
                self._last_input_tokens = (
                    usage.get("input_tokens", 0)
                    + usage.get("cache_creation_input_tokens", 0)
                    + usage.get("cache_read_input_tokens", 0)
                )
                usage_pct = self._last_input_tokens / self.CONTEXT_LIMIT

                log.info(
                    "Done: %.1fs, $%.4f, tokens=%d (%.0f%%), session=%s",
                    duration / 1000, cost,
                    self._last_input_tokens, usage_pct * 100,
                    self.session_id,
                )
                continue

        stderr_data = await self._process.stderr.read()
        return_code = await self._process.wait()
        self._process = None

        if silent:
            log.info("Silent run done, text length=%d", len(collected_text))
            return

        if return_code != 0 and not collected_text:
            stderr_text = stderr_data.decode("utf-8", errors="replace").strip()
            error_msg = f"⚠️ Claude error (code {return_code})"
            if stderr_text:
                error_msg += f":\n{stderr_text[:500]}"
            log.error("Claude exited with code %d: %s", return_code, stderr_text[:200])
            if thinking_msg:
                try:
                    await thinking_msg.edit_text(error_msg)
                except Exception:
                    await bot.send_message(chat_id=chat_id, text=error_msg)
            else:
                await bot.send_message(chat_id=chat_id, text=error_msg)
            return

        if collected_text:
            if thinking_msg:
                try:
                    await thinking_msg.delete()
                except Exception:
                    pass

            html = md_to_telegram_html(collected_text.strip())
            for chunk in split_text(html):
                try:
                    await bot.send_message(
                        chat_id=chat_id, text=chunk, parse_mode="HTML",
                    )
                except Exception:
                    try:
                        await bot.send_message(chat_id=chat_id, text=chunk)
                    except Exception as e:
                        log.error("Send error: %s", e)
        else:
            if thinking_msg:
                try:
                    await thinking_msg.edit_text("⚠️ Claude вернул пустой ответ")
                except Exception:
                    pass

    def _reset(self):
        self.session_id = None
        self._last_input_tokens = 0
        log.info("Session reset")

    def clear_session(self):
        self._reset()
        log.info("Session cleared by user")

    async def cancel(self) -> str:
        if self._process and self._process.returncode is None:
            self._process.terminate()
            self._busy = False
            return "Запрос отменён."
        return "Нет активного запроса."


runner = ClaudeRunner()


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
        "Просто пиши — сообщения передаются в Claude.\n\n"
        "Управление:\n"
        "/clear — новый диалог\n"
        "/compact — сохранить + сбросить контекст\n"
        "/cancel — отменить текущий запрос\n"
        "/status — статус\n\n"
        "Обучение:\n"
        "/learn — продолжить обучение\n"
        "/next, /yes, /practice, /deep, /skip\n"
        "/save, /stop, /progress"
    )


async def cmd_clear(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    runner.clear_session()
    await update.message.reply_text("Контекст очищен. Следующее сообщение начнёт новый диалог.")


async def cmd_compact(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    if runner.is_busy:
        await update.message.reply_text("⏳ Claude занят, подожди.")
        return
    if not runner.session_id:
        await update.message.reply_text("Нечего сжимать — диалог ещё не начат.")
        return

    usage_pct = runner._last_input_tokens / runner.CONTEXT_LIMIT
    await update.message.reply_text(
        f"🔄 Контекст {usage_pct:.0%} — сохраняю прогресс и сбрасываю сессию..."
    )
    runner._busy = True
    try:
        await runner._run("сохрани", ctx.bot, update.effective_chat.id, silent=True)
        runner._reset()
        await update.message.reply_text("✅ Прогресс сохранён, сессия обновлена.")
    except Exception as e:
        log.error("Compact failed: %s", e)
        runner._reset()
        await update.message.reply_text(f"⚠️ Ошибка при сохранении, сессия сброшена: {e}")
    finally:
        runner._busy = False


async def cmd_cancel(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    result = await runner.cancel()
    await update.message.reply_text(result)


async def cmd_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    busy = "⏳ Обрабатывает запрос..." if runner.is_busy else "✅ Свободен"
    session = runner.session_id[:8] + "..." if runner.session_id else "новый диалог"
    await update.message.reply_text(f"{busy}\nСессия: {session}\n{PROJECT_DIR}")


async def cmd_help(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    await update.message.reply_text(
        "Управление:\n"
        "  /clear — новый диалог\n"
        "  /cancel — отменить запрос\n"
        "  /status — статус\n\n"
        "Обучение:\n"
        "  /learn [тема] — учим\n"
        "  /next — дальше\n"
        "  /yes — да\n"
        "  /practice — практика\n"
        "  /deep — углубись\n"
        "  /skip — пропусти\n"
        "  /save — сохрани\n"
        "  /stop — стоп\n"
        "  /progress — прогресс\n\n"
        "Обычные сообщения передаются в Claude."
    )


# ─────────────────────────────────────────
#  Shortcut-команды обучения
# ─────────────────────────────────────────
SHORTCUTS = {
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

    command = update.message.text.split()[0].lstrip("/").split("@")[0]
    text = SHORTCUTS.get(command, command)
    args = update.message.text.split(maxsplit=1)
    if len(args) > 1:
        text = f"учим {args[1]}" if command == "learn" else f"{text} {args[1]}"

    log.info("/%s -> %s", command, text)
    await runner.ask(text, ctx.bot, update.effective_chat.id)


async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    if not is_allowed(update):
        return
    text = update.message.text.strip()
    if not text:
        return
    log.info("Message: %s", text[:80])
    await runner.ask(text, ctx.bot, update.effective_chat.id)


# ─────────────────────────────────────────
#  Запуск
# ─────────────────────────────────────────
async def post_init(app: Application):
    await app.bot.set_my_commands([
        BotCommand("learn",    "Учим [тема]"),
        BotCommand("next",     "Следующий блок"),
        BotCommand("yes",      "Подтвердить"),
        BotCommand("practice", "Задачи"),
        BotCommand("deep",     "Углубиться"),
        BotCommand("skip",     "Пропустить"),
        BotCommand("save",     "Сохранить"),
        BotCommand("stop",     "Завершить"),
        BotCommand("progress", "Прогресс"),
        BotCommand("clear",    "Новый диалог"),
        BotCommand("compact",  "Сохранить + сбросить контекст"),
        BotCommand("cancel",   "Отменить запрос"),
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
    app.add_handler(CommandHandler("clear",   cmd_clear))
    app.add_handler(CommandHandler("compact", cmd_compact))
    app.add_handler(CommandHandler("cancel",  cmd_cancel))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("help",   cmd_help))
    for cmd in SHORTCUTS:
        app.add_handler(CommandHandler(cmd, cmd_shortcut))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    log.info("Bot started.")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()
