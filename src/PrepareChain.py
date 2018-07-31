#!/usr/bin/env python
#-*- coding:utf-8 -*-
import re
import sqlite3
from collections import defaultdict

import MeCab

class PrepareChain(object):
    """
    チェーンの作成してDBに保存
    """
    BEGIN = "__BEGIN_SENTENCE__"
    END = "__END_SENTENCE__"

    DB_PATH = "/Users/t16076yi/text_writer/src/chain.db"
    DB_SCHEMA_PATH = "/Users/t16076yi/text_writer/src/schema.sql"

    def __init__(self, text):
        """
        初期化用
        @params text チェーンを作成するための元の文章
        """
        if isinstance(text, str):
            self.text = text
        self.tagger = MeCab.Tagger("-Owakati -d /usr/local/lib/mecab/dic/mecab-ipadic-neologd")

    def make_triplet_freqs(self):
        """
        形態素解析から３つ組の出現回数まで
        @return ３つ組とその出現回数の辞書 key: ３つ組(tuple) val: freq
        """
        sentences = self._divide(self.text)
        triplet_freqs = defaultdict(int)

        for sentence in sentences:
            morphemes = self._morphological_analysis(sentence)
            triplets = self._make_triplet(morphemes)
            for (triplet, n) in triplets.items():
                triplet_freqs[triplet] += n
        return triplet_freqs

    def _divide(self, text):
        """
        改行文字で一文ずつに分ける
        @param text 分割前の文章
        @return １文ずつのlist
        """
        text = text.split("\n")
        text = [line for line in text if text != ""]
        return text

    def _morphological_analysis(self, sentence):
        """
        １文を形態素解析する

        @param sentence 一文
        @return 形態素解析されたlist
        """
        node = self.tagger.parse(sentence)
        node = node.split(' ')[:-1]
        return node

    def _make_triplet(self, morphemes):
        """
        形態素に分けた配列を３つ組にしてその出現回数を数える。
        @param morphemes 形態素配列
        @return ３つ組とその出現回数の辞書 key: triplet(tuple) val: freq
        """
        if len(morphemes) < 3:
            return {}
        # frequency dictionary
        triplet_freqs = defaultdict(int)
        for i in range(len(morphemes)-2):
            triplet = tuple(morphemes[i:i+3])
            triplet_freqs[triplet] += 1
        
        # add BEGIN
        triplet = (PrepareChain.BEGIN, morphemes[0], morphemes[1])
        triplet_freqs[triplet] = 1

        # add END
        triplet = (morphemes[-2], morphemes[-1], PrepareChain.END)
        triplet_freqs[triplet] = 1
        return triplet_freqs

    def save(self, triplet_freqs, init=False):
        """
        3つ組毎に出現回数をDBに保存
        @param triplet_freqs 3つ組とその出現回数の辞書 key: triplet(tuple) val: freq
        """
        # open DB
        con = sqlite3.connect(PrepareChain.DB_PATH)
        if init:
            with open(PrepareChain.DB_SCHEMA_PATH, "r") as f:
                schema = f.read()
                con.executescript(schema)

        datas = [(triplet[0], triplet[1], triplet[2], freq) for (triplet, freq) in triplet_freqs.items()]
        p_statement = "INSERT INTO chain_freqs (prefix1, prefix2, suffix, freq) values (?, ?, ?, ?)"
        con.executemany(p_statement, datas)

        con.commit()
        con.close()

    def show(self, triplet_freqs):
        """
        ３つ組の出現回数を出力
        @param triplet_freqs 3つ組とその出現回数の辞書 key: triplet(tuple) val: apper_count
        """
        for triplet in triplet_freqs:
            print("|".join(triplet), "\t", triplet_freqs[tiplet])

