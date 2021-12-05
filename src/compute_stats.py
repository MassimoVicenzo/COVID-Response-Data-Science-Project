import os.path as op
from os import getcwd
import argparse as ap
import json

def parse_input():
    parser = ap.ArgumentParser()
    parser.add_argument('-j', '--jsonfile', required=True)
    parser.add_argument('-d', '--dir', required=True)

    args = parser.parse_args()

    jsonfile_path = op.normpath(op.join(getcwd(), args.jsonfile))
    output_dir = op.normpath(op.join(getcwd(), args.dir))

    with open(jsonfile_path) as f:
        data = dict(json.load(f))

    return data, output_dir

def percentage_tweets(data):
    d = {}
    for cat in data:
        if cat == "total":
            continue
        for subcat in data[cat]:
            d[cat + ' ' + subcat] = round((data[cat][subcat]["count"]/data["total"])*100,1)

    d = dict(sorted(d.items(),key=lambda x : x[1],reverse=True))

    return d

def avg_reception(data, kind):
    d = {}
    for cat in data:
        if cat == "total":
            continue
        for subcat in data[cat]:
            d[cat + ' ' + subcat] = round((data[cat][subcat][f'{kind}_reception']/data[cat][subcat]['count']),2)

    d = dict(sorted(d.items(),key=lambda x : x[1],reverse=True))

    return d

def avg_engagment(data, kind, non_zero):
    d = {}
    for cat in data:
        if cat == "total":
            continue
        for subcat in data[cat]:
            if non_zero:
                d[cat + ' ' + subcat] = round((data[cat][subcat][f'{kind}_sum']/data[cat][subcat][f'{kind}_count']),2)
            else:
                d[cat + ' ' + subcat] = round((data[cat][subcat][f'{kind}_sum']/data[cat][subcat]["count"]),2)


    d = dict(sorted(d.items(),key=lambda x : x[1],reverse=True))

    return d

def avg_reception_score(data):
    d = {}
    for cat in data:
        if cat == "total":
            continue
        for subcat in data[cat]:
            sum = data[cat][subcat]["pos_reception"] - data[cat][subcat]["neg_reception"]
            d[cat + ' ' + subcat] = round((sum/data[cat][subcat]['count']),2)


    d = dict(sorted(d.items(),key=lambda x : x[1],reverse=True))

    return d

def avg_engagment_category(data, kind, non_zero):
    d = {}
    for cat in data:
        sum_kind = 0
        sum = 0
        if cat == "total":
            continue
        for subcat in data[cat]:
            sum_kind += data[cat][subcat][f'{kind}_sum']
            if non_zero:
                sum += data[cat][subcat][f'{kind}_count']
            else:
                sum += data[cat][subcat]['count']
        
        d[cat] = round(sum_kind/sum,2)

    d = dict(sorted(d.items(),key=lambda x : x[1],reverse=True))

    return d

def avg_engagment_content(data, kind, non_zero):
    d = {}
    for subcat in data["scientific"]:
        sum_kind = 0
        sum = 0
        for cat in data:
            if cat == "total":
                continue
            sum_kind += data[cat][subcat][f'{kind}_sum']
            if non_zero:
                sum += data[cat][subcat][f'{kind}_count']
            else:
                sum += data[cat][subcat]['count']
        
        d[subcat] = round(sum_kind/sum,2)

    d = dict(sorted(d.items(),key=lambda x : x[1],reverse=True))

    return d

def avg_reception_category(data, kind):
    d = {}
    for cat in data:
        sum_kind = 0
        sum = 0
        if cat == "total":
            continue
        for subcat in data[cat]:
            sum_kind += data[cat][subcat][f'{kind}_reception']
            sum += data[cat][subcat]['count']
        
        d[cat] = round(sum_kind/sum,2)

    d = dict(sorted(d.items(),key=lambda x : x[1],reverse=True))

    return d

