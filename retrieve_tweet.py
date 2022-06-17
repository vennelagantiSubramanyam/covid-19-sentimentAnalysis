import tweepy
from tweepy import Cursor
import unicodecsv
import numpy as np
import pandas as pd
from unidecode import unidecode
import json
import os

#try:
 #   os.stat(os.getcwd()+'\\collectindividual')
  #  path = os.getcwd()+'\\collectindividual'
#except:
    #os.mkdir(os.getcwd()+'\\collectindividual') 
    #path = os.getcwd()+'\\collectindividual'      



pd.set_option('display.max_columns', 1000)
pd.set_option('display.max_rows', 1000)
#pd.set_option('display.width', 1000)
#pd.set_option('max_colwidth', 30)
pd.set_option('colheader_justify', 'center')

# Authentication and connection to Twitter API.
consumer_key ='YBAUoHlkgYKQ9fDljywpM1DGd'
consumer_secret ='67yxNaSftHGGKfbqYe4G8nYeXZIXSe9F3il68HMLOSX5ysU047'
access_key ='120092298-stEI5XDozGPotvSYLFonT1HIbK4TAuofi9NzDm7x'
access_secret ='UiAKoMghPOCoRZ9D3BHFaKBHaVcnAJJLV3h0aBmMH8aoR'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth, wait_on_rate_limit=True)


words = ["#covid","#corona","#lockdown","#Covid-19","#coronavirus","#pandemic","#social distance","#stay home" ]
date_since = "2020-2-01"
my_list_of_dicts = []
my_demo_list = []
# Collect tweets

def data_collection(): 
    for search_words in words:
        tweets = tweepy.Cursor(api.search_tweets,q=search_words,lang="en",since=date_since).items(10)
        print(search_words)
        for json_tweet in tweets:
            my_list_of_dicts.append(json_tweet._json)
        with open('tweet_json.txt','w') as file:
            file.write(json.dumps(my_list_of_dicts, indent=4))
        with open('tweet_json.txt', encoding='utf-8') as json_file:  
            all_data = json.load(json_file)
            for each_dictionary in all_data:
                created_at = each_dictionary['created_at']
                tweet_id = each_dictionary['id']
                text = each_dictionary['text']
                retweet_count = each_dictionary['retweet_count']
                favorite_count = each_dictionary['favorite_count']
                place = each_dictionary['place']
                lang = each_dictionary['lang']
                username = each_dictionary['user']['screen_name']
                my_demo_list.append({'created_at': created_at,
                             'tweet_id': str(tweet_id),
                             'text': str(text),
                             'favorite_count': int(favorite_count),
                             'retweet_count': int(retweet_count),
                             'place': str(place),
                             'lang': str(lang),
                             'username':str(username)
                            })
                #print(my_demo_list)
                df = pd.DataFrame(my_demo_list)
                df = df.drop_duplicates(subset ="tweet_id", keep ='first').reset_index(drop=True) 
                df = df[['created_at','username','tweet_id','text','favorite_count','retweet_count','lang']]
                #print(df)
    return df
 #for tweet in tweets:
#     print(tweet)
#     tweet = pd.DataFrame()
#     print(tweet)
    


def getExceptionMessage(msg):
    words = msg.split(' ')
    errorMsg = ""
    for index, word in enumerate(words):
        if index not in [0,1,2]:
            errorMsg = errorMsg + ' ' + word
    errorMsg = errorMsg.rstrip("\'}]")
    errorMsg = errorMsg.lstrip(" \'")

    return errorMsg


def download_user_bulk(dl_user):
    try:    
        user_obj = api.get_user(dl_user)
        with open(os.path.join(path,'coba'+dl_user+'.csv'), 'wb') as file:
            writer = unicodecsv.writer(file, delimiter = ',', quotechar = '"')
            # Write header row.
            
            writer.writerow(["id",
                            "id_str",
                            "Name",
                            "Username",
                            "Followers_count",
                            "Listed_count",
                            "Friends_count",
                            "Favorites_count",
                            "Created_at",
                            "Verified",
                            "Default_profile",
                            "Default_profile_image",
                            "Location",
                            "Statuses_count",
                            "Description",
                            "URL",
                            "Geo_enabled",
                        ])
            # Gather info specific to the current user.
            user_info = [user_obj.id,
                        user_obj.id_str,
                        user_obj.name,
                        user_obj.screen_name,
                        user_obj.followers_count,
                        user_obj.listed_count,
                        user_obj.friends_count,
                        user_obj.favourites_count,
                        user_obj.created_at,
                        user_obj.verified,
                        user_obj.default_profile,
                        user_obj.default_profile_image,
                        user_obj.location,
                        user_obj.statuses_count,
                        user_obj.description,
                        user_obj.url,
                        user_obj.geo_enabled,
                        ]
            writer.writerow(user_info)
             # Show status if success
            print("Wrote tweets by %s to CSV." % dl_user)
    except tweepy.TweepError as e:
            print ("\n"+str(e.api_code) +":"+ getExceptionMessage(e.reason)+"\n")



def download_user(dl_user):
    try:    
        user_obj = api.get_user(dl_user)
        with open('coba.csv', 'wb') as file:
            writer = unicodecsv.writer(file, delimiter = ',', quotechar = '"')
            # Write header row.
            
            writer.writerow(["id",
                            "id_str",
                            "Name",
                            "Username",
                            "Followers_count",
                            "Listed_count",
                            "Friends_count",
                            "Favorites_count",
                            "Created_at",
                            "Verified",
                            "Default_profile",
                            "Default_profile_image",
                            "Location",
                            "Statuses_count",
                            "Description",
                            "URL",
                            "Geo_enabled",
                        ])
            # Gather info specific to the current user.
            user_info = [user_obj.id,
                        user_obj.id_str,
                        user_obj.name,
                        user_obj.screen_name,
                        user_obj.followers_count,
                        user_obj.listed_count,
                        user_obj.friends_count,
                        user_obj.favourites_count,
                        user_obj.created_at,
                        user_obj.verified,
                        user_obj.default_profile,
                        user_obj.default_profile_image,
                        user_obj.location,
                        user_obj.statuses_count,
                        user_obj.description,
                        user_obj.url,
                        user_obj.geo_enabled,
                        ]
            writer.writerow(user_info)
             # Show status if success
            print("Wrote tweets by %s to CSV." % dl_user)
    except tweepy.TweepError as e:
            print ("\n"+str(e.api_code) +":"+ getExceptionMessage(e.reason)+"\n")

