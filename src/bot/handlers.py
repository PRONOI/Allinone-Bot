from telegram.ext import CommandHandler
from src.database.crud import get_latest_news, get_confirmed_news, get_player_news
from src.utils.text_tools import emoji_tag

async def start(update, _):
    await update.message.reply_text(
        "🔵🔴 Hola, Culér! I deliver only Tier-1 Barça transfer news.\n"
        "Use /help to see commands."
    )

async def latest(update, _):
    for item in get_latest_news(5):
        await update.message.reply_text(emoji_tag(item))

async def confirmed(update, _):
    for item in get_confirmed_news(5):
        await update.message.reply_text(emoji_tag(item))

async def player(update, context):
    name = " ".join(context.args)
    if not name:
        await update.message.reply_text("Usage: /players <name>")
        return
    for item in get_player_news(name):
        await update.message.reply_text(emoji_tag(item))

async def help_handler(update, _):
    txt = (
        "/start - Welcome\n"
        "/latest - Last 5 stories\n"
        "/confirmed - Only done deals\n"
        "/players <name> - News about player"
    )
    await update.message.reply_text(txt)

start = CommandHandler("start", start)
latest = CommandHandler("latest", latest)
confirmed = CommandHandler("confirmed", confirmed)
player = CommandHandler("players", player)
help_handler = CommandHandler("help", help_handler)
