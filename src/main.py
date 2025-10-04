#!/usr/bin/env python3
"""
Barça Transfer Bot – entry point
Production-ready:  no blocking calls inside running loop,
idempotent mongo wait, graceful shutdown.
"""
from __future__ import annotations

import asyncio
import signal
import sys
import time
from pathlib import Path

from pymongo import MongoClient
from telegram.ext import Application

# add project root to path (safe for Docker)
SRC = Path(__file__).parent
sys.path.insert(0, str(SRC.parent))

from config.settings import BOT_TOKEN, MONGODB_URI, WEBHOOK_URL  # noqa: E402
from database.crud import init_db                               # noqa: E402
from scrapers.twitter import stream_tier_one                    # noqa: E402
from bot.handlers import (                                      # noqa: E402
    start,
    latest,
    confirmed,
    player,
    help_handler,
)


# --------------------------------------------------------------------------- #
#  Helpers
# --------------------------------------------------------------------------- #
def _wait_mongo(uri: str, timeout: int = 30) -> None:
    """Synchronous retry until Mongo accepts a ping."""
    for _ in range(timeout):
        try:
            MongoClient(uri, serverSelectionTimeoutMS=2_000).admin.command("ping")
            return
        except Exception:  # noqa: S112
            time.sleep(1)
    sys.exit("Mongo unavailable")


# --------------------------------------------------------------------------- #
#  Graceful shutdown
# --------------------------------------------------------------------------- #
async def _shutdown(app: Application) -> None:  # noqa: D401
    """Stop bot & persistent streams."""
    await app.shutdown()
    await app.stop()


def _signal_handler(app: Application) -> None:
    def _inner(signum, frame) -> None:  # noqa: ARG001
        asyncio.create_task(_shutdown(app))
        sys.exit(0)

    signal.signal(signal.SIGINT, _inner)
    signal.signal(signal.SIGTERM, _inner)


# --------------------------------------------------------------------------- #
#  Main
# --------------------------------------------------------------------------- #
def main() -> None:
    _wait_mongo(MONGODB_URI)
    init_db()

    app = Application.builder().token(BOT_TOKEN).build()
    _signal_handler(app)

    #  Commands
    app.add_handler(start)
    app.add_handler(latest)
    app.add_handler(confirmed)
    app.add_handler(player)
    app.add_handler(help_handler)

    #  Mode selector
    if WEBHOOK_URL:
        app.run_webhook(
            listen="0.0.0.0",
            port=8443,
            url_path="webhook",
            webhook_url=WEBHOOK_URL,
        )
    else:
        asyncio.run(_polling(app))


# --------------------------------------------------------------------------- #
#  Polling helper (keeps loop clean)
# --------------------------------------------------------------------------- #
async def _polling(app: Application) -> None:
    await app.initialize()
    async with app:
        # start twitter background stream
        asyncio.create_task(stream_tier_one(app.bot))
        await app.start()
        await app.updater.start_polling()  # type: ignore[attr-defined]
        # run forever until signal
        await app.updater.idle()           # type: ignore[attr-defined]


# --------------------------------------------------------------------------- #
if __name__ == "__main__":
    main()
    
