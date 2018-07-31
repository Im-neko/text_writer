#!/usr/bin/env python
#-*- coding:utf-8 -*-
import re

import pandas as pd
from lxml import html

def clean_tweet(text):
    """
    一旦全てを置換し、文末の改行コードだけ元に戻す。
    この際、置換するワードは今までの自分の記憶を辿り、
    今までつぶやいたことがないワードが望ましい
    """
    data = text.replace('\n', ' ').replace('" ', '"\n')
    with open('./../dataset/clean_tweets.csv', 'w') as f:
        f.write(data)
    df = pd.read_csv('./../dataset/clean_tweets.csv')
    # 正規表現でIDとURL,ハッシュタグ、RTを消す
    replypattern = '@[\w]+'
    hashpattern = '#[\w]+'
    urlpattern = 'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
    whitelist = ['Twitter for iPhone', 'TweetDeck']
    processedtweets = []
    
    for index, rows in df.iterrows():
        if html.fromstring(rows['source']).text_content() in whitelist:
            tweet = rows['text']
            if str(rows['retweeted_status_timestamp']) == 'nan':
                i = re.sub(replypattern, '', tweet)
                i = re.sub(hashpattern, '', i)
                i = re.sub(urlpattern, '', i)
                if isinstance(i, str) and not i.split():
                    pass
                else:
                    processedtweets.append(i)
                    print(i)
    processedtweetsDataFrame = pd.Series(processedtweets)
    newDF = pd.DataFrame({'text': processedtweetsDataFrame})
    return newDF
    
def main():
    text = ''
    with open('./../dataset/tweets.csv', 'r') as f:
        text = f.read()
    newDF = clean_tweet(text)
    newDF.to_csv('./../dataset/processedtweets.csv')

if __name__=='__main__':
    main()
