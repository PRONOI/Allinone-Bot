#!/usr/bin/env python3
"""Barça Transfer Bot – entry point (webhook-ready)"""
from __future__ import annotations

import asyncio
import os
import signal
import sys
import time
from pathlib import Path

from pymongo import MongoClient
from telegram import Update
from telegram.ext import Application
from fastapi import FastAPI, Request
import uvicorn
import requests

# ---------- Fix imports for src/ package ----------
SRC = Path(__file__).parent
sys.path.insert(0, str(SRC))  # src/ is top-level for imports

# ---------- Internal modules using relative imports ----------
from .config.settings import BOT_TOKEN, MONGODB_URI, WEBHOOK_URL, OWNER_ID
from .database.crud import init_db
from .scrapers.twitter import stream_tier_one
from .bot.handlers import start, latest, confirmed, player, help_handler
# You can add other modules like filters or utils if needed
# from .filters.my_filters import some_filter
# from .utils.helpers import some_helper

# ---------- Startup ping ----------
def _startup_ping():
    token = BOT_TOKEN
    owner = OWNER_ID
    if not token or not owner:
        print("❌  BOT_TOKEN or OWNER_ID missing")
        return
    time.sleep(5)  # let Render flush logs
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    r = requests.post(url, json={"chat_id": owner, "text": "Bot starting…"})
    print("Startup ping:", r.status_code, r.text)

# ---------- Rate-limit ----------
SEND_SEM = asyncio.Semaphore(25)

# ---------- Helpers ----------
def _wait_mongo(uri: str, timeout: int = 30) -> None:
    for _ in range(timeout):
        try:
            MongoClient(uri, serverSelectionTimeoutMS=2_000).admin.command("ping")
            return
        except Exception:
            time.sleep(1)
    sys.exit("Mongo unavailable")

def _signal_handler(app: Application) -> None:
    def _inner(signum, frame):
        asyncio.create_task(app.shutdown())
        sys.exit(0)
    signal.signal(signal.SIGINT, _inner)
    signal.signal(signal.SIGTERM, _inner)

# ---------- FastAPI webhook app ----------
app = FastAPI()
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Add handlers
telegram_app.add_handler(start)
telegram_app.add_handler(latest)
telegram_app.add_handler(confirmed)
telegram_app.add_handler(player)
telegram_app.add_handler(help_handler)

@app.post("/webhook")
async def telegram_webhook(request: Request):
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.update_queue.put(update)
    return {"ok": True}

@app.get("/healthz")
async def health():
    return {"status": "ok"}

# ---------- Main ----------
def main() -> None:
    _startup_ping()
    _wait_mongo(MONGODB_URI)
    init_db()
    _signal_handler(telegram_app)

    # Start Twitter stream asynchronously
    asyncio.create_task(stream_tier_one(telegram_app.bot))

    # Start FastAPI server
    PORT = int(os.environ.get("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=PORT)

if __name__ == "__main__":
    main()
