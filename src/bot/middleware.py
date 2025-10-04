from telegram.ext import MessageHandler, filters
from config.settings import CHANNEL_ID, OWNER_ID

async def introduce_bot(update, _):
    await update.message.reply_text(
        "👋 Thanks for starting me!\n"
        f"Join our channel {CHANNEL_ID} for instant alerts.\n"
        f"Questions? DM {OWNER_ID}"
    )

auto_introduce = MessageHandler(filters.ChatType.PRIVATE & ~filters.COMMAND, introduce_bot)
