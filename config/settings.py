import os
from dotenv import load_dotenv
load_dotenv()

BOT_TOKEN      = os.getenv("8494296417:AAGSOP084f-TyrIwo6gdq7K-bjFK4i2vU44")
MONGODB_URI    = os.getenv("mongodb+srv://AsadAli:AsadAli@cluster0.3ejv7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
TWITTER_BEARER = os.getenv("AAAAAAAAAAAAAAAAAAAAAIdj4gEAAAAAFdhOFrXgv08UoVlsQT1k7fFI2CE%3Dote1sHYDoPPGZIvMSJyfH3FCGXwRpyxo7ykFXu9ODszarUBwaw")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
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
