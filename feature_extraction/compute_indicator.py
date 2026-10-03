"""
Using 6 indicators, ones that are simple to understand for a beginner like myself.
For basic return: one day return.
For trend: macd.
For trend strength: aaron.
For momentum: rsi.
For volatility: bollinger bands.
For volume: ad_osc.

https://ta-lib.github.io/ta-lib-python/
https://ta-lib.org/functions/
"""

from download_data import ASSETS #Specifics for assets.
import numpy as np
import pandas as pd
import talib as ta

def build_features(df, use_vol):

    #No indicator requires open right now, keeping it for future.
    #astype(float) to use specifically with talib.
    o, h, l, c, v = (df[col].astype(float) for col in ["Open", "High", "Low", "Close", "Volume"])
    feature_table = pd.DataFrame(index=df.index)

    #1d turns out to be a one dimensional array so, one_day
    feature_table["one_day_return"] = c.pct_change()

    #Keeping the defaults for all indicators.
    macd, _, _ = ta.MACD(c)
    feature_table["macd"] = macd/c

    feature_table["aaron"] = ta.AROONOSC(h, l)
    feature_table["rsi"] = ta.RSI(c)

    upper, middle, lower = ta.BBANDS(c)
    feature_table["bb_width"] = (upper - lower) / middle

    #This one will not be used for forex and brent.
    if use_vol:
        ad_osc = ta.ADOSC(h, l, c, v)
        feature_table["ad_osc"] = ad_osc / ta.SMA(v)

    feature_table = feature_table.replace([np.inf, -np.inf], np.nan) #Replace any infinity with NaN values.

    #Dropping rows with NaN.
    feature_table = feature_table.dropna()
    print(f"{len(df) - len(feature_table)} rows dropped")

    return feature_table

if __name__ == "__main__":

    for name, asset in ASSETS.items():
        #May seems redundant to take in dfs at dataload,
        #make them csvs, then read them into dfs again here but i'm just studying.
        df = pd.read_csv(f"data/{name}.csv", index_col="Date", parse_dates=True)
        features = build_features(df, asset["volume"])
        features.to_csv(f"feature/{name}.csv")




    













