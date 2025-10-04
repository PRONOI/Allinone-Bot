import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN      = os.getenv("8494296417:AAGSOP084f-TyrIwo6gdq7K-bjFK4i2vU44")
MONGODB_URI    = os.getenv("mongodb+srv://footballcontenthd:RizoeL@cluster0.z4ccfiu.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
TWITTER_BEARER = os.getenv("AAAAAAAAAAAAAAAAAAAAAIdj4gEAAAAAFdhOFrXgv08UoVlsQT1k7fFI2CE%3Dote1sHYDoPPGZIvMSJyfH3FCGXwRpyxo7ykFXu9ODszarUBwaw")
OPENAI_API_KEY = os.getenv("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")
CHANNEL_ID     = os.getenv("-1003120225849")
OWNER_ID       = os.getenv("1063334882")
WEBHOOK_URL    = os.getenv("WEBHOOK_URL")

# config/settings.py
TIER_ONE_HANDLES = {
    "13334762":  "FabrizioRomano",   # global “Here we go”
    "789456":    "gerardromero",     # Jijantes FC / Barça board leaks
    "28271466":  "orioldomenech",    # Cat Radio, inside info
    "5388642":   "albert_roge",      # Relevo / Jijantes
    "4355981":   "javi_miguel",      # AS / Cadena SER
    "4728101":   "DBR8",             # David Bernabéu Reverter
    "14745570":  "AchrafBenAyad",    # beIN Sports
}


KEYWORDS = ["Barcelona", "Barça", "Blaugrana", "Camp Nou", "La Liga"]
