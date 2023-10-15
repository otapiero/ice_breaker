import os
from datetime import datetime, timezone
import logging, dotenv

import tweepy

dotenv.load_dotenv()
logger = logging.getLogger("twitter")
print(os.environ["TWITTER_BEARER_TOKEN"])
print(os.environ["TWITTER_API_KEY"])
print(os.environ["TWITTER_API_SECRET"])
print(os.environ["TWITTER_ACCESS_TOKEN"])
print(os.environ["TWITTER_ACCESS_SECRET"])
twitter_client = tweepy.Client(
    bearer_token=os.environ["TWITTER_BEARER_TOKEN"],
    consumer_key=os.environ["TWITTER_API_KEY"],
    consumer_secret=os.environ["TWITTER_API_SECRET"],
    access_token=os.environ["TWITTER_ACCESS_TOKEN"],
    access_token_secret=os.environ["TWITTER_ACCESS_SECRET"],
)


def scrape_user_tweets(username, num_tweets=5):
    """
    Scrapes a Twitter user's original tweets (i.e., not retweets or replies) and returns them as a list of dictionaries.
    Each dictionary has three fields: "time_posted" (relative to now), "text", and "url".
    """
    user_id = twitter_client.get_user(username=username).data.id
    tweets = twitter_client.get_users_tweets(
        id=user_id, max_results=num_tweets, exclude=["retweets", "replies"]
    )
    tweets_list = []
    for tweet in tweets.data:
        tweet_dict = {
            "text": tweet["text"],
            "url": f"https://twitter.com/{username}/status/{tweet.id}",
        }
        tweets_list.append(tweet_dict)

    return tweets_list


print(scrape_user_tweets(username="hwchase17"))
