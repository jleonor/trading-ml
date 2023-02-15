import pandas as pd
from DL.DL_config import *


def convert_to_zscores():
    for ticker in TICKERS:
        df = pd.read_csv(transform_path + r'\\' + ticker + '_added_target.csv').iloc[:, 1:]
        df = df.drop(['peaks', 'valleys'], axis=1)

        df['hi_lo_diff'] = df['High'] - df['Low']
        df['cl_hi_diff'] = df['Close'] - df['High']
        df['cl_lo_diff'] = df['Close'] - df['Low']

        for tframe in TFRAMES:
            df['cl_psar_' + tframe + '_diff'] = df['Close'] - df['PSAR_' + tframe]
            df['cl_obv_' + tframe + '_div'] = df['Close'] / df['OBV_' + tframe].astype(float)

            df = df.drop(['PSAR_' + tframe], axis=1)
            df = df.drop(['OBV_' + tframe], axis=1)

        cols = list(df.columns)
        cols.remove('Date_Time')
        remove_list = ['Date_Time', 'Open', 'High', 'Low', 'Close', 'Volume', 'target_signal']
        cols[:] = (value for value in cols if value not in remove_list)

        # df = df[df['target_signal'] == 1]
        # print(len(df))

        for col in cols:
            col_zscore = col + '_zscore'
            df[col_zscore] = (df[col] - df[col].mean()) / df[col].std(ddof=0)
            # counts = df[col_zscore][df[col_zscore] > 3].value_counts().sum() + df[col_zscore][df[col_zscore] < -3].value_counts().sum()
            # print(col_zscore + ':   ' + str(counts))
            df = df.drop(col, axis=1)
            # print(col)

        for col in df.columns:
            print(col)
        df.to_csv(transform_path + r'\\' + ticker + '_convert_zscores.csv')


