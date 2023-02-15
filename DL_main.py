from DL.Data_DL import *
from DL.merge_DL_data import merge_dl_data
from DL.add_ta_indicators import add_ta_indicators
from DL.add_target_signal import add_target_signal
from DL.convert_zscores import convert_to_zscores
from DL.tweets_to_sentiment import convert_tweets_to_sentiment
from DL.tweets_to_whale_change import convert_tweets_to_whale_change

dl_price_data()
dl_trends_data()
dl_spread_data()
dl_blockchain_data()
dl_twitter_sentiments()
dl_twitter_whale_alert()
convert_tweets_to_sentiment()
convert_tweets_to_whale_change()

merge_dl_data()
add_ta_indicators()
# add_target_signal()
# convert_to_zscores()

# for ticker in TICKERS:
#     df = pd.read_csv(transform_path + r'\\' + ticker + '_convert_zscores.csv').iloc[:, 1:]
#     print(df)
#     print(df.columns)
