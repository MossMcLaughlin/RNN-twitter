# 02-2017 | Moss McLaughlin

'''

Get text content from tweet IDs

'''

# standard
from __future__ import print_function
import getopt
import logging
import os
import sys
import numpy as np
# import traceback
# third-party: `pip install tweepy`
import tweepy

# global logger level is configured in main()
Logger = None

# Generate at https://apps.twitter.com/app
CONSUMER_KEY = 'IVaf7RQIknSTczbMV5kB2onis'
CONSUMER_SECRET = 'FJAPeipzPlgbBz5vuYxZ83N5YjAC5aySW43sX0djxN7VNiQKft'
OAUTH_TOKEN = '823299052813090817-3WBWGzjiSEAiSLAFLZxteQSATfGEmsB'
OAUTH_TOKEN_SECRET = 'I73ZKWPkz3NIHVZMetEGfBvR9Hxq92e3gRELNJjrWUGyt'

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
api = tweepy.API(auth)


def get_tweet_id(doc):
    f = open(doc)
    a = f.read()
    line = a.split('\n')
    tweet_id=list(np.zeros(len(line)))
    i = 0
    for lines in line:
        tweet_id[i] = lines.split('\t')
        i = i+1
    tweet_id.pop()
    tweet_id.pop()
    f.close()
#    print("tweet_id: " , tweet_id)
    return tweet_id

def get_tweet_content(doc):
    tweet_ids = []
    for conversation in get_tweet_id(doc):
        get_tweet(conversation)

def get_tweet(ids):

        #  To call multiple tweets per request 
        #  (note order is shuffled, limit 100/request)
        #tweets = api.statuses_lookup(id_=ids, include_entities=False, trim_user=True)

        # Only pull tweets with full conversation
        try: 
            tweets=  [api.get_status(ids[0]),api.get_status(ids[1]),api.get_status(ids[2])]
            with open("tweets.txt","a") as f:
                for tweet in tweets:
                    print(tweet.text.encode('UTF-8'))
                    f.write(tweet.text.encode('UTF-8')) 
                    f.write(" | ")
                f.write("\n")
        except tweepy.TweepError: None
        
    

get_tweet_content("data/MSRSocialMediaConversationCorpus/twitter_ids.tuning.txt")

