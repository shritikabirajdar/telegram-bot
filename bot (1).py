import os
import logging
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)
import anthropic

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

TELEGRAM_TOKEN = os.environ["TELEGRAM_TOKEN"]
ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
SYSTEM_PROMPT = os.environ.get(
    "SYSTEM_PROMPT",
    "You are Shritika, a helpful and friendly AI assistant. Be concise, clear, and warm in your replies.",
)
MAX_HISTORY = int(os.environ.get("MAX_HISTORY", "10"))

client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

user_histories: dict[int, list[dict]] = {}


def get_history(user_id: int) -> list[dict]:
    return user_histories.get(user_id, [])


def add_to_history(user_id: int, role: str, content: str):
    history = user_histories.setdefault(user_id, [])
    history.append({"role": role, "content": content})
    if len(history) > MAX_HISTORY * 2:
        user_histories[user_id] = history[-(MAX_HISTORY * 2):]


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Hi! I'm Shritika, your personal AI assistant.\n\n"
        "Just send me a message and I'll be happy to help!\n\n"
        "Commands:\n"
        "/start — show this message\n"
        "/clear — clear your conversation history\n"
        "/help  — show help\n\n"
        "— shritika_bot"
    )


async def clear(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_histories.pop(user_id, None)
    await update.message.reply_text("Conversation history cleared. Let's start fresh!")


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "I'm Shritika — here to help with anything you need!\n\n"
        "Just send me a message and I'll reply.\n"
        "I remember recent messages so we can have a real conversation.\n\n"
        "Use /clear to reset the conversation.\n\n"
        "— shritika_bot"
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_text = update.message.text

    await context.bot.send_chat_action(
        chat_id=update.effective_chat.id, action="typing"
    )

    add_to_history(user_id, "user", user_text)
    messages = get_history(user_id)

    try:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            system=SYSTEM_PROMPT,
            messages=messages,
        )
        reply = response.content[0].text
        add_to_history(user_id, "assistant", reply)

        if len(reply) > 4096:
            for i in range(0, len(reply), 4096):
                await update.message.reply_text(reply[i : i + 4096])
        else:
            await update.message.reply_text(reply)

    except anthropic.APIError as e:
        logger.error("API error: %s", e)
        await update.message.reply_text(
            "Sorry, I couldn't get a response right now. Please try again."
        )
    except Exception as e:
        logger.error("Unexpected error: %s", e)
        await update.message.reply_text("An unexpected error occurred.")


def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("clear", clear))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    logger.info("shritika_bot is running...")
    app.run_polling()


if __name__ == "__main__":
    main()
