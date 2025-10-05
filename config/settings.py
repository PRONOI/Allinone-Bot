import os
from pathlib import Path
from dotenv import load_dotenv

# local dev only – Render ignores .env
load_dotenv()

# ---------- required ----------
BOT_TOKEN      = os.environ["BOT_TOKEN"]        # Your Telegram bot token
MONGODB_URI    = os.environ["MONGODB_URI"]      # MongoDB Atlas or local URI
TWITTER_BEARER = os.environ["TWITTER_BEARER"]   # Twitter Developer bearer token
CHANNEL_ID     = os.environ["CHANNEL_ID"]       # Telegram channel username or numeric ID
OWNER_ID       = os.environ["OWNER_ID"]         # Bot owner's username or numeric ID]           # @YourUsername or numeric ID

# ---------- optional ----------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY") or None
WEBHOOK_URL    = os.getenv("WEBHOOK_URL") or None

# ---------- constants ----------
TIER_ONE_HANDLES = {
    "13334762": "FabrizioRomano",
    "789456":   "gerardromero",
    "28271466": "orioldomenech",
    "5388642":  "albert_roge",
    "4355981":  "javi_miguel",
    "4728101":  "DBR8",
    "14745570": "AchrafBenAyad",
}

KEYWORDS = ["Barcelona", "Barça", "Blaugrana", "Camp Nou", "La Liga"]
