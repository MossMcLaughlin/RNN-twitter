# 02-2017 | Moss McLaughlin

import csv
import itertools
import numpy as np
import nltk
import time
import sys
import operator
import io
import array
from datetime import datetime
from GRU import GRUTheano

SENTENCE_START_TOKEN = "SENTENCE_START"
SENTENCE_END_TOKEN = "SENTENCE_END"
UNKNOWN_TOKEN = "UNKNOWN_TOKEN"

def load_data(filename="tweets.txt", vocabulary_size=2000, min_sent_characters=0):


    word_to_index = []
    index_to_word = []

    print("Reading text file...")
    with open(filename, 'rt') as f:
        # split document into conversations (by line)
        txt = f.read()
        txt = txt.split('\n')
        txt = [line.split(' |') for line in txt]
        txt.pop()
        txt.pop()
        for line in txt: line.pop()

        # Filter sentences
        txt = [s for s in txt if len(s) >= min_sent_characters]
#        txt = [s for s in txt if "@" not in s]

        # Append SENTENCE_START and SENTENCE_END
    ii = 0
    for line in txt:
        jj = 0
        for tweet in line:
            txt[ii][jj] = '%s %s %s' % (SENTENCE_START_TOKEN,tweet,SENTENCE_END_TOKEN)
            jj += 1
        ii += 1

    print("Parsed %d conversation." % (len(txt)))

    # Tokenize utf-8 decoded lines 
    tokenized_sentences = [[nltk.word_tokenize(tweet.decode('utf-8')) for tweet in line] for line in txt]

    for i,line in enumerate(tokenized_sentences):
        try: tokenized_sentences[i] = line[0] + line[1] + line[2]
        except IndexError: break
         
    # FIlter words (names)
    #tokenized_sentences = [w for w in tokenized_sentences if '@' not in w]

    print(tokenized_sentences[0])

    # Count the word frequencies
    word_freq = nltk.FreqDist(itertools.chain(*tokenized_sentences))
    print("Found %d unique words tokens." % len(word_freq.items()))

    # Get the most common words and build index_to_word and word_to_index vectors
    vocab = sorted(word_freq.items(), key=lambda x: (x[1], x[0]), reverse=True)[:vocabulary_size-2]
    print("Using vocabulary size %d." % vocabulary_size)
    print("The least frequent word in our vocabulary is '%s' and appeared %d times." % (vocab[-1][0], vocab[-1][1]))

    sorted_vocab = sorted(vocab, key=operator.itemgetter(1))
    index_to_word = ["<MASK/>", UNKNOWN_TOKEN] + [x[0] for x in sorted_vocab]
    word_to_index = dict([(w, i) for i, w in enumerate(index_to_word)])
    print('\nLeast freq words in vocab: ')
    print(sorted_vocab[:25])
    print('\n')

    # Replace all words not in our vocabulary with the unknown token
    for i,line in enumerate(tokenized_sentences):
        tokenized_sentences[i] = [w if w in word_to_index else UNKNOWN_TOKEN for w in line] 

    print tokenized_sentences[0]

    # Create the training data
    X_train = np.asarray([[word_to_index[w] for w in sent[:-1]] for sent in tokenized_sentences])
    y_train = np.asarray([[word_to_index[w] for w in sent[1:]] for sent in tokenized_sentences])

    return X_train, y_train, word_to_index, index_to_word

