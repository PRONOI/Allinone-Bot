from pymongo import MongoClient, ASCENDING, DESCENDING, TEXT
from config.settings import MONGODB_URI

client = MongoClient(MONGODB_URI)
db = client.get_database()
news = db.news


def create_indexes() -> None:
    """Create all persistent indexes for the news collection."""
    # 1. unique link → prevent duplicates
    news.create_index("url", unique=True)

    # 2. latest-first queries (/latest, /confirmed)
    news.create_index([("created_at", DESCENDING)])

    # 3. full-text search (/players <name>)
    news.create_index([("text", TEXT)])

    # 4. filter by journalist  (future /by_journalist feature)
    news.create_index("author_id")

    # 5. compound:  journalist + date  (newest by journo)
    news.create_index([("author_id", ASCENDING), ("created_at", DESCENDING)])
    
