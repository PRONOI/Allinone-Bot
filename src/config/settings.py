import os
from dotenv import load_dotenv

# Load .env for local development only
load_dotenv()

# ---------- Required ----------
BOT_TOKEN      = os.environ["BOT_TOKEN"]        # Telegram bot token
MONGODB_URI    = os.environ["MONGODB_URI"]      # MongoDB URI
TWITTER_BEARER = os.environ["TWITTER_BEARER"]   # Twitter Bearer token
CHANNEL_ID     = os.environ["CHANNEL_ID"]       # Telegram channel ID or username
OWNER_ID       = os.environ["OWNER_ID"]         # Bot owner's username or numeric ID

# ---------- Optional ----------
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
WEBHOOK_URL    = os.getenv("WEBHOOK_URL")

# ---------- Constants ----------
TIER_ONE_HANDLES = {
    "13334762": "FabrizioRomano",
    "789456": "gerardromero",
    "28271466": "orioldomenech",
    "5388642": "albert_roge",
    "4355981": "javi_miguel",
    "4728101": "DBR8",
    "14745570": "AchrafBenAyad",
}

KEYWORDS = ["Barcelona", "Barça", "Blaugrana", "Camp Nou", "La Liga"]
