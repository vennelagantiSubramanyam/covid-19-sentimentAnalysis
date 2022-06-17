import pandas as pd
import tweepy
from time import sleep
import csv
from datetime import datetime, date, time, timedelta
import datetime as dt
import io
import numpy as np
import joblib
import pickle
import re


def preprocess_bulk(df):
    #df=pd.read_csv('coba.csv')
    df=pd.DataFrame(df)
    df["Created_at"]= pd.to_datetime(df["Created_at"])
    
    #Count age in days
    now = pd.Timestamp('now')
    df['age_in_days'] = (now - df['Created_at']).dt.days
    #Number of tweets/age
    df['Ratio Statuses_count/age']=(df['Statuses_count']/df['age_in_days']).round(3)
    #Number of favourites/age
    df['Ratio Favorites/age']=(df['Favorites_count']/df['age_in_days']).round(3)
    #Ratio friends/follower
    df['Ratio Friends/Followers']=(df['Friends_count']/df['Followers_count']).round(3)
    #Count length of bio
    df['Length_of_Bio']=df['Description'].astype(str).str.len()
    #Measure reputation
    df['Reputation']= df['Followers_count']/(df['Followers_count']+ df['Friends_count'])
    df1=df.drop(['Geo_enabled','id_str','Created_at'], axis=1)
    df1['URL'] = pd.notnull(df1["URL"]) 
    df1['Location']=pd.notnull(df1['Location'])
    bag_of_word ='bot|b0t|updates|hourly|automatically|twitterbot|automated|'
    df2=df1
    df2['contains_bot_name']=df2['Description'].astype(str).str.contains(bag_of_word, flags=re.IGNORECASE, regex=True)
    df2=df2.drop(['Description'], axis=1)
    df2["Length_of_Bio"].fillna(0, inplace = True) 

    df2["Reputation"].fillna(0, inplace = True) 
    df2["contains_bot_name"].fillna(False, inplace=True)
    df2=pd.DataFrame(df2)
    db=df2
    db=pd.DataFrame(db)
    db['URL'].fillna(False,inplace=True)
    db.replace(np.inf, 0)
    db.replace(-np.inf, 0)
    db = db.replace([np.inf, -np.inf], 0)
    db=db.drop(['id'], axis=1)
    db = db[['Followers_count',
            'Listed_count',
            'Friends_count',
            'Favorites_count',
            'Verified',
            'Default_profile',
            'Default_profile_image',
            'Location',
            'Statuses_count',
            'URL',
            'age_in_days',
            'Ratio Statuses_count/age',
            'Ratio Favorites/age',
            'Ratio Friends/Followers',
            'Length_of_Bio',
            'contains_bot_name', 
            'Reputation',
            ]]
    data_prob=db.values.tolist()
    db=pd.DataFrame(db)
    return data_prob


def preprocess(df):
    df=pd.read_csv('coba.csv')
    df=pd.DataFrame(df)
    df["Created_at"]= pd.to_datetime(df["Created_at"])
    
    #Count age in days
    now = pd.Timestamp('now')
    df['age_in_days'] = (now - df['Created_at']).dt.days
    #Number of tweets/age
    df['Ratio Statuses_count/age']=(df['Statuses_count']/df['age_in_days']).round(3)
    #Number of favourites/age
    df['Ratio Favorites/age']=(df['Favorites_count']/df['age_in_days']).round(3)
    #Ratio friends/follower
    df['Ratio Friends/Followers']=(df['Friends_count']/df['Followers_count']).round(3)
    #Count length of bio
    df['Length_of_Bio']=df['Description'].astype(str).str.len()
    #Measure reputation
    df['Reputation']= df['Followers_count']/(df['Followers_count']+ df['Friends_count'])
    df1=df.drop(['Geo_enabled','id_str','Created_at'], axis=1)
    df1['URL'] = pd.notnull(df1["URL"]) 
    df1['Location']=pd.notnull(df1['Location'])
    bag_of_word ='bot|b0t|updates|hourly|automatically|twitterbot|automated|'
    df2=df1
    df2['contains_bot_name']=df2['Description'].astype(str).str.contains(bag_of_word, flags=re.IGNORECASE, regex=True)
    df2=df2.drop(['Description'], axis=1)
    df2["Length_of_Bio"].fillna(0, inplace = True) 

    df2["Reputation"].fillna(0, inplace = True) 
    df2["contains_bot_name"].fillna(False, inplace=True)
    df2=pd.DataFrame(df2)
    db=df2
    db=pd.DataFrame(db)
    db['URL'].fillna(False,inplace=True)
    db.replace(np.inf, 0)
    db.replace(-np.inf, 0)
    db = db.replace([np.inf, -np.inf], 0)
    db=db.drop(['id'], axis=1)
    db = db[['Followers_count',
            'Listed_count',
            'Friends_count',
            'Favorites_count',
            'Verified',
            'Default_profile',
            'Default_profile_image',
            'Location',
            'Statuses_count',
            'URL',
            'age_in_days',
            'Ratio Statuses_count/age',
            'Ratio Favorites/age',
            'Ratio Friends/Followers',
            'Length_of_Bio',
            'contains_bot_name', 
            'Reputation',
            ]]
    data_prob=db.values.tolist()
    db=pd.DataFrame(db)
    
    return data_prob,db