def avg_reception_content(data, kind):
    d = {}
    for subcat in data["scientific"]:
        sum_kind = 0
        sum = 0
        for cat in data:
            if cat == "total":
                continue

            sum_kind += data[cat][subcat][f'{kind}_reception']
            sum += data[cat][subcat]['count']
        
        d[subcat] = round(sum_kind/sum,2)

    d = dict(sorted(d.items(),key=lambda x : x[1],reverse=True))

    return d

def avg_reception_category_score(data):
    d = {}
    for cat in data:
        sum_kind = 0
        sum = 0
        if cat == "total":
            continue
        for subcat in data[cat]:
            sum_kind += data[cat][subcat]["pos_reception"] - data[cat][subcat]["neg_reception"]
            sum += data[cat][subcat]['count']
        
        d[cat] = round(sum_kind/sum,2)

    d = dict(sorted(d.items(),key=lambda x : x[1],reverse=True))

    return d    

def avg_reception_content_score(data):
    d = {}
    for subcat in data["scientific"]:
        sum_kind = 0
        sum = 0
        for cat in data:
            if cat == "total":
                continue
            sum_kind += data[cat][subcat]["pos_reception"] - data[cat][subcat]["neg_reception"]
            sum += data[cat][subcat]['count']
        
        d[subcat] = round(sum_kind/sum,2)

    d = dict(sorted(d.items(),key=lambda x : x[1],reverse=True))

    return d

def output(dic,output_dir,kind):
    with open(op.join(output_dir,f'{kind}.json'),'w') as f:
        json.dump(dic,f,indent=4)


def main():
    data, output_dir = parse_input()
    
    # Computing percentages
    dic = {}
    dic["%_tweets_by_topic"] = percentage_tweets(data)
    output(dic, output_dir, "count_percentages")

    # Computing averages for interactions    
    dic.clear()
    for type_interation in ["like", "reply", "retweet"]:
        dic[f'avg_{type_interation}_by_topic'] = avg_engagment(data, type_interation, False)
        dic[f'avg_{type_interation}_by_topic_non_zero'] = avg_engagment(data, type_interation, True)
    output(dic,output_dir, "interactions")

    # Computing averages for reception
    dic.clear()
    for type_reception in ["pos", "neu", "neg"]:
        dic[f'avg_amount_of_{type_reception}_reception_by_topic'] = avg_reception(data, type_reception)
    dic['avg_reception_by_topic'] = avg_reception_score(data)
    output(dic,output_dir, "reception")

    # Computing interactions for categories
    dic.clear()
    for type_interation in ["like", "reply", "retweet"]:
        dic[f'avg_{type_interation}_by_category'] = avg_engagment_category(data, type_interation, False)
        dic[f'avg_{type_interation}_by_category_non_zero'] = avg_engagment_category(data, type_interation, True)
    output(dic,output_dir, "interactions_categroies")

    # Computing interactions for content
    dic.clear()
    for type_interation in ["like", "reply", "retweet"]:
        dic[f'avg_{type_interation}_by_content'] = avg_engagment_content(data, type_interation, False)
        dic[f'avg_{type_interation}_by_content_non_zero'] = avg_engagment_content(data, type_interation, True)
    output(dic,output_dir, "interactions_content")

    # Computing reception for categories
    dic.clear()
    for type_reception in ["pos", "neu", "neg"]:
        dic[f'avg_amount_of_{type_reception}_reception_by_category'] = avg_reception_category(data, type_reception)
    dic['avg_reception_by_category'] = avg_reception_category_score(data)
    output(dic,output_dir, "reception_categories")
    
    # Computing reception for categories
    dic.clear()
    for type_reception in ["pos", "neu", "neg"]:
        dic[f'avg_amount_of_{type_reception}_reception_by_content'] = avg_reception_content(data, type_reception)
    dic['avg_reception_by_content'] = avg_reception_content_score(data)
    output(dic,output_dir, "reception_content")

    

if __name__ == '__main__':
    main()
    
