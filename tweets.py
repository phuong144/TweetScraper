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
    print(f"UID {ith_tweet[0]}:")
    print(f"Username:{ith_tweet[1]}")
    print(f"Description:{ith_tweet[2]}")
    print(f"User_location:{ith_tweet[3]}")
    print(f"Created At:{ith_tweet[4]}")
    print(f"Text:{ith_tweet[5]}")
    print(f"Like_Count:{ith_tweet[6]}")
    print(f"Tweet_Location:{ith_tweet[7]}")

# function to perform data extraction
def scrape(words, numtweet):

    # Creating DataFrame using pandas

    db = pd.DataFrame(
        columns=[
            "uid",
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

    res = client.search_recent_tweets(
        query=words,
        expansions=["author_id", "geo.place_id"],
        tweet_fields=[
            "created_at",
            "public_metrics",
        ],
        user_fields=["description", "location"],
        place_fields=["country", "name", "country_code", "place_type"],
        max_results=numtweet,
    )

    print(len(res.data), len(res.includes["users"]))

    userDict = {}
    for user in res.includes["users"]:
        userDict[user.id] = user

    placesDict = {}
    if "places" in res.includes:
        for place in res.includes["places"]:
            placesDict[place.id] = place
    

    # https://developer.twitter.com/en/docs/twitter-api/fields
    for i in range(len(res.data)):
        uid = res.data[i].author_id
        text = res.data[i].text
        created_at = res.data[i].created_at

        username = userDict[res.data[i].author_id].username
        description = userDict[res.data[i].author_id].description
        user_location = userDict[res.data[i].author_id].location

        like_count = res.data[i].public_metrics["like_count"]

        tweet_location = "None"
        tweet_country = "None"
        tweet_place_type = "None"

        if "geo" in res.data[i]:
            tweet_location = placesDict[res.data[i]['geo'].place_id].full_name
            tweet_country = placesDict[res.data[i]['geo'].place_id].country
            tweet_place_type = placesDict[res.data[i]['geo'].place_id].place_type

        ith_tweet = [
            uid,
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
        printtweetdata(i, ith_tweet)
    filename = "scraped_tweets.csv"

    # we will save our database as a CSV file.
    # db.to_csv(filename)

if __name__ == "__main__":

    # search_recent api only allows OAuth2.0 Bearer Token (App-Only)
    client = tweepy.Client(os.getenv("bearerToken"))

    # Enter Hashtag and initial date
    print("Enter Twitter HashTag to search for")
    words = input()

    # print("Enter Date since The Tweets are required in yyyy-mm--dd")
    # date_since = input()

    # words += " -is:retweet"

    # number of tweets you want to extract in one run
    numtweet = 100
    scrape(words, numtweet)
    print("Scraping has completed!")
