import pandas as pd

def backtest(df, lookback=50, threshold=2.0, initial_cash=100000):
    # Safety: force Series
    df['price'] = df['price'].astype(float)
    df['volume'] = df['volume'].astype(float)

    # Z-score setup
    df['mean'] = df['price'].rolling(window=lookback).mean()
    df['std'] = df['price'].rolling(window=lookback).std()
    df['z_score'] = (df['price'] - df['mean']) / df['std']

    # Volume filter setup
    df['avg_volume'] = df['volume'].rolling(window=20).mean()

    cash = initial_cash
    shares = 0
    trades = []
    entry_date = None
    entry_price = None
    portfolio_values = []

    for i in range(lookback, len(df)):
        price = df.iloc[i]['price']
        z = df.iloc[i]['z_score']
        volume = df.iloc[i]['volume']
        avg_volume = df.iloc[i]['avg_volume']
        date = df.index[i]

        # Volume condition
        if pd.isna(avg_volume) or volume <= avg_volume:
            continue

        # Buy signal
        if shares == 0 and z < -threshold:
            shares = cash // price
            cash -= shares * price
            entry_date = date
            entry_price = price

        # Sell signal
        elif shares > 0 and z > threshold:
            cash += shares * price
            exit_date = date
            exit_price = price
            profit = (exit_price - entry_price) * shares
            holding_period = (exit_date - entry_date).days

            trades.append({
                'entry_date': entry_date,
                'entry_price': entry_price,
                'exit_date': exit_date,
                'exit_price': exit_price,
                'shares': shares,
                'profit': profit,
                'holding_period': holding_period
            })

            shares = 0
            entry_date = None
            entry_price = None

        # Track portfolio value
        current_value = cash + shares * price
        portfolio_values.append({'date': date, 'value': current_value})

    # Final cleanup if still holding
    if shares > 0:
        exit_date = df.index[-1]
        exit_price = df.iloc[-1]['price']
        profit = (exit_price - entry_price) * shares
        holding_period = (exit_date - entry_date).days
        trades.append({
            'entry_date': entry_date,
            'entry_price': entry_price,
            'exit_date': exit_date,
            'exit_price': exit_price,
            'shares': shares,
            'profit': profit,
            'holding_period': holding_period
        })

    # Ensure final portfolio value is added
    final_value = cash + shares * df.iloc[-1]['price']
    portfolio_values.append({'date': df.index[-1], 'value': final_value})

    trades_df = pd.DataFrame(trades)
    portfolio_series = pd.DataFrame(portfolio_values).set_index('date')

    return trades_df, final_value, portfolio_series
