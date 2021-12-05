import os.path as op
from os import getcwd
import argparse as ap
import pandas as pd
import json

THINGS_TO_COUNT = ["count","retweet_count","reply_count","like_count","retweet_sum","reply_sum",
                   "like_sum","pos_reception", "neu_reception", "neg_reception"]

def parse_input():
    parser = ap.ArgumentParser()
    parser.add_argument('-c', '--csvfile', required=True)
    parser.add_argument('-o', '--output', required=True)

    args = parser.parse_args()

    csvfile_path = op.normpath(op.join(getcwd(), args.csvfile))
    output_path = op.normpath(op.join(getcwd(), args.output))

    csv_data = pd.read_csv(csvfile_path)

    return csv_data, output_path

def get_counts(data):
    dic = {}
    dic["total"] = int(data["id"].count())
    for category in ["scientific","political","economical"]:

        dic[category] = {}

        for subcategory in ["news","reaction","opinion"]:

            subframe = data[data["topic"] == f'{category[0]}{subcategory[0]}']
            dic[category][subcategory] = {}

            for thing_to_count in THINGS_TO_COUNT:
                dic[category][subcategory][thing_to_count] = int(tweet_count(subframe,thing_to_count))

    return dic

def tweet_count(data,query):
    if query == "count":
        return data["id"].count()
    
    elif query[-5:] == "count":
        return data.loc[data[f'{query[:-5]}count'] != 0, "id"].count()
    
    elif query[-3:] == "sum":
        return data[f'{query[:-3]}count'].sum()
    
    else:
        if query[:3] == "pos":
            return data.loc[data["reception"] == 1, "id"].count()
        
        elif query[:3] == "neu":
            return data.loc[data["reception"] == 0, "id"].count() 
        
        elif query[:3] == "neg":
            return data.loc[data["reception"] == -1, "id"].count()         

def output(output, dic):    
    with open(output,'w') as f:
        json.dump(dic,f,indent=4)

def main():
    dataframe, output_path = parse_input()
    dic = get_counts(dataframe)
    output(output_path, dic)

if __name__ == '__main__':
    main()
    
