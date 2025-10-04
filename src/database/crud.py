from datetime import datetime
from .models import news, create_indexes

def init_db():
    create_indexes()

def insert_news(tweet):
    news.insert_one({
        "text": tweet.text,
        "author_id": str(tweet.author_id),
        "url": f"https://twitter.com/{tweet.author_id}/status/{tweet.id}",
        "created_at": datetime.utcnow(),
        "confirmed": False
    })

def get_latest_news(limit=5):
    return list(news.find().sort("created_at", -1).limit(limit))

def get_confirmed_news(limit=5):
    return list(news.find({"confirmed": True}).sort("created_at", -1).limit(limit))

def get_player_news(name):
    return list(news.find({"text": {"$regex": name, "$options": "i"}}).sort("created_at", -1).limit(5))
  
