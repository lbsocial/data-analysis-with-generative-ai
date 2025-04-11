@tool
def collect_tweets(
    query: str,
    max_results: int,
    bearer_token: str,
    mongo_connection: str
) -> str:
    import tweepy
    from pymongo import MongoClient

    tweet_client = tweepy.Client(bearer_token=bearer_token, wait_on_rate_limit=True)
    mongo_client = MongoClient(mongo_connection)
    db = mongo_client["twitter_db"]
    tweet_collection = db["tweets"]

    tweets = tweet_client.search_recent_tweets(
        query=query,
        max_results=min(max_results, 100),
        expansions=["author_id"],
        tweet_fields=["created_at", "entities", "lang", "public_metrics", "geo"],
        user_fields=["id", "location", "name", "public_metrics", "username"]
    )

    tweet_data = tweets.data or []
    user_data = tweets.includes.get("users", [])
    inserted = 0

    for user, tweet in zip(user_data, tweet_data):
        tweet_json = {"tweet": tweet.data, "user": user.data}
        try:
            tweet_collection.insert_one(tweet_json)
            inserted += 1
        except:
            pass

    return f"Inserted {inserted} tweets about '{query}' into MongoDB."