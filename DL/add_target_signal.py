import pandas as pd
from scipy.signal import find_peaks
from DL.DL_config import *
import numpy as np
import vectorbt as vbt

prominence = 5
distance = 30
width = 10


def add_target_signal():
    for ticker in TICKERS:
        df = pd.read_csv(transform_path + r'\\' + ticker + '_added_ta_indicators.csv').iloc[:, 1:]

        peaks, _ = find_peaks(df['Close'], prominence=prominence, distance=distance, width=width)
        valleys, _ = find_peaks(-df['Close'], prominence=prominence, distance=distance, width=width)

        df['target_signal'] = np.nan
        df['target_signal'] = np.where(df.index.isin(peaks), -1, df['target_signal'])
        df['target_signal'] = np.where(df.index.isin(valleys), 1, df['target_signal'])
        df['target_signal'] = df['target_signal'].ffill()

        df['target_signal_shifted'] = df['target_signal'].shift(1)
        df['target_signal'] = df['target_signal'].where(df['target_signal'] != df['target_signal_shifted'], 0)
        df['peaks'] = df[df['target_signal'] == -1]['target_signal']
        df['valleys'] = df[df['target_signal'] == 1]['target_signal']

        df = df.drop(columns=['target_signal_shifted'])
        df.to_csv(transform_path + r'\\' + ticker + '_added_target.csv')
        print(df['target_signal'].value_counts())

        # Check performance with transaction fee
        close = df.set_index('Date_Time').get('Close').astype(float)
        peaks = df.set_index('Date_Time').get('peaks').astype(float)
        valleys = df.set_index('Date_Time').get('valleys').astype(float)

        entries = np.where(valleys == 1, True, False)
        exits = np.where(peaks == -1, True, False)
        pf = vbt.Portfolio.from_signals(close, entries, exits, init_cash=1000, fees=0.0035)

        print(pf.stats())
        pf.plot().show()
