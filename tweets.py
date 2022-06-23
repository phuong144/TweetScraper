# Python Script to Extract tweets of a
# particular Hashtag using Tweepy and Pandas
import os
from dotenv import load_dotenv

load_dotenv()
# import modules
import pandas as pd
import tweepy

# function to display data of each tweet
def printtweetdata(n, ith_tweet):
    print()
    print(f"Tweet {n}:")
    print(f"Username:{ith_tweet[0]}")
    print(f"Description:{ith_tweet[1]}")
    print(f"Location:{ith_tweet[2]}")
    print(f"Following Count:{ith_tweet[3]}")
    print(f"Follower Count:{ith_tweet[4]}")
    print(f"Total Tweets:{ith_tweet[5]}")
    print(f"Retweet Count:{ith_tweet[6]}")
    print(f"Tweet Text:{ith_tweet[7]}")
    print(f"Hashtags Used:{ith_tweet[8]}")


# function to perform data extraction
def scrape(words, numtweet):

    # Creating DataFrame using pandas

    db = pd.DataFrame(
        columns=[
            "username",
            "description",
            "user_location",
            "created_at",
            "text",
            "like_count",
            "tweet_location",
            "tweet_country",
            "tweet_place_type",
        ]
    )

    # classtweepy.Response(data, includes, errors, meta)
    # type(res.data) = <class 'list'>
    res = client.search_recent_tweets(
        query=words,
        expansions=["author_id", "geo.place_id"],
        tweet_fields=[
            "context_annotations",
            "created_at",
            "public_metrics",
        ],
        user_fields=["description", "location"],
        place_fields=["country", "name", "country_code", "place_type"],
        max_results=numtweet,
    )
    # Counter to maintain Tweet Count
    i = 1
    """
    # https://developer.twitter.com/en/docs/twitter-api/fields
    for i in range(len(res.data)):
        text = res.data[i].text
        created_at = res.data[i].created_at
        username = res.includes["users"][i].username
        description = res.includes["users"][i].description
        user_location = res.includes["users"][i].location

        like_count = res.data[i].public_metrics.like_count

        tweet_location = res.includes.places[i].full_name
        tweet_country = res.includes.places[i].country
        tweet_place_type = res.includes.places[i].place_type

        # Retweets can be distinguished by
        # a retweeted_status attribute,
        # in case it is an invalid reference,
        # except block will be executed

        # Here we are appending all the
        # extracted information in the DataFrame
        ith_tweet = [
            username,
            description,
            user_location,
            created_at,
            text,
            like_count,
            tweet_location,
            tweet_country,
            tweet_place_type,
        ]
        db.loc[len(db)] = ith_tweet
        # Function call to print tweet data on screen
        # printtweetdata(i, ith_tweet)
        i = i + 1
    filename = "scraped_tweets.csv"

    # we will save our database as a CSV file.
    db.to_csv(filename)
    """


if __name__ == "__main__":

    # search_recent api only allows OAuth2.0 Bearer Token (App-Only)
    client = tweepy.Client(os.getenv("bearerToken"))

    """ Twitter API v1.1 User Context
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_key, access_secret)
    api = tweepy.API(auth)
    """

    # Enter Hashtag and initial date
    print("Enter Twitter HashTag to search for")
    words = input()
    # print("Enter Date since The Tweets are required in yyyy-mm--dd")
    # date_since = input()

    # number of tweets you want to extract in one run
    numtweet = 10
    scrape(words, numtweet)
    print("Scraping has completed!")
