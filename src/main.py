#!/usr/bin/env python3
"""Barça Transfer Bot – entry point"""
from __future__ import annotations

import asyncio
import signal
import sys
import time
from pathlib import Path

from pymongo import MongoClient
from telegram.ext import Application

SRC = Path(__file__).parent
sys.path.insert(0, str(SRC.parent))

from config.settings import BOT_TOKEN, MONGODB_URI, WEBHOOK_URL  # noqa: E402
from database.crud import init_db                               # noqa: E402
from scrapers.twitter import stream_tier_one                    # noqa: E402
from bot.handlers import start, latest, confirmed, player, help_handler  # noqa: E402

# ---------- 1-A.  NEW:  startup ping ----------
import os, requests   # add these two imports

def _startup_ping():
    token = os.environ.get("BOT_TOKEN")
    owner = os.environ.get("OWNER_ID")
    if not token or not owner:
        print("❌  BOT_TOKEN or OWNER_ID missing")
        return
    time.sleep(5)   # let Render flush logs
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.post(url, json={"chat_id": owner, "text": "Bot starting…"})
    print("Startup ping:", r.status_code, r.text)

# ---------- 1.  rate-limit  ----------
SEND_SEM = asyncio.Semaphore(25)   # max 25 concurrent sends

# ---------- 2.  health stub  ----------
if WEBHOOK_URL:
    from aiohttp import web
    async def health(_: web.Request) -> web.Response:
        return web.Response(text="ok")

# ---------- helpers ----------
def _wait_mongo(uri: str, timeout: int = 30) -> None:
    for _ in range(timeout):
        try:
            MongoClient(uri, serverSelectionTimeoutMS=2_000).admin.command("ping")
            return
        except Exception:  # noqa: S112
            time.sleep(1)
    sys.exit("Mongo unavailable")

def _signal_handler(app: Application) -> None:
    def _inner(signum, frame) -> None:  # noqa: ARG001
        asyncio.create_task(app.shutdown())
        sys.exit(0)
    signal.signal(signal.SIGINT, _inner)
    signal.signal(signal.SIGTERM, _inner)

# ---------- main ----------
def main() -> None:
    _startup_ping()      # ← call it first
    _wait_mongo(MONGODB_URI)
    init_db()

    app = Application.builder().token(BOT_TOKEN).build()
    _signal_handler(app)

    # commands
    app.add_handler(start)
    app.add_handler(latest)
    app.add_handler(confirmed)
    app.add_handler(player)
    app.add_handler(help_handler)

    # webhook mode → health endpoint
    if WEBHOOK_URL:
        runner = web.AppRunner(web.Application())
        runner.app.router.add_get("/healthz", health)
        asyncio.run(runner.setup())
        site = web.TCPSite(runner, "0.0.0.0", 8080)
        asyncio.create_task(site.start())

        app.run_webhook(
            listen="0.0.0.0",
            port=8443,
            url_path="webhook",
            webhook_url=WEBHOOK_URL,
        )
    else:
        asyncio.run(_polling(app))


async def _polling(app: Application) -> None:
    await app.initialize()
    async with app:
        asyncio.create_task(stream_tier_one(app.bot))
        await app.start()
        await app.updater.start_polling()  # type: ignore[attr-defined]
        await app.updater.idle()           # type: ignore[attr-defined]


if __name__ == "__main__":
    main()
