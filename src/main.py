import asyncio
from telegram.ext import Application
from config.settings import BOT_TOKEN, WEBHOOK_URL
from src.bot.handlers import start, latest, confirmed, player, help_handler
from src.scrapers.twitter import stream_tier_one
from src.database.crud import init_db

def main():
    init_db()
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(start)
    app.add_handler(latest)
    app.add_handler(confirmed)
    app.add_handler(player)
    app.add_handler(help_handler)

    if WEBHOOK_URL:
        app.run_webhook(listen="0.0.0.0", port=8443, webhook_url=WEBHOOK_URL)
    else:
        asyncio.get_event_loop().create_task(stream_tier_one(app.bot))
        app.run_polling()

if __name__ == "__main__":
    main()
  
