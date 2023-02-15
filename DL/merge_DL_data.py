import pandas as pd
from DL.DL_config import *
import datetime as dt


def merge_trends(dl_path_ticker, df):
    trends_df = pd.read_csv(dl_path_ticker + '_DL_trends.csv').iloc[:, 1:]
    trends_df = trends_df.drop(['isPartial'], axis=1)
    trends_df['Date_Time'] = pd.to_datetime(
        trends_df['Date_Time'].astype('datetime64[ns]').dt.strftime('%Y-%m-%dT%H:%M:%SZ'))
    trends_df['Date_Time'] = trends_df['Date_Time'].astype(str)
    new_df = pd.merge(df, trends_df, on='Date_Time', how='left').ffill(axis=0)
    return new_df


def merge_spread(dl_path_ticker, df):
    spread_df = pd.read_csv(dl_path_ticker + '_DL_spread.csv').iloc[:, 1:]
    df['Date_Time'] = df['Date_Time'].astype('datetime64[ns]').dt.strftime('%Y-%m-%d %H:%M:%S')
    first_datetime = df['Date_Time'].iloc[0]
    first_date = df['Date_Time'].astype('datetime64[ns]').dt.strftime('%Y-%m-%d').astype('datetime64[ns]').dt.strftime(
        '%Y-%m-%d %H:%M:%S').iloc[0]
    first_daily_idx = spread_df[spread_df['Date_Time'] == first_date].index.tolist()[0]
    spread_df = spread_df.iloc[first_daily_idx:].reset_index(drop=True)
    spread_df.loc[0, 'Date_Time'] = first_datetime
    new_df = pd.merge(df, spread_df, on='Date_Time', how='left').ffill(axis=0)
    return new_df


