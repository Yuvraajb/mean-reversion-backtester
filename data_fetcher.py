# data_fetcher.py

import yfinance as yf

def get_data(ticker: str, start: str = "2020-01-01", end: str = "2024-12-31"):
    raw = yf.download(ticker, start=start, end=end, auto_adjust=True)

    # Select only Close and Volume
    df = raw[['Close', 'Volume']].copy()
    df.columns = ['price', 'volume']

    # Add 20-day average volume
    df['avg_volume_20d'] = df['volume'].rolling(window=20).mean()

    return df
