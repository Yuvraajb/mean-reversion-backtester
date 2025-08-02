import pandas as pd

def generate_signals(df: pd.DataFrame, lookback: int = 20, entry_z: float = 1.5):
    print("Incoming df columns/types:", list(df.columns),
          {c: type(df[c]) for c in df.columns})
    df = df.copy()
    df['mean'] = df['price'].rolling(window=lookback).mean()
    df['std']  = df['price'].rolling(window=lookback).std()
    df['z_score'] = (df['price'] - df['mean']) / df['std']

    # Generate positions
    df['position'] = 0
    df.loc[df['z_score'] < -entry_z, 'position'] = 1
    df.loc[df['z_score'] >  entry_z, 'position'] = -1
    df.loc[df['z_score'].abs() < 0.5, 'position'] = 0

    return df
