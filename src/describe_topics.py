import os.path as op
from os import getcwd
import argparse as ap
import pandas as pd
from collections import defaultdict
import json



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
        df = pd.read_csv(path, index_col=0)
    return df

def get_top(ser, n):
    return ser.nlargest(n).index.to_list()

def get_tops(df_tfidfs, n):
    return {topic:get_top(df_tfidfs[topic],n) for topic in df_tfidfs.columns}

def short_to_long(short):
    short_to_long0 = {'s':'scientific', 'p':'political', 'e':'economic'}
    short_to_long1 = {'n':"news", 'r':"reaction", 'o':"opinion"}
    return short_to_long0[short[0]], short_to_long1[short[1]]

def unpack(short_tops):
    out = defaultdict(dict)
    for short,top_tfidfs in short_tops.items():
        long0, long1 = short_to_long(short)
        out[long1][long0] = top_tfidfs
    return dict(out)

def write(outpath, dic):
    with open(outpath, 'w', newline='', encoding='utf-8') as f:
        json.dump(dic,f, indent=4, ensure_ascii=False)


def main():
    inpath, outpath = parse_input()
    df_tfidfs = load(inpath)
    tops = get_tops(df_tfidfs, 10)
    tops = unpack(tops)
    write(outpath, tops)

if __name__ == '__main__':
    main()