import os.path as op
from os import getcwd
import argparse as ap
import pandas as pd
import spacy


nlp = spacy.load("en_core_web_sm")

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

def process(df):
    df

    
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
    header, rows = load(path)
    write(path, header, rows)



if __name__ == '__main__':
    main()