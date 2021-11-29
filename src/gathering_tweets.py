import tweepy as tw
import os.path as op
from os import getcwd
import argparse as ap
import csv
import html

#Change this list if you want to look for different words
KEYWORDS = ["vaccine","vaccination","COVID","pandemic","outbreak","virus","Pfizer","BioNTech","Moderna"]

def parse_input():
    parser = ap.ArgumentParser()
    parser.add_argument('-b', '--bearer', required=True)
    parser.add_argument('-o', '--output', required=True)

    args = parser.parse_args()

    output_path = op.normpath(op.join(getcwd(), args.output))

    return args.bearer, output_path

def setup_auth(bearer):
    
    print("Setting up authentication")

    client = tw.Client(bearer_token=bearer, wait_on_rate_limit=True)
    
    print("Authentication finished")

    return client

def collect_tweets(api):

    print("Collecting tweets")

    #Using the keywords array, we search for them in english non-retweet tweets
    query = " lang:en -is:retweet -is:reply"
    query = '(' + ' OR '.join(KEYWORDS) + ')' + query #LIMIT OF 512 CHARACTERS FOR THE BASIC ACCOUNT
    
    #Currently we are grabbing the id, text, and metrics like replies and likes
    tweets = tw.Paginator(
        api.search_recent_tweets, 
        query=query, 
        max_results=100,
        tweet_fields=["id","text","public_metrics"]
    ).flatten(limit=1000)
    
    print("Finished collecting tweets")

    return tweets #generator of tweepy.tweet.Tweet objects

def extract_and_format(tweets, out_path):
    
    print("Extracting pertinant information from tweets")
    
    #Here we grab the information we need from the tweets we scraped
    with open(out_path,'w', newline='',encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(['id','text','retweet_count','reply_count','like_count'])
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
    bearer, out_path = parse_input()
    api = setup_auth(bearer)
    tweets = collect_tweets(api) 
    extract_and_format(tweets, out_path)

if __name__ == '__main__':
    main()