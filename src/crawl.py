#!/usr/bin/env python3
#-*- coding:utf-8 -*-

from PrepareChain import PreapreChain

def addData(text):
    """
    add newTweet
    @param text newtweet
    """
    lines = text.split('\n')
    lines = [line.strip() for line in lines]
    for line in lines:
        chain = PrepareChain(line)
        triplet_freqs = chain.make_triplet_freqs()
        chain.save(triplet_freqs, False)
