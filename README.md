# Data-Science-Project
In November 2021, we scraped tweets on Twitter with the goal of analysing them and determining what factors may be contributing to vaccine hesitancy. In this repository we have all our code and scripts, statistics and results, including words with high Term Frequency - Inverse Document Frequency scores. 

## Installation
`pip install -U pip setuptools wheel`\
`pip install -U spacy`\
`python -m spacy download en_core_web_sm`\
`pip install spacymoji`

## Data
In this folder we have `stopwords.twt`, a file which contains many irrelevant words to our analysis ("the", "of", etc.). We have different csv files, most importantly are `vaccome_tweets.csv` and `vaccome_tweets_annotated.csv` which both contain our sample of 1000 tweets, before and after our hand annotation respectively. The remaining files are contain statistics and numbers needed to compute final results.

## Src
Here we have `gathering_tweets.py` which uses Twitter's API to grap a sample of tweets, which has some restrictions, namely, english original tweets that contained certain keywords. `gather_counts.py` and `compute_stats.py` compute statistics and counts of the tweets based off of the different topics we came up with, these were saved in json files. `describe_topics.py` and `compute_tfidfs.py` dealt with the computation of the Term Frequency - Inverse Document Frequency scores, and what words described our topics the best.

## Results
Here we have the final results stats and counts, organized into different json files. Also we have our full report on this project, which goes through the entire process and our findings in detail.