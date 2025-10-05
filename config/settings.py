import os
from pathlib import Path
from dotenv import load_dotenv

# local dev only – Render ignores .env
load_dotenv()

# ---------- required ----------
BOT_TOKEN      = os.environ["8494296417:AAGSOP084f-TyrIwo6gdq7K-bjFK4i2vU44"]          # 46-50 chars, no spaces
MONGODB_URI    = os.environ["mongodb+srv://footballcontenthd:RizoeL@cluster0.j4idtvi.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"]        # full Atlas or local string
TWITTER_BEARER = os.environ["AAAAAAAAAAAAAAAAAAAAAIdj4gEAAAAAFdhOFrXgv08UoVlsQT1k7fFI2CE%3Dote1sHYDoPPGZIvMSJyfH3FCGXwRpyxo7ykFXu9ODszarUBwaw"]     # Twitter Developer bearer
CHANNEL_ID     = os.environ["-1003120225849"]         # @ChannelName or numeric ID
OWNER_ID       = os.environ["1003120225849"]           # @YourUsername or numeric ID

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
