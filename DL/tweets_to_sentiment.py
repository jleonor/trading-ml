from transformers import AutoTokenizer, AutoModelForSequenceClassification
from scipy.special import softmax
import pandas as pd
from DL.DL_config import *

roberta = 'cardiffnlp/twitter-roberta-base-sentiment'
model = AutoModelForSequenceClassification.from_pretrained(roberta)
tokenizer = AutoTokenizer.from_pretrained(roberta)


def process(tweet):
    tweet_words = []
    for word in tweet.split(' '):
        if word.startswith('@') and len(word) > 1:
            word = '@user'

        elif word.startswith('http'):
            word = 'http'

        tweet_words.append(word)

    tweet_proc = ' '.join(tweet_words)
    return tweet_proc


def encode_tweet(tweet_proc):
    encoded_tweet = tokenizer(tweet_proc, return_tensors='pt')
    output = model(**encoded_tweet)
    scores = output[0][0].detach().numpy()
    scores = softmax(scores)

    return scores


def convert_tweets_to_sentiment():
    print('Converting tweets to sentiment scores...')
    for ticker in TICKERS:
        dl_path_ticker = dl_path + r'\\' + ticker
        for usernames_list in usernames_dict:
            tweets_df = pd.read_csv(dl_path_ticker + '_DL_' + usernames_list + '_tweets.csv').iloc[:, 1:]
            df = tweets_df[['date', 'content', 'retweetCount', 'likeCount']]

            tweets = []
            for i in df['content']:
                tweet = i.replace('&amp;', '&')
                tweet_proc = process(tweet)
                tweets.append(tweet_proc)

            df = df.assign(tweets_proc=tweets)
            df = df[['date', 'tweets_proc', 'retweetCount', 'likeCount']]
            df = df.groupby('tweets_proc').agg({'date': 'first',
                                                'tweets_proc': 'first',
                                                'retweetCount': 'sum',
                                                'likeCount': 'sum'})
            df = df.reset_index(drop=True)

            negative = []
            neutral = []
            positive = []

            for i in df['tweets_proc']:
                scores = encode_tweet(i)

                neg_score = scores[0]
                neu_score = scores[1]
                pos_score = scores[2]

                negative.append(neg_score)
                neutral.append(neu_score)
                positive.append(pos_score)

            df['base_negative'] = negative
            df['base_neutral'] = neutral
            df['base_positive'] = positive

            df['weight'] = 1 + ((df['retweetCount'] * df['likeCount'])/100)
            df['weighted_negative'] = df['weight'] * df['base_negative']
            df['weighted_neutral'] = df['weight'] * df['base_neutral']
            df['weighted_positive'] = df['weight'] * df['base_positive']

            df = df.drop(['tweets_proc'], axis=1)
            df = df.reset_index(drop=True)
            df = df.sort_values(by="date")
            df = df.add_prefix(usernames_list + '_')
            df = df.rename(columns={usernames_list + '_date': 'Date_Time'})
            df.to_csv(dl_path_ticker + '_DL_' + usernames_list + '_sentiment.csv')