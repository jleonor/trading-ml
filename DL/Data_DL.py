import pandas as pd
from DL.DL_config import *
import datetime as dt
from urllib import parse
import alpaca_trade_api as tradeapi
from pytrends.request import TrendReq
import snscrape.modules.twitter as sntwitter


def get_historical_data(ticker, exchange, start_date, end_date):
    api = tradeapi.REST(API_KEY, SECRET_KEY, API_BASE_URL, api_version='v2')
    hist_data = api.get_crypto_bars(symbol=ticker,
                                    timeframe=TIMEFRAME_DL,
                                    exchanges=exchange,
                                    limit=10100,
                                    start=start_date,
                                    end=end_date)

    hist_data = hist_data.df.reset_index()
    hist_data = hist_data.drop(['exchange', 'trade_count', 'vwap'], axis=1)
    hist_data = hist_data.rename(columns={'timestamp': 'Date_Time',
                                          'open': 'Open',
                                          'high': 'High',
                                          'low': 'Low',
                                          'close': 'Close',
                                          'volume': 'Volume'})
    return hist_data


def dl_price_data():
    print('Downloading price data...')
    today = str(dt.datetime.today())[:-7]
    for ticker in TICKERS:
        price_df = pd.DataFrame(columns=['Date_Time', 'Open', 'High', 'Low', 'Close', 'Volume'])
        dt_end = dt.datetime.strptime(today, '%Y-%m-%d %H:%M:%S')
        dt_start = dt_end + dt.timedelta(days=-2)
        end_date = dt.datetime.strftime(dt_end, "%Y-%m-%dT%H:%M:%SZ")
        start_date = dt.datetime.strftime(dt_start, "%Y-%m-%dT%H:%M:%SZ")

        while dt_start > dt.datetime(from_year, from_month, from_day):
            # print('DOWNLOADING -----------------------------')
            # print('END_DATE: ' + str(end_date))
            # print('START_DATE: ' + str(start_date))
            data = get_historical_data(ticker, EXCHANGES[0], start_date, end_date)
            dt_end = dt_end + dt.timedelta(days=-2)
            dt_start = dt_end + dt.timedelta(days=-2)
            end_date = dt.datetime.strftime(dt_end, "%Y-%m-%dT%H:%M:%SZ")
            start_date = dt.datetime.strftime(dt_start, "%Y-%m-%dT%H:%M:%SZ")
            price_df = pd.concat([data, price_df]).reset_index(drop=True)

        price_df.to_csv(dl_path + r'\\' + ticker + '_DL_price.csv')


def dl_trends_data():
    print('Downloading trends data...')
    today = dt.datetime.today()
    until_year = int(today.strftime('%Y'))
    until_month = int(today.strftime('%m'))
    until_day = int(today.strftime('%d'))
    until_hour = int(today.strftime(('%H')))

    for ticker in TICKERS:
        keyword = keyword_dict[ticker]
        pytrends = TrendReq(hl='en-US')
        keywords = ['cryptocurrency', 'crypto', keyword]
        trends_df = pytrends.get_historical_interest(keywords,
                                                     from_year,
                                                     from_month,
                                                     from_day,
                                                     0,
                                                     until_year,
                                                     until_month,
                                                     until_day,
                                                     until_hour)

        trends_df = trends_df.reset_index()
        trends_df = trends_df.rename(columns={'date': 'Date_Time',
                                              'cryptocurrency': 'cryptocurrency_trend',
                                              'crypto': 'crypto_trend',
                                              keyword: keyword + '_trend'})
        trends_df.to_csv(dl_path + r'\\' + ticker + '_DL_trends.csv')


