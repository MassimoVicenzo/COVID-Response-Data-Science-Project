import tweepy as tw
import os.path as op
from os import getcwd
import argparse as ap
import csv
import html

def parse_input():
    parser = ap.ArgumentParser()
    parser.add_argument('-b', '--bearer', required=True)
    parser.add_argument('-k', '--keywords', required=True)
    parser.add_argument('-o', '--output', required=True)
    parser.add_argument('-n', '--number-of-tweets', default=1000)

    args = parser.parse_args()

    keywords_path = path = op.normpath(op.join(getcwd(), args.keywords))
    output_path = op.normpath(op.join(getcwd(), args.output))

    return args.bearer, keywords_path, output_path, int(args.number_of_tweets)

def setup_auth(bearer):
    
    print("Setting up authentication")

    client = tw.Client(bearer_token=bearer, wait_on_rate_limit=True)
    
    print("Authentication finished")

    return client


def collect_keywords(path):
    keywords = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            if line[:2] != '//': 
                keywords.append(line)
    return keywords

def build_query(keywords):
    #Using the keywords array, we will search for them in english non-retweet tweets
    #LIMIT OF 512 CHARACTERS FOR THE BASIC ACCOUNT
    query = ' OR '.join(keywords)
    query = f"({query})"
    query += ' lang:en'
    query += ' -is:quote -is:retweet -is:reply'
    query += ' -England -Britain -UK'
    if len(query) > 512:
        raise ValueError(f"Query of length {len(query)} > 512 too long for api basic account.")
    return query


def collect_tweets(api, keywords, n):

    print("Collecting tweets")

    query = build_query(keywords)
    
    #Currently we are grabbing the id, text, and metrics like replies and likes
    tweets = tw.Paginator(
        api.search_recent_tweets, 
        query=query, 
        max_results=100,
        tweet_fields=["id","text","public_metrics"]
    ).flatten(limit=n)
    
    print("Finished collecting tweets")

    return tweets #generator of tweepy.tweet.Tweet objects

def extract_and_format(tweets, out_path):
    
    print("Extracting pertinant information from tweets")
    
    #Here we grab the information we need from the tweets we scraped
    with open(out_path,'w', newline='',encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['id','text','retweet_count','reply_count','like_count','topic','reception'])
        for tweet in tweets:
            arr = [
                tweet.id, 
                html.unescape(tweet.text),
                tweet.public_metrics['retweet_count'],
                tweet.public_metrics['reply_count'],
                tweet.public_metrics['like_count']
            ]
            writer.writerow(arr)

    print("Outputed CSV file")


def main():
    bearer, keywords_path, out_path, n = parse_input()
    api = setup_auth(bearer)
    keywords = collect_keywords(keywords_path)
    tweets = collect_tweets(api, keywords, n) 
    extract_and_format(tweets, out_path)

if __name__ == '__main__':
    main()