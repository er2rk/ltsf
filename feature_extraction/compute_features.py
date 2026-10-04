"""
Builds two feature datasets per asset from the same raw big5 data:
    data/indicators/<ASSET>_ti.csv   technical indicators
    data/returns/<ASSET>_ret.csv     percentage returns
Both are cleaned together, so they always cover the exact same dates.

For Technical Indicators:
Using 6 indicators, ones that are simple to understand for a beginner like myself.
For basic return: one day return.
For trend: macd.
For trend strength: aaron.
For momentum: rsi.
For volatility: bollinger bands.
For volume: ad_osc.

https://ta-lib.github.io/ta-lib-python/
https://ta-lib.org/functions/

For Percentage Returns:
For the overnight gap: open_ret.
For the day's highest point: high_ret.
For the day's lowest point: low_ret.
For the day's move: close_ret.
For volume: volume_chg, change in log volume.
"""

from download_data import ASSETS #Specifics for assets.
import numpy as np
import pandas as pd
import talib as ta

def build_indicators(df, use_vol):

    #No indicator requires open right now, keeping it for future.
    #astype(float) to use specifically with talib.
    o, h, l, c, v = (df[col].astype(float) for col in ["Open", "High", "Low", "Close", "Volume"])
    feature_table = pd.DataFrame(index=df.index)

    #Going to be used in LiquidMamba.
    feature_table["close"] = c

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

    return feature_table

def build_returns(df, use_vol):
 
    o, h, l, c, v = (df[col].astype(float) for col in ["Open", "High", "Low", "Close", "Volume"])

    prev_close = c.shift(1)

    feature_table = pd.DataFrame(index=df.index)
 
    #Going to be used in LiquidMamba.
    feature_table["close"] = c
 
    feature_table["open_ret"] = o / prev_close - 1  
    feature_table["high_ret"] = h / prev_close - 1
    feature_table["low_ret"] = l / prev_close - 1
    feature_table["close_ret"] = c / prev_close - 1
 
    if use_vol:
        feature_table["volume_chg"] = np.log1p(v).diff()
 
    return feature_table


if __name__ == "__main__":

    for name, asset in ASSETS.items():
        #May seems redundant to take in dfs at dataload,
        #make them csvs, then read them into dfs again here but i'm just studying.
        df = pd.read_csv(f"data/raw/{name}_big5.csv", index_col="Date", parse_dates=True)

        indicators = build_indicators(df, asset["volume"]).replace([np.inf, -np.inf], np.nan)
        returns = build_returns(df, asset["volume"]).replace([np.inf, -np.inf], np.nan)

        complete = indicators.notna().all(axis=1) & returns.notna().all(axis=1)

        print(f"{name}: {(~complete).sum()} rows dropped, {complete.sum()} kept")

        indicators[complete].to_csv(f"data/indicators/{name}_ti.csv")
        returns[complete].to_csv(f"data/returns/{name}_ret.csv")

        




    













