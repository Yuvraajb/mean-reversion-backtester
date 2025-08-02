import numpy as np
import pandas as pd
import yfinance as yf

def calculate_sharpe_ratio(portfolio_series: pd.DataFrame, risk_free_rate: float = 0.03):
    daily_returns = portfolio_series['value'].pct_change().dropna()
    excess_returns = daily_returns - (risk_free_rate / 252)
    sharpe_ratio = np.mean(excess_returns) / np.std(excess_returns)
    return sharpe_ratio * np.sqrt(252)  # Annualized Sharpe

def calculate_daily_returns(portfolio_series: pd.DataFrame):
    return portfolio_series['value'].pct_change().dropna()

def calculate_drawdown(portfolio_series):
    cumulative = portfolio_series['value']
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown


def compare_multiple_stocks(ticker_list, start="2020-01-01", end="2024-12-31"):
    results = []
    for ticker in ticker_list:
        df = yf.download(ticker, start=start, end=end, auto_adjust=True)[['Close']]
        if df.empty:
            continue
        df['returns'] = df['Close'].pct_change()
        total_return = df['Close'].iloc[-1] / df['Close'].iloc[0] - 1
        annualized_return = (1 + total_return) ** (1 / (len(df) / 252)) - 1
        volatility = df['returns'].std() * np.sqrt(252)
        sharpe = (annualized_return - 0.03) / volatility if volatility != 0 else 0
        results.append({
            "Ticker": ticker,
            "Total Return (%)": round(total_return * 100, 2),
            "Annualized Return (%)": round(annualized_return * 100, 2),
            "Volatility (%)": round(volatility * 100, 2),
            "Sharpe Ratio": round(sharpe, 2)
        })

    return pd.DataFrame(results)
