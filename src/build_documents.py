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

    args = parser.parse_args()

    inpath = op.normpath(op.join(getcwd(), args.inpath))
    outpath = op.normpath(op.join(getcwd(), args.outpath))

    return inpath, outpath

def load(path):
    with open(path, 'r', encoding='utf-8') as f:
        df = pd.read_csv(path)
    return df

def combine_topics(df, sep):
    groups = df.groupby(['topic'])
    df['document'] = df.groupby(['topic'])['text'].transform(lambda x: sep.join(x))
    df2 = df[['topic', 'document']].drop_duplicates().set_index('topic')
    return df2['document']
    

def is_unwanted_token(token):
    return token.is_space \
        or token.is_stop \
        or token.is_punct \
        or token.like_num \
        or token.like_url \
        or token.like_email \
        or token.is_currency

def get_lemmas(text):
    doc = nlp(text)
    return [word.lemma_ for word in doc if not is_unwanted_token(word)]

def process(ser):
    return ser.apply(get_lemmas)

def get_tfs(ser):
    return ser.apply(Counter)

def get_all_words(lists_of_words):
    raise NotImplementedError
    
def get_idf(word, ser):
    return log(len(ser) / ser.apply(lambda x: int(word in x)).sum())

def get_bag_of_words(ser):
    return set(word for words in ser for word in words)

def get_idfs(word, ser):
    words = get_bag_of_words(ser)
    
list(zip(*aaah.items()))


    
def write(path, header, rows):
    with open(path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for row in rows:
            text = row[1]
            text = '\n'.join(text.splitlines())
            writer.writerow(row[:1] + [text] + row[2:])

def main():
    inpath, outpath = parse_input()
    df_tweets = load(inpath)
    ser_docs = combine_topics(df_tweets, '\n\n\n')
    process(ser)



if __name__ == '__main__':
    main()