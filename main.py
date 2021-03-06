
import numpy as np # linear algebra
import pandas as pd # data processing
import matplotlib.pyplot as plt
#s%matplotlib inline
from wordcloud import WordCloud,STOPWORDS
from aux import *



#######################################################################
#Pull data directly from Twitter

api=connect_to_twitter("../twitter_credentials.txt")

search_for="pfizer + vaccine"
search_query = search_for + " -filter:retweets"
start_date="2020-01-08"
until_date="2021-01-09"
num_tweets=100
cloud_title="pfizer vaccine"
barg_title="pfizer vaccine"
map_filename="pfizer_vaccine_map"

#######################################################################

tweets_df=get_tweets(api,search_query,start_date,until_date,num_tweets)

if len(tweets_df.index)!=0:

	#print(tweets_df[['date']]) #date verification
	# show the dataframe
	#tweets_df.head()

	# clean words for word clouds
	clean_words = clean_word(tweets_df)
	#create word cloud and save image
	wcloud(clean_words,"../data/wc_"+search_for.replace(" ","_")+"_"+start_date,cloud_title+" - "+start_date)

	#run sentiment analysis classifier
	tweets_df=sa_tweets(tweets_df,"../data/barg_vaccine_"+start_date,barg_title+" ("+start_date+")")

	#save to csv file
	tweets_df.to_csv('../data/tweets_'+search_for.replace(" ","_")+'_'+start_date+'.csv', index = True)

	# #save to database
	# #save_df_to_db(tweets_df,"../database_credentials.txt","tweets_"+search_for)


	#create a map
	create_tweets_map(tweets_df,"../data/maps/"+map_filename)
else:
	print("No tweets were retrieved.")


########################################################################
#Pull tweets from csv file

#tweets_df2=pd.read_csv("../data/tweets_#vaccine_2021-01-04.csv")
#print(tweets_df2.head())

#word cloud
#clean words for word clouds
#clean_words2 = clean_word(tweets_df2)
#create word cloud and save image
#wcloud(clean_words2,"read_experiment","Vaccine word cloud 2- 2021-01-04")


#run sentiment analysis classifier
# tweets_df2=sa_tweets(tweets_df2,"vaccine_image_test","Vaccine mentions (2021-01-04)")