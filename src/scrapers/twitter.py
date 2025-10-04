import tweepy, asyncio
from config.settings import TWITTER_BEARER, TIER_ONE_HANDLES, CHANNEL_ID
from src.filters.barca_filter import is_barca_related
from src.database.crud import insert_news

class MyStream(tweepy.StreamingClient):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    def on_tweet(self, tweet):
        if tweet.referenced_tweets:
            return
        if is_barca_related(tweet.text):
            insert_news(tweet)
            handle = TIER_ONE_HANDLES.get(str(tweet.author_id), str(tweet.author_id))
            url = f"https://twitter.com/{handle}/status/{tweet.id}"
            asyncio.create_task(
                self.bot.send_message(CHANNEL_ID, f"🚨 {tweet.text}\n— {url}")
            )

async def stream_tier_one(bot):
    stream = MyStream(bot, bearer_token=TWITTER_BEARER)
    for handle, uid in TIER_ONE_HANDLES.items():
        stream.add_rules(tweepy.StreamRule(f"from:{uid}"))
    stream.filter(expansions=["author_id"])
  
