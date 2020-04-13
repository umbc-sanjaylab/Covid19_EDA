#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import LatentDirichletAllocation
import argparse


class make_topics(object):

    def __init__(self, nrt_df):
        """
        df = no retweets
        """
        self.nrt_df = nrt_df

    def make_frames(self):
        hospital =  self.nrt_df.loc[(self.nrt_df['hospital'] ==True)]
        mask = self.nrt_df.loc[(self.nrt_df['mask'] ==True)]
        icu = self.nrt_df.loc[(self.nrt_df['icu'] ==True)]
        help_ = self.nrt_df.loc[(self.nrt_df['help'] ==True)]
        nurse = self.nrt_df.loc[(self.nrt_df['nurse'] ==True)]
        doctors = self.nrt_df.loc[(self.nrt_df['doctors'] ==True)]
        vent = self.nrt_df.loc[(self.nrt_df['vent'] ==True)]
        test_pos = self.nrt_df.loc[(self.nrt_df['test_pos'] ==True)]
        serious_cond = self.nrt_df.loc[(self.nrt_df['serious_cond'] ==True)]
        exposure = self.nrt_df.loc[(self.nrt_df['exposure'] ==True)]
        cough = self.nrt_df.loc[(self.nrt_df['cough'] ==True)]
        fever = self.nrt_df.loc[(self.nrt_df['fever'] ==True)]
        return hospital, mask, icu, help, nurse, doctors, vent, test_pos, serious_cond, exposure, cough, fever


    def get_topics(self, frames_df, outfile):

        #Args: df is result of make_frames

        #===processing====
        #will create a new dataframe column called 'cln'

        # removing everything except alphabets`
        frames_df['cln'] = frames_df['text'].str.replace("[^a-zA-Z#]", " ")

        # removing short words
        frames_df['cln'] = frames_df['text'].apply(lambda x: ' '.join([w for w in x.split() if len(w)>3]))

        # make all text lowercase
        frames_df['cln'] = frames_df['text'].apply(lambda x: x.lower())

        #remove the https: and all urls
        frames_df['cln'] = frames_df['cln'].str.replace(r'https?://[^\s<>"]+|www\.[^\s<>"]+', "")

        #remove usernames @signs
        frames_df['cln'] = frames_df['cln'].str.replace(r'(@[A-Za-z0-9]+)', "")

        """
        #SVD APPROACH

        vectorizer = TfidfVectorizer(ngram_range=(3,4))
        matrix = vectorizer.fit_transform(df['cln'])


        # SVD represent documents and terms in vectors
        svd_model = TruncatedSVD(n_components=10, algorithm='randomized', n_iter=100, random_state=122)

        svd_model.fit(matrix)

        len(svd_model.components_)

        terms = vectorizer.get_feature_names()

        for i, comp in enumerate(svd_model.components_):
            terms_comp = zip(terms, comp)
            sorted_terms = sorted(terms_comp, key= lambda x:x[1], reverse=True)[:7]
            print("Topic "+str(i)+": ")
            for t in sorted_terms:
                print(t[0])
                print(" \n")

        """

        n_samples = 2000
        n_features = 1000
        n_components = 10
        n_top_words = 10


        def print_top_words(model, feature_names, n_top_words):
            #outfile is a path "outfile.txt"
            text_file = open(outfile, "w")
            for topic_idx, topic in enumerate(model.components_):
                message = "Topic #%d: " % topic_idx
                message += " ".join([feature_names[i] for i in topic.argsort()[:-n_top_words - 1:-1]])
                print(message)

                text_file.write(message)
                text_file.write("\n")
            text_file.close()
            print()

        # Use tf-idf features for NMF.
        print("Extracting tf-idf features for NMF...")
        tfidf_vectorizer = TfidfVectorizer(max_df=0.95, min_df=2,
                                       max_features=n_features,
                                       stop_words='english',
                                      ngram_range=(2,3))

        tfidf = tfidf_vectorizer.fit_transform(frames_df['cln'])

        print("Fitting LDA models with tf features, "
          "n_samples=%d and n_features=%d..." % (n_samples, n_features))
        lda = LatentDirichletAllocation(n_components=n_components, max_iter=5,
                                    learning_method='online',
                                    learning_offset=50.,
                                    random_state=0)

        lda.fit(tfidf)


        print("\nTopics in LDA model:")
        tf_feature_names = tfidf_vectorizer.get_feature_names()
        print_top_words(lda, tf_feature_names, n_top_words)
