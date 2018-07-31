#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import json

from requests_oauthlib import OAuth1Session

from GenerateText import GenerateText

def genTweet():
    """
    Generate Tweets
    """
    try:
        keysfile = open('/home/ubuntu/text_writer/src/keys.json') 
        keys = json.load(keysfile)
        print('before generator')
        generator = GenerateText(1)
        print('after generator')	    
        oauth = create_oauth_session(keys)
        print('after oauth')
        sendtweet(oauth, generator)
        print('after sendtweet')
    except Exception as e:
        print('%r' % e, flush=True)
    

def create_oauth_session(oauth_key_dict):
    """
    make session
    """
    oauth = OAuth1Session(
                oauth_key_dict['consumer_key'],
                oauth_key_dict['consumer_secret'],
                oauth_key_dict['access_token'],
                oauth_key_dict['access_token_secret']
                )
    return oauth

def sendtweet(oauth, generator):
    """
    making line and sending tweet
    """
    print('in sendtweet')
    url = 'https://api.twitter.com/1.1/statuses/update.json'
    tweet = generator.generate()
    print(tweet)
    params = { 'status': tweet }
    req = oauth.post(url, params)

    if req.status_code == 200:
        print('tweet success', flush=True)
    else:
        print('tweet failed', flush=True)

if __name__ == '__main__':
    try:
        genTweet()
    except Exception as e:
        print('%r' % e, flush=True)
