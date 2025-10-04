from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from config.settings import MONGODB_URI

client = MongoClient(MONGODB_URI)
db = client.get_database()
news = db.news

def create_indexes():
    news.create_index("url", unique=True)
    news.create_index([("created_at", DESCENDING)])
    # text-search for /players <name>
    news.create_index([("text", TEXT)])
    
