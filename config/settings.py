import os
from pathlib import Path
from dotenv import load_dotenv

# local dev only – Render ignores .env
load_dotenv()

# ---------- required ----------
BOT_TOKEN      = os.environ["BOT_TOKEN"]          # 46-50 chars, no spaces
MONGODB_URI    = os.environ["MONGODB_URI"]        # full Atlas or local string
TWITTER_BEARER = os.environ["TWITTER_BEARER"]     # Twitter Developer bearer
CHANNEL_ID     = os.environ["CHANNEL_ID"]         # @ChannelName or numeric ID
OWNER_ID       = os.environ["OWNER_ID"]           # @YourUsername or numeric ID

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