def merge_blockchain(dl_path_ticker, df):
    for chart in BC_charts_list:
        BC_df = pd.read_csv(dl_path_ticker + '_DL_' + chart + '.csv').iloc[:, 1:]
        BC_df['Date_Time'] = BC_df['Date_Time'].astype('datetime64[ns]').apply(
            lambda x: x.replace(minute=x.minute // 5 * 5)).apply(lambda x: x.replace(second=0))
        BC_df['Date_Time'] = BC_df['Date_Time'].astype('datetime64[ns]').dt.strftime('%Y-%m-%d %H:%M:%S')
        df['Date_Time'] = df['Date_Time'].astype('datetime64[ns]').dt.strftime('%Y-%m-%d %H:%M:%S')
        first_datetime = df['Date_Time'].iloc[0]

        try:
            first_date = \
                df['Date_Time'].astype('datetime64[ns]').dt.strftime('%Y-%m-%d').astype('datetime64[ns]').dt.strftime(
                    '%Y-%m-%d %H:%M:%S').iloc[0]  # %H:%M:%S
            first_daily_idx = BC_df[BC_df['Date_Time'].astype('datetime64[ns]').dt.strftime('%Y-%m-%d').astype(
                'datetime64[ns]').dt.strftime(
                '%Y-%m-%d %H:%M:%S') == first_date].index.tolist()[0]
            BC_df = BC_df.iloc[first_daily_idx:].reset_index(drop=True)

        except IndexError as Exception:
            try:
                first_date = \
                    BC_df['Date_Time'].astype('datetime64[ns]').dt.strftime('%Y-%m-%d').astype(
                        'datetime64[ns]').dt.strftime(
                        '%Y-%m-%d %H:%M:%S').iloc[0]
                first_daily_idx = df[df['Date_Time'].astype('datetime64[ns]').dt.strftime('%Y-%m-%d').astype(
                'datetime64[ns]').dt.strftime(
                '%Y-%m-%d %H:%M:%S') == first_date].index.tolist()[0]
                df = df.iloc[first_daily_idx:].reset_index(drop=True)

            except IndexError as Exception:
                print(Exception)

        BC_df.loc[0, 'Date_Time'] = first_datetime
        df = pd.merge(df, BC_df, on='Date_Time', how='left').ffill(axis=0)

    new_df = df
    return new_df


def merge_sentiment(dl_path_ticker, df):
    for usernames_list in usernames_dict:
        sentiment_df = pd.read_csv(dl_path_ticker + '_DL_' + usernames_list + '_sentiment.csv').iloc[:, 1:]

        if usernames_list == 'crypto_influencers':
            sentiment_df['Date_Time'] = pd.to_datetime(sentiment_df['Date_Time'])
            sentiment_df = sentiment_df.groupby(pd.Grouper(key='Date_Time', freq='2H')).agg({'Date_Time': 'first',
                                                                                             usernames_list + '_retweetCount': 'sum',
                                                                                             usernames_list + '_likeCount': 'sum',
                                                                                             usernames_list + '_base_negative': 'mean',
                                                                                             usernames_list + '_base_neutral': 'mean',
                                                                                             usernames_list + '_base_positive': 'mean',
                                                                                             usernames_list + '_weight': 'mean',
                                                                                             usernames_list + '_weighted_negative': 'mean',
                                                                                             usernames_list + '_weighted_neutral': 'mean',
                                                                                             usernames_list + '_weighted_positive': 'mean'})
            sentiment_df = sentiment_df.drop('Date_Time', axis=1)
            sentiment_df = sentiment_df.reset_index(drop=False)
            sentiment_df['Date_Time'] = sentiment_df['Date_Time'].astype('datetime64[ns]').dt.strftime(
                '%Y-%m-%d %H:%M:%S')

        if usernames_list == 'financial_news':
            sentiment_df['Date_Time'] = pd.to_datetime(sentiment_df['Date_Time'])
            sentiment_df = sentiment_df.groupby(pd.Grouper(key='Date_Time', freq='6H')).agg({'Date_Time': 'first',
                                                                                             usernames_list + '_retweetCount': 'sum',
                                                                                             usernames_list + '_likeCount': 'sum',
                                                                                             usernames_list + '_base_negative': 'mean',
                                                                                             usernames_list + '_base_neutral': 'mean',
                                                                                             usernames_list + '_base_positive': 'mean',
                                                                                             usernames_list + '_weight': 'mean',
                                                                                             usernames_list + '_weighted_negative': 'mean',
                                                                                             usernames_list + '_weighted_neutral': 'mean',
                                                                                             usernames_list + '_weighted_positive': 'mean'})
            sentiment_df = sentiment_df.drop('Date_Time', axis=1)
            sentiment_df = sentiment_df.reset_index(drop=False)
            sentiment_df['Date_Time'] = sentiment_df['Date_Time'].astype('datetime64[ns]').dt.strftime(
                '%Y-%m-%d %H:%M:%S')

        if usernames_list == 'general_news':
            sentiment_df['Date_Time'] = pd.to_datetime(sentiment_df['Date_Time'])
            sentiment_df = sentiment_df.groupby(pd.Grouper(key='Date_Time', freq='1D')).agg({'Date_Time': 'first',
                                                                                             usernames_list + '_retweetCount': 'sum',
                                                                                             usernames_list + '_likeCount': 'sum',
                                                                                             usernames_list + '_base_negative': 'mean',
                                                                                             usernames_list + '_base_neutral': 'mean',
                                                                                             usernames_list + '_base_positive': 'mean',
                                                                                             usernames_list + '_weight': 'mean',
                                                                                             usernames_list + '_weighted_negative': 'mean',
                                                                                             usernames_list + '_weighted_neutral': 'mean',
                                                                                             usernames_list + '_weighted_positive': 'mean'})
            sentiment_df = sentiment_df.drop('Date_Time', axis=1)
            sentiment_df = sentiment_df.reset_index(drop=False)
            sentiment_df['Date_Time'] = sentiment_df['Date_Time'].astype('datetime64[ns]').dt.strftime(
                '%Y-%m-%d %H:%M:%S')

        df['Date_Time'] = df['Date_Time'].astype('datetime64[ns]').dt.strftime('%Y-%m-%d %H:%M:%S')
        df = pd.merge(df, sentiment_df, on='Date_Time', how='left').ffill(axis=0)

    new_df = df
    return new_df


def merge_whale_change(dl_path_ticker, df):
    whale_change_df = pd.read_csv(dl_path_ticker + '_DL_' + 'whale_change.csv').iloc[:, 1:]

    whale_change_df['Date_Time'] = pd.to_datetime(whale_change_df['Date_Time'])
    whale_change_df = whale_change_df.groupby(pd.Grouper(key='Date_Time', freq='5Min')).agg({'Date_Time': 'first',
                                                                                             'BTC_whale_change': 'sum',
                                                                                             'USD_whale_change': 'sum'})
    whale_change_df = whale_change_df.drop('Date_Time', axis=1)
    whale_change_df = whale_change_df.reset_index(drop=False)
    whale_change_df['Date_Time'] = whale_change_df['Date_Time'].astype('datetime64[ns]').dt.strftime(
        '%Y-%m-%d %H:%M:%S')

    df['Date_Time'] = df['Date_Time'].astype('datetime64[ns]').dt.strftime('%Y-%m-%d %H:%M:%S')
    df = pd.merge(df, whale_change_df, on='Date_Time', how='left').ffill(axis=0)

    new_df = df
    return new_df


def merge_dl_data():
    for ticker in TICKERS:
        dl_path_ticker = dl_path + r'\\' + ticker
        price_df = pd.read_csv(dl_path_ticker + '_DL_price.csv').iloc[:, 1:]

        new_df = merge_trends(dl_path_ticker, price_df)
        new_df = merge_spread(dl_path_ticker, new_df)
        new_df = merge_blockchain(dl_path_ticker, new_df)
        new_df = merge_sentiment(dl_path_ticker, new_df)
        new_df = merge_whale_change(dl_path_ticker, new_df)

        new_df.to_csv(transform_path + r'\\' + ticker + '_merged_DL.csv')
