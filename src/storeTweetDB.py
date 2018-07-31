#!/usr/bin/env python
#-*- coding:utf-8 -*-

from PrepareChain import PrepareChain
import pandas as pd
from tqdm import tqdm

def storeTweetDB(csv_path):
    """
    read tweetcsv
    """
    df = pd.read_csv(csv_path)

    tweets = df['text']
    print(len(tweets))
    
    chain = PrepareChain(tweets[0])
    triplet_freqs = chain.make_triplet_freqs()
    chain.save(triplet_freqs, True)

    for i in tqdm(tweets[1:]):
        print(i)
        chain = PrepareChain(i)
        triplet_freqs = chain.make_triplet_freqs()
        chain.save(triplet_freqs, False)

if __name__ == '__main__':
    csv_path = '../dataset/processedtweets.csv'
    storeTweetDB(csv_path)

