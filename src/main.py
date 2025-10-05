#!/usr/bin/env python3
"""Barça Transfer Bot – Render-ready with webhook"""

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
from fastapi.responses import JSONResponse
import uvicorn
import requests

# ---------- Fix imports for src package ----------
SRC = Path(__file__).parent
sys.path.insert(0, str(SRC))

# ---------- Internal modules ----------
from config.settings import BOT_TOKEN, MONGODB_URI, WEBHOOK_URL, OWNER_ID
from database.crud import init_db
from scrapers.twitter import stream_tier_one
from bot.handlers import start, latest, confirmed, player, help_handler

# ---------- Startup ping ----------
def _startup_ping():
    """Send a startup message to the bot owner (optional for logs)."""
    if not BOT_TOKEN or not OWNER_ID:
        print("❌ BOT_TOKEN or OWNER_ID missing.")
        return
    time.sleep(5)  # let Render flush logs
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    try:
        r = requests.post(url, json={"chat_id": OWNER_ID, "text": "🚀 Bot starting on Render…"})
        print("Startup ping:", r.status_code, r.text)
    except Exception as e:
        print("Failed startup ping:", e)

# ---------- Helpers ----------
def _wait_mongo(uri: str, timeout: int = 30) -> None:
    """Wait for MongoDB to become available."""
    for _ in range(timeout):
        try:
            MongoClient(uri, serverSelectionTimeoutMS=2_000).admin.command("ping")
            print("✅ MongoDB connected.")
            return
        except Exception:
            time.sleep(1)
    sys.exit("❌ Mongo unavailable after waiting 30 seconds.")

def _signal_handler(app: Application) -> None:
    """Graceful shutdown on SIGINT or SIGTERM."""
    def _inner(signum, frame):
        asyncio.create_task(shutdown_bot(app))
        sys.exit(0)
    signal.signal(signal.SIGINT, _inner)
    signal.signal(signal.SIGTERM, _inner)

async def shutdown_bot(app: Application):
    """Stop the Telegram bot gracefully."""
    print("🛑 Shutting down Telegram bot…")
    await app.stop()
    await app.shutdown()
    print("✅ Bot stopped.")

# ---------- FastAPI webhook app ----------
app = FastAPI()
telegram_app = Application.builder().token(BOT_TOKEN).build()

# Add Telegram command handlers
telegram_app.add_handler(start)
telegram_app.add_handler(latest)
telegram_app.add_handler(confirmed)
telegram_app.add_handler(player)
telegram_app.add_handler(help_handler)

# Webhook endpoint for Telegram
@app.post("/webhook")
async def telegram_webhook(request: Request):
    """Handle incoming Telegram updates via webhook."""
    data = await request.json()
    update = Update.de_json(data, telegram_app.bot)
    await telegram_app.update_queue.put(update)
    return {"ok": True}

# Health check for Render
@app.get("/healthz")
async def health():
    return {"status": "ok"}

# Home route
@app.api_route("/", methods=["GET", "HEAD"])
async def home(request: Request):
    if request.method == "HEAD":
        return JSONResponse(status_code=200, content=None)
    return {"status": "Barça Transfer Bot is running!"}

# ---------- Webhook setup ----------
async def set_webhook():
    """Set the Telegram webhook."""
    if WEBHOOK_URL:
        webhook_url = f"{WEBHOOK_URL.rstrip('/')}/webhook"
        async with telegram_app.bot:
            await telegram_app.bot.set_webhook(url=webhook_url)
            print(f"✅ Webhook set successfully: {webhook_url}")
    else:
        print("⚠️ WEBHOOK_URL not set, skipping webhook setup.")

# ---------- Main async entry ----------
async def main_async():
    _startup_ping()
    _wait_mongo(MONGODB_URI)
    init_db()
    _signal_handler(telegram_app)

    # Start Twitter stream asynchronously
    asyncio.create_task(stream_tier_one(telegram_app.bot))

    # Initialize and start Telegram bot (webhook mode)
    await telegram_app.initialize()
    await telegram_app.start()
    await set_webhook()
    print("✅ Telegram bot started and webhook active.")

    # Start FastAPI server
    PORT = int(os.environ.get("PORT", 8080))
    print(f"🌍 Starting FastAPI server on port {PORT}")
    config = uvicorn.Config(app, host="0.0.0.0", port=PORT)
    server = uvicorn.Server(config)
    await server.serve()

# ---------- Main ----------
if __name__ == "__main__":
    asyncio.run(main_async())
