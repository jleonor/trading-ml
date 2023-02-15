import pandas as pd
from DL.DL_config import *


def convert_tweets_to_whale_change():
    print('Converting whale tweets...')

    for ticker in TICKERS:
        tick = ticker[:-3]
        dl_path_ticker = dl_path + r'\\' + ticker
        df = pd.read_csv(dl_path_ticker + '_DL_' + 'whale_alert_tweets.csv').iloc[:, 1:]
        df = df[['date', 'content']]
        df = df.rename(columns={'content': 'Text'})

        # FROM https://github.com/dorienh/bitcoin_synthesizer/blob/main/parsing_script/merge_wtoe_etow.ipynb
        df = df[df['Text'].str.contains(r'^(?=.*#' + tick + ')')]
        df["Text"] = df["Text"].replace(r'http\S+', '', regex=True)     # remove url
        df["Text"] = df["Text"].replace(r'\n', '', regex=True)          # remove new lines
        df["Text"] = df["Text"].replace(',', '', regex=True)            # remove commas
        df["Text"] = df["Text"].replace('USD', '', regex=True)          # remove USD to allow taking of numbers in brackets
        df["Text"] = df["Text"].replace('Tx:', '', regex=True)          # idk whats this
        df["Text"] = df["Text"].replace('To:', '', regex=True)          # remove to
        df["kw_check"] = df["Text"].str.extract(r'(\w*?)\s*\(')
        df = df[df["kw_check"] == "BTC"]
        df['BTC'] = df["Text"].str.extract(r'(\S+?) #' + tick)
        df['USD'] = df["Text"].str.extract(r'\((.*?)\)')
        df['USD'] = df['USD'].str.replace('[^0-9]', '', regex=True)
        df['Source'] = df["Text"].str.extract(r"from(.*?)to")
        df['Source'] = df['Source'].str.lower()
        df['Destination'] = df["Text"].str.extract(r'(?<=to )(.*)')
        df['Destination'] = df['Destination'].str.lower()
        df["transferred"] = df["Text"].str.extract(r'(\S+?) from')
        df["scam"] = df["Text"].str.contains("scam")
        df["stolen"] = df["Text"].str.contains("stolen")
        df = df[(df['scam'] == False) & (df['stolen'] == False)]

        wtoe = df[(df['Source'].str.contains("unknown", na=False))]      # Wallet to exchange
        etow = df[(df['Destination'].str.contains("unknown", na=False))] # Exchange to wallet

        wtoe['Destination'] = wtoe['Destination'].str.rstrip()
        wtoe = wtoe[wtoe['Destination'] != "unknown wallet"]

        etow['Source'] = etow['Source'].str.rstrip()
        etow['Source'] = etow['Source'].str.lstrip()
        # etow[etow['Destination'] != "unknown walletℹ️ the coins in this transaction were mined in the first month of bitcoin's existence. "]
        etow = etow[etow['Source'] != "unknown wallet"]

        # FROM https://github.com/dorienh/bitcoin_synthesizer/blob/main/parsing_script/merge_wtoe_etow.ipynb
        df_etow = etow[['date', tick, 'USD']]
        df_etow[tick + '_whale_change'] = df_etow[tick] * 1
        df_etow['USD_whale_change'] = df_etow['USD'] * 1

        df_wtoe = wtoe[['date', tick, 'USD']]
        df_wtoe[tick + '_whale_change'] = df_wtoe[tick] * (-1)
        df_wtoe['USD_whale_change'] = df_wtoe['USD'] * (-1)
        df = pd.concat([df_etow, df_wtoe], ignore_index=True, sort=False)
        df = df.rename(columns={'date': 'Date_Time'})
        df = df[['Date_Time', tick + '_whale_change', 'USD_whale_change']]

        df.to_csv(dl_path_ticker + '_DL_' + 'whale_change.csv')
