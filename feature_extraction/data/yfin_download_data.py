"""
Assets to be used in feature extraction via technical analysis.
A little explanation for myself in the future.
Two stocks. Bank of China is a stable asset. Nvidia, a volatile one, especially with the AI advancements.
Two ETFs. SPY to use with stocks, XLE to use with the oil commodity.
Two FOREXs. EURUSD is relatively stable. EURTRY for fun, it never goes down :D.
BRENT as a commodity.
TLT as a bond.
BTC as cryptocurrency.

Check these for yfinance API.
https://pythonfintech.com/articles/how-to-download-market-data-yfinance-python/
https://ranaroussi.github.io/yfinance/reference/api/yfinance.download.html
"""

ASSETS = {
    "BOC": {
        "ticker": "601988.SS",
        "name": "Bank of China (Shanghai Exchange)",
        "asset_class": "stock"
    },
    "NVDA": {
        "ticker": "NVDA",
        "name": "NVIDIA",
        "asset_class": "stock"
    },
    "SPY": {
        "ticker": "SPY",
        "name": "S&P 500 ETF",
        "asset_class": "etf"
    },
    "XLE": {
        "ticker": "XLE",
        "name": "Energy Select Sector SPDR ETF",
        "asset_class": "etf"
    },
    "EURUSD": {
        "ticker": "EURUSD=X",
        "name": "EUR/USD",
        "asset_class": "forex"
    },
    "EURTRY": {
        "ticker": "EURTRY=X",
        "name": "EUR/TRY",
        "asset_class": "forex"
    },
    "BRENT": {
        "ticker": "BZ=F",
        "name": "Brent crude oil futures (continuous)",
        "asset_class": "commodity",
        "notes": "Continuous front-month contract: roll jumps, volume mixes contracts."
    },
    "TLT": {
        "ticker": "TLT",
        "name": "iShares 20+ Year Treasury Bond ETF",
        "asset_class": "bond"
    },
    "BTC": {
        "ticker": "BTC-USD",
        "name": "Bitcoin",
        "asset_class": "crypto"
    }
}

#We'll use the config later on during feature extraction.
if __name__ == "__main__":

    import yfinance as yf

    for name, asset in ASSETS.items():
    
        df = yf.download(tickers=asset["ticker"], period="max", interval="1d", multi_level_index=False, auto_adjust=True)
        if df.empty:
            print(f"No data for: {name}. Going through with the rest.")
            continue
        df.to_csv(f"{name}.csv")
