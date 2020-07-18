#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import string
from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
from nltk.stem.porter import PorterStemmer


#to list
def preprocess(frames_df):

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

    #remove non-latin chars
    frames_df['cln'] = frames_df['cln'].str.replace(r'[^\x00-\x7f]', "") 

    data = frames_df.cln.values.tolist()
    data_words = list(data)
    print(data_words[:1])
    return data_words

#remove non alpha and punctutation


def remove_digits(mylist):
    no_digits = [x for x in mylist if not any(c.isdigit() for c in x)]
    no_punc = ["".join( j for j in i if j not in string.punctuation) for i in mylist]
    #return no_digits
    return no_punc


stop_words = stopwords.words('english')
stop_words.extend(['from', 'subject', 're', 'edu', 'use', 'not', 'would',
                     'say', 'could', '_', 'be', 'know', 'good', 'go', 'get',
                     'do', 'done', 'try', 'many', 'some', 'nice', 'thank', 'think',
                     'see', 'rather', 'easy', 'easily', 'lot', 'lack', 'make',
                     'want', 'seem', 'run', 'need', 'even', 'right', 'line',
                     'even', 'also', 'may', 'take', 'come', 'coronavirus', 'covid', '19', 'covid19',
                     'to', 'of', 'for', 'at'])

# list for tokenized documents in loop
tokenizer = RegexpTokenizer(r'\w+')
p_stemmer = PorterStemmer()

def tokenize_and_stopwords(mylist):

   texts = []

   # loop through document list
   for i in mylist:

       # clean and tokenize document string
       raw = i.lower()
       tokens = tokenizer.tokenize(raw)

       # remove stop words from tokens
       stopped_tokens = [i for i in tokens if not i in stop_words]

       # stem tokens
       stemmed_tokens = [p_stemmer.stem(i) for i in stopped_tokens]

       # add tokens to list
       texts.append(stemmed_tokens)
       #texts.append(stopped_tokens)

   return texts