def dl_spread_data():  # Bitcoin only
    print('Downloading spread data...')
    for ticker in TICKERS:
        if ticker == 'BTCUSD':
            ABS_2y = pd.read_csv('https://data.bitcoinity.org/export_data.csv?c=e&currency=USD&data_type=spread&f=m10&r=day&st=log&t=l&timespan=2y')
            ABS_30d = pd.read_csv('https://data.bitcoinity.org/export_data.csv?c=e&currency=USD&data_type=spread&r=hour&st=log&t=l&timespan=30d')

            ABS_30d['Time'] = ABS_30d['Time'].str[:-4].astype('datetime64[ns]').dt.strftime('%Y-%m-%d %H:%M:%S')
            ABS_2y['Time'] = ABS_2y['Time'].str[:-4].astype('datetime64[ns]').dt.strftime('%Y-%m-%d %H:%M:%S')

            first_hourly_idx = ABS_30d[ABS_30d['Time'].astype('datetime64[ns]').dt.strftime('%H:%M:%S').astype('str') == '00:00:00'].index.tolist()[0]
            first_hour = ABS_30d.iloc[first_hourly_idx:]['Time'].reset_index(drop=True).iloc[0]
            last_daily_idx = ABS_2y[ABS_2y['Time'] == first_hour].index.tolist()[0]

            ABS_2y = ABS_2y.iloc[:last_daily_idx + 1]
            ABS_30d = ABS_30d.iloc[first_hourly_idx + 1:]

            ABS_df = pd.concat([ABS_2y, ABS_30d])
            ABS_df = ABS_df[['Time', 'coinbase']]
            ABS_df = ABS_df.rename(columns={'Time': 'Date_Time', 'coinbase': 'ABSpread'})
            ABS_df.to_csv(dl_path + r'\\' + ticker + '_DL_spread.csv')


def dl_blockchain_data():
    for ticker in TICKERS:
        if ticker == 'BTCUSD':
            base_url = 'https://api.blockchain.info/charts/'
            params = {'timespan': '1year',
                      'format': 'csv'}
            for chart in BC_charts_list:
                print('Downloading ' + chart + 'data...')
                csv_url = base_url + chart + '?' + parse.urlencode(params)
                BC_data_df = pd.read_csv(csv_url, names=['Date_Time', chart], header=None)
                BC_data_df.to_csv(dl_path + r'\\' + ticker + '_DL_' + chart + '.csv')


def dl_twitter_sentiments():
    end_date = dt.date.today()
    from_date = str(dt.datetime(from_year, from_month, from_day).strftime('%Y-%m-%d'))
    lang = 'lang:en'

    for ticker in TICKERS:
        keyword = keyword_dict[ticker]

        for usernames_list in usernames_dict:
            print('Downloading ' + usernames_list + ' twitter sentiment data...')
            list_name = usernames_list
            df_list = []

            for user in usernames_dict[list_name]:
                search = '"' + keyword + ' ' + lang + ' ' + 'from:' + user + ' ' + 'since:' + from_date + ' ' + 'until:' + str(
                    end_date) + '"'
                scraped_tweets = sntwitter.TwitterSearchScraper(search).get_items()

                try:
                    df_tweets = pd.DataFrame(scraped_tweets)[
                        ['date', 'content', 'media', 'replyCount', 'retweetCount', 'likeCount', 'quoteCount', 'user']]
                    df_list.append(df_tweets)

                except KeyError:
                    pass

            df_all_tweets = pd.concat(df_list)
            df_all_tweets.to_csv(dl_path + r'\\' + ticker + '_DL_' + list_name + '_tweets' + '.csv')


def dl_twitter_whale_alert():
    end_date = dt.date.today()
    from_date = str(dt.datetime(from_year, from_month, from_day).strftime('%Y-%m-%d'))
    lang = 'lang:en'

    for ticker in TICKERS:
        keyword = ticker[:-3]
        print('Downloading twitter whale alert data...')

        search = '"' + '#' + keyword + ' ' + lang + ' ' + 'from:' + 'whale_alert' + ' ' + 'since:' + from_date + ' ' + 'until:' + str(
            end_date) + '"'
        scraped_tweets = sntwitter.TwitterSearchScraper(search).get_items()
        df_tweets = pd.DataFrame(scraped_tweets)[
            ['date', 'content', 'media', 'replyCount', 'retweetCount', 'likeCount', 'quoteCount', 'user']]

        df_tweets.to_csv(dl_path + r'\\' + ticker + '_DL_' + 'whale_alert_tweets' + '.csv')