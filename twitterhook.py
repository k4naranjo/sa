#Twitter hook

# import tweepy
import tweepy as tw

#reads login info
f=open("../twitter_credentials.txt","r")
lines=f.readlines()
# your Twitter API key and API secret
my_api_key=lines[1].rstrip("\n")
my_api_secret=lines[3].rstrip("\n")
access_token=lines[5].rstrip("\n")
access_token_secret=lines[7].rstrip("\n")
f.close()

#print(twitter_key)
#print(twitter_secret)
#print(access_token)
#print(access_token_secret)


# authenticate
auth = tw.OAuthHandler(my_api_key, my_api_secret)
auth.set_access_token(access_token, access_token_secret)

api = tw.API(auth, wait_on_rate_limit=True)


search_query = "#defundthepolice -filter:retweets"

# get tweets from the API
tweets = tw.Cursor(api.search,
              q=search_query,
              lang="en",
              since="2020-09-16").items(50)


# store the API responses in - list third part 
tweets_copy = []
for tweet in tweets:
	try:
		tweets_copy.append(tweet)
	except tw.TweepError as e:
		print("Something went wrong")
		print("Tweepy Error: {}".format(e))

print("Total Tweets fetched:", len(tweets_copy))


#organize tweets from a data frame 
import pandas as pd

# intialize the dataframe
tweets_df = pd.DataFrame()

# populate the dataframe
for tweet in tweets_copy:
    hashtags = []
    try:
        for hashtag in tweet.entities["hashtags"]:
            hashtags.append(hashtag["text"])
        text = api.get_status(id=tweet.id, tweet_mode='extended').full_text
    except:
        pass
    tweets_df = tweets_df.append(pd.DataFrame({'user_name': tweet.user.name, 
                                               'user_location': tweet.user.location,\
                                               'user_description': tweet.user.description,
                                               'user_verified': tweet.user.verified,
                                               'date': tweet.created_at,
                                               'text': text, 
                                               'hashtags': [hashtags if hashtags else None],
                                               'source': tweet.source}))
    tweets_df = tweets_df.reset_index(drop=True)

# show the dataframe
tweets_df.head()