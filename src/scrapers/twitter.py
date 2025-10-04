import asyncio
import tweepy
from config.settings import TWITTER_BEARER, TIER_ONE_HANDLES, CHANNEL_ID
from src.filters.barca_filter import is_barca_related
from src.database.crud import insert_news


class MyStream(tweepy.StreamingClient):
    def __init__(self, bot, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.bot = bot

    def on_tweet(self, tweet):
        if tweet.referenced_tweets:               # skip retweets / replies
            return
        if is_barca_related(tweet.text):
            insert_news(tweet)
            handle = TIER_ONE_HANDLES.get(str(tweet.author_id), str(tweet.author_id))
            url  = f"https://twitter.com/{handle}/status/{tweet.id}"
            # schedule the coroutine from the event-loop thread-safe
            asyncio.create_task(
                self.bot.send_message(CHANNEL_ID, f"🚨 {tweet.text}\n— {url}")
            )


async def stream_tier_one(bot):
    client = MyStream(bot, bearer_token=TWITTER_BEARER)

    # 1. remove old rules (idempotent)
    old_rules = client.get_rules().data
    if old_rules:
        client.delete_rules([r.id for r in old_rules])

    # 2. add new rules
    for uid in TIER_ONE_HANDLES.keys():
        client.add_rules(tweepy.StreamRule(f"from:{uid}"))

    # 3. start filtered stream
    client.filter(expansions=["author_id"], tweet_fields=["created_at"])
    
