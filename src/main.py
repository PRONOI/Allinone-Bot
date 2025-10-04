import asyncio
import signal
import sys
from pymongo import MongoClient
from telegram.ext import Application
from config.settings import BOT_TOKEN, WEBHOOK_URL, MONGODB_URI
from src.bot.handlers import start, latest, confirmed, player, help_handler
from src.scrapers.twitter import stream_tier_one
from src.database.crud import init_db


def _wait_mongo(uri: str, timeout: int = 30) -> None:
    """Block until Mongo answers or timeout."""
    for _ in range(timeout):
        try:
            MongoClient(uri).admin.command("ping")
            return
        except Exception:
            pass
        asyncio.get_event_loop().run_until_complete(asyncio.sleep(1))
    sys.exit("Mongo unavailable")


def _sig_handler(signum, frame) -> None:
    """Graceful shutdown on SIGINT/SIGTERM."""
    asyncio.create_task(app.shutdown())
    sys.exit(0)


def main() -> None:
    _wait_mongo(MONGODB_URI)
    init_db()

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(start)
    app.add_handler(latest)
    app.add_handler(confirmed)
    app.add_handler(player)
    app.add_handler(help_handler)

    signal.signal(signal.SIGINT, _sig_handler)
    signal.signal(signal.SIGTERM, _sig_handler)

    if WEBHOOK_URL:
        app.run_webhook(listen="0.0.0.0", port=8443, webhook_url=WEBHOOK_URL)
    else:
        asyncio.get_event_loop().create_task(stream_tier_one(app.bot))
        app.run_polling()


if __name__ == "__main__":
    main()
    
