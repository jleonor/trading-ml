import pandas as pd
from DL.DL_config import *
import talib as ta


def convert_df_by_timeframe(df, timeframe):
    df.Date_Time = pd.to_datetime(df.Date_Time, format='%Y-%m-%d %H:%M')
    df = df.set_index('Date_Time')
    new_df = df.groupby(pd.Grouper(freq=timeframe)).agg({'Open': 'first',
                                                         'High': 'max',
                                                         'Low': 'min',
                                                         'Close': 'last',
                                                         'Volume': 'sum'})
    new_df = new_df.reset_index()
    return new_df


def add_ta_indicators():
    for ticker in TICKERS:
        df = pd.read_csv(transform_path + r'\\' + ticker + '_merged_DL.csv').iloc[:, 1:]
        df_timeframes_list = []

        for timeframe in TFRAMES:
            df_tf = convert_df_by_timeframe(df, timeframe)
            df_tf = df_tf.dropna()

            op = df_tf['Open'].values
            hi = df_tf['High'].values
            lo = df_tf['Low'].values
            cl = df_tf['Close'].values
            vo = df_tf['Volume'].values

            df_tf['NATR_' + timeframe] = ta.NATR(hi, lo, cl)
            df_tf['ADX_' + timeframe] = ta.ADX(hi, lo, cl)
            df_tf['PSAR_' + timeframe] = ta.SAR(hi, lo)
            df_tf['OBV_' + timeframe] = ta.OBV(cl, vo)

            df_tf['RSI_' + timeframe] = ta.RSI(cl)
            df_tf['CCI_' + timeframe] = ta.CCI(hi, lo, cl)
            df_tf['DX_' + timeframe] = ta.DX(hi, lo, cl)
            df_tf['MFI_' + timeframe] = ta.MFI(hi, lo, cl, vo)
            df_tf['APO_' + timeframe] = ta.APO(cl)
            df_tf['AROONOSC_' + timeframe] = ta.AROONOSC(hi, lo)
            df_tf['CMO_' + timeframe] = ta.CMO(cl)
            df_tf['PPO_' + timeframe] = ta.PPO(cl)
            df_tf['ULTOSC_' + timeframe] = ta.ULTOSC(hi, lo, cl)
            df_tf['ADOSC_' + timeframe] = ta.ADOSC(hi, lo, cl, vo)

            df_tf['CDL2CROWS_' + timeframe] = ta.CDL2CROWS(op, hi, lo, cl)
            df_tf['CDL3BLACKCROWS_' + timeframe] = ta.CDL3BLACKCROWS(op, hi, lo, cl)
            df_tf['CDL3INSIDE_' + timeframe] = ta.CDL3INSIDE(op, hi, lo, cl)
            df_tf['CDL3LINESTRIKE_' + timeframe] = ta.CDL3LINESTRIKE(op, hi, lo, cl)
            df_tf['CDL3OUTSIDE_' + timeframe] = ta.CDL3OUTSIDE(op, hi, lo, cl)
            df_tf['CDL3STARSINSOUTH_' + timeframe] = ta.CDL3STARSINSOUTH(op, hi, lo, cl)
            df_tf['CDL3WHITESOLDIERS_' + timeframe] = ta.CDL3WHITESOLDIERS(op, hi, lo, cl)
            df_tf['CDLABANDONEDBABY_' + timeframe] = ta.CDLABANDONEDBABY(op, hi, lo, cl)
            df_tf['CDLADVANCEBLOCK_' + timeframe] = ta.CDLADVANCEBLOCK(op, hi, lo, cl)
            df_tf['CDLBELTHOLD_' + timeframe] = ta.CDLBELTHOLD(op, hi, lo, cl)
            df_tf['CDLBREAKAWAY_' + timeframe] = ta.CDLBREAKAWAY(op, hi, lo, cl)
            df_tf['CDLCLOSINGMARUBOZU_' + timeframe] = ta.CDLCLOSINGMARUBOZU(op, hi, lo, cl)
            df_tf['CDLCONCEALBABYSWALL_' + timeframe] = ta.CDLCONCEALBABYSWALL(op, hi, lo, cl)
            df_tf['CDLCOUNTERATTACK_' + timeframe] = ta.CDLCOUNTERATTACK(op, hi, lo, cl)
            df_tf['CDLDARKCLOUDCOVER_' + timeframe] = ta.CDLDARKCLOUDCOVER(op, hi, lo, cl)
            df_tf['CDLDOJI_' + timeframe] = ta.CDLDOJI(op, hi, lo, cl)
            df_tf['CDLDOJISTAR_' + timeframe] = ta.CDLDOJISTAR(op, hi, lo, cl)
            df_tf['CDLDRAGONFLYDOJI_' + timeframe] = ta.CDLDRAGONFLYDOJI(op, hi, lo, cl)
            df_tf['CDLENGULFING_' + timeframe] = ta.CDLENGULFING(op, hi, lo, cl)
            df_tf['CDLEVENINGDOJISTAR_' + timeframe] = ta.CDLEVENINGDOJISTAR(op, hi, lo, cl)
            df_tf['CDLEVENINGSTAR_' + timeframe] = ta.CDLEVENINGSTAR(op, hi, lo, cl)
            df_tf['CDLGAPSIDESIDEWHITE_' + timeframe] = ta.CDLGAPSIDESIDEWHITE(op, hi, lo, cl)
            df_tf['CDLGRAVESTONEDOJI_' + timeframe] = ta.CDLGRAVESTONEDOJI(op, hi, lo, cl)
            df_tf['CDLHAMMER_' + timeframe] = ta.CDLHAMMER(op, hi, lo, cl)
            df_tf['CDLHANGINGMAN_' + timeframe] = ta.CDLHANGINGMAN(op, hi, lo, cl)
            df_tf['CDLHARAMI_' + timeframe] = ta.CDLHARAMI(op, hi, lo, cl)
            df_tf['CDLHARAMICROSS_' + timeframe] = ta.CDLHARAMICROSS(op, hi, lo, cl)
            df_tf['CDLHIGHWAVE_' + timeframe] = ta.CDLHIGHWAVE(op, hi, lo, cl)
            df_tf['CDLHIKKAKEMOD_' + timeframe] = ta.CDLHIKKAKEMOD(op, hi, lo, cl)
            df_tf['CDLHOMINGPIGEON_' + timeframe] = ta.CDLHOMINGPIGEON(op, hi, lo, cl)
            df_tf['CDLIDENTICAL3CROWS_' + timeframe] = ta.CDLIDENTICAL3CROWS(op, hi, lo, cl)
            df_tf['CDLINNECK_' + timeframe] = ta.CDLINNECK(op, hi, lo, cl)
            df_tf['CDLINVERTEDHAMMER_' + timeframe] = ta.CDLINVERTEDHAMMER(op, hi, lo, cl)
            df_tf['CDLKICKING_' + timeframe] = ta.CDLKICKING(op, hi, lo, cl)
            df_tf['CDLKICKINGBYLENGTH_' + timeframe] = ta.CDLKICKINGBYLENGTH(op, hi, lo, cl)
            df_tf['CDLLADDERBOTTOM_' + timeframe] = ta.CDLLADDERBOTTOM(op, hi, lo, cl)
            df_tf['CDLLONGLEGGEDDOJI_' + timeframe] = ta.CDLLONGLEGGEDDOJI(op, hi, lo, cl)
            df_tf['CDLLONGLINE_' + timeframe] = ta.CDLLONGLINE(op, hi, lo, cl)
            df_tf['CDLMARUBOZU_' + timeframe] = ta.CDLMARUBOZU(op, hi, lo, cl)
            df_tf['CDLMATCHINGLOW_' + timeframe] = ta.CDLMATCHINGLOW(op, hi, lo, cl)
            df_tf['CDLMATHOLD_' + timeframe] = ta.CDLMATHOLD(op, hi, lo, cl)
            df_tf['CDLMORNINGDOJISTAR_' + timeframe] = ta.CDLMORNINGDOJISTAR(op, hi, lo, cl)
            df_tf['CDLMORNINGSTAR_' + timeframe] = ta.CDLMORNINGSTAR(op, hi, lo, cl)
            df_tf['CDLONNECK_' + timeframe] = ta.CDLONNECK(op, hi, lo, cl)
            df_tf['CDLPIERCING_' + timeframe] = ta.CDLPIERCING(op, hi, lo, cl)
            df_tf['CDLRICKSHAWMAN_' + timeframe] = ta.CDLRICKSHAWMAN(op, hi, lo, cl)
            df_tf['CDLRISEFALL3METHODS_' + timeframe] = ta.CDLRISEFALL3METHODS(op, hi, lo, cl)
            df_tf['CDLSEPARATINGLINES_' + timeframe] = ta.CDLSEPARATINGLINES(op, hi, lo, cl)
            df_tf['CDLSHOOTINGSTAR_' + timeframe] = ta.CDLSHOOTINGSTAR(op, hi, lo, cl)
            df_tf['CDLSHORTLINE_' + timeframe] = ta.CDLSHORTLINE(op, hi, lo, cl)
            df_tf['CDLSPINNINGTOP_' + timeframe] = ta.CDLSPINNINGTOP(op, hi, lo, cl)
            df_tf['CDLSTALLEDPATTERN_' + timeframe] = ta.CDLSTALLEDPATTERN(op, hi, lo, cl)
            df_tf['CDLSTICKSANDWICH_' + timeframe] = ta.CDLSTICKSANDWICH(op, hi, lo, cl)
            df_tf['CDLTAKURI_' + timeframe] = ta.CDLTAKURI(op, hi, lo, cl)
            df_tf['CDLTASUKIGAP_' + timeframe] = ta.CDLTASUKIGAP(op, hi, lo, cl)
            df_tf['CDLTHRUSTING_' + timeframe] = ta.CDLTHRUSTING(op, hi, lo, cl)
            df_tf['CDLTRISTAR_' + timeframe] = ta.CDLTRISTAR(op, hi, lo, cl)
            df_tf['CDLUNIQUE3RIVER_' + timeframe] = ta.CDLUNIQUE3RIVER(op, hi, lo, cl)
            df_tf['CDLUPSIDEGAP2CROWS_' + timeframe] = ta.CDLUPSIDEGAP2CROWS(op, hi, lo, cl)
            df_tf['CDLXSIDEGAP3METHODS_' + timeframe] = ta.CDLXSIDEGAP3METHODS(op, hi, lo, cl)

            df_tf = df_tf.drop(['Open', 'High', 'Low', 'Close', 'Volume'], axis=1)

            df_timeframes_list.append(df_tf)

        new_df = df_timeframes_list[0]
        for idx in range(len(df_timeframes_list)):
            if idx != 0:
                new_df = pd.merge(new_df, df_timeframes_list[idx], on='Date_Time', how='left')
                new_df.columns = new_df.columns.str.replace('_x', '')

                for col in new_df.columns:
                    if '_y' in col:
                        new_df = new_df.drop([col], axis=1)
        new_df = new_df.ffill(axis=0)
        new_df = pd.merge(df, new_df, on='Date_Time', how='left')
        new_df.to_csv(transform_path + r'\\' + ticker + '_added_ta_indicators.csv')

