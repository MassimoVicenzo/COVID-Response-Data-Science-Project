import os.path as op
from os import getcwd
import argparse as ap
import pandas as pd
import spacy
from collections import Counter
from math import log


nlp = spacy.load("en_core_web_sm")
nlp.add_pipe("emoji", first=True)


def parse_input():
    parser = ap.ArgumentParser()
    parser.add_argument('-i', '--inpath', required=True)
    parser.add_argument('-o', '--outpath', required=True)
    parser.add_argument('-w', '--stopwordspath', required=True)

    args = parser.parse_args()

    inpath = op.normpath(op.join(getcwd(), args.inpath))
    outpath = op.normpath(op.join(getcwd(), args.outpath))
    stopwordspath = op.normpath(op.join(getcwd(), args.stopwordspath))

    return inpath, outpath, stopwordspath

def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        df = pd.read_csv(path, index_col='id', usecols=['id', 'text', 'topic'])
    return df

def load_stopwords(path):
    with open(path) as f:
        stopwords = f.read().split('\n')[6:]
    return set(stopwords)

def combine_topics(df, sep):
    groups = df.groupby(['topic'])
    df['document'] = df.groupby(['topic'])['text'].transform(lambda x: sep.join(x))
    df2 = df[['topic', 'document']].drop_duplicates().set_index('topic')
    return df2['document'].rename('documents')
    

def is_unwanted_token(token, stopwords):
    return token.is_space \
        or token.is_stop \
        or token.is_punct \
        or token.like_num \
        or token.like_url \
        or token.like_email \
        or token.is_currency \
        or token._.is_emoji \
        or '\uFE0F' in token.text \
        or token.lemma_ in stopwords

def get_lemmas(text, stopwords):
    doc = nlp(text)
    return [token.lemma_ for token in doc if not is_unwanted_token(token, stopwords)]

def process(ser, stopwords):
    return ser.apply(lambda x: get_lemmas(x, stopwords))

def get_counts(ser):
    return ser.apply(Counter)

def get_tfs(ser_counts):
    df = pd.json_normalize(ser_counts)
    df = df.fillna(0)
    df = df.set_index(ser_counts.index)
    return df

def get_bag_of_words(ser_counts): #TODO make lowercase & remove repeats
    return set(word for words in ser_counts for word in words)
    
def get_idf(word, ser_counts):
    return log(len(ser_counts) / ser_counts.apply(lambda x: int(word in x)).sum())

def get_idfs(ser_counts):
    words = get_bag_of_words(ser_counts)
    idfs = {word:get_idf(word, ser_counts) for word in words}
    return pd.Series(idfs).rename('idfs')
    
def get_tfidfs(ser_counts):
    tfs = get_tfs(ser_counts)
    idfs = get_idfs(ser_counts)
    return (tfs * idfs).transpose()
    
def write(outpath, df):
    with open(outpath, 'w', newline='', encoding='utf-8') as f:
        df.to_csv(f)

def main():
    inpath, outpath, stopwordspath = parse_input()
    df_tweets = load(inpath)
    stopwords = load_stopwords(stopwordspath)
    ser_docs = combine_topics(df_tweets, '\n\n\n')
    ser_lemmas = process(ser_docs, stopwords)
    ser_counts = get_counts(ser_lemmas)
    df_tfidfs = get_tfidfs(ser_counts)
    write(outpath, df_tfidfs)

if __name__ == '__main__':
    main()