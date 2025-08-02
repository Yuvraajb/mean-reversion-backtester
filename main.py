import matplotlib.pyplot as plt
from data_fetcher import get_data
from backtester.basic_backtest import backtest
from metrics import calculate_sharpe_ratio
from metrics import calculate_daily_returns
from metrics import compare_multiple_stocks
from metrics import calculate_drawdown
import pandas as pd

def show_equity_curve(df, trades_df, ticker):
    plt.figure(figsize=(14, 7))
    plt.plot(df.index, df['price'], label='Price')
    plt.scatter(trades_df['entry_date'], trades_df['entry_price'], marker='^', color='g', label='Buy', s=100)
    plt.scatter(trades_df['exit_date'], trades_df['exit_price'], marker='v', color='r', label='Sell', s=100)
    plt.title(f"{ticker} Mean Reversion Trades")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.tight_layout()
    plt.show()

def show_portfolio_curve(portfolio_series):
    plt.figure(figsize=(14, 6))
    plt.plot(portfolio_series.index, portfolio_series['value'], label='Portfolio Value', color='blue')
    plt.title("Portfolio Value Over Time")
    plt.xlabel("Date")
    plt.ylabel("Portfolio Value ($)")
    plt.legend()
    plt.tight_layout()
    plt.show()

def show_daily_returns(portfolio_series):
    returns = calculate_daily_returns(portfolio_series)
    plt.figure(figsize=(14, 6))
    plt.plot(returns.index, returns.values, label='Daily Returns', color='purple')
    plt.axhline(0, linestyle='--', color='gray')
    plt.title("Daily Returns Over Time")
    plt.xlabel("Date")
    plt.ylabel("Daily Return")
    plt.tight_layout()
    plt.show()

def show_cross_stock_performance():
    tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "TSLA"]
    result_df = compare_multiple_stocks(tickers)
    print("\n=== Per-Stock Performance Comparison ===")
    print(result_df)

def show_chart_menu():
    while True:
        print("\n--- Chart Menu ---")
        print("c - Cross-stock performance comparison")
        print("d - Drawdown chart")
        print("e - Equity curve with buy/sell trades")
        print("r - Daily returns")
        print("q - Quit")


        choice = input("Enter your choice: ").lower()

        if choice == "c":
            show_cross_stock_performance()
        elif choice == "d":
            show_drawdown_chart(portfolio_series_global)
        elif choice == "e":
            run_equity_chart()
        elif choice == "r":
            run_daily_returns_chart()
        elif choice == "q":
            print("Exiting chart viewer.")
            break
        else:
            print("Invalid choice. Try again.")

# These global variables will be used to store data for repeated charting
df_global = None
trades_df_global = None
portfolio_series_global = None
ticker_global = None

def run_equity_chart():
    show_equity_curve(df_global, trades_df_global, ticker_global)

def run_daily_returns_chart():
    show_daily_returns(portfolio_series_global)

def main():
    global df_global, trades_df_global, portfolio_series_global, ticker_global

    ticker = "TSLA"
    initial_cash = 100000
    risk_free_rate = 0.03

    # Fetch and prepare data
    df = get_data(ticker)
    df = df.rename(columns={'Close': 'price'})

    # Backtest
    trades_df, final_portfolio_value, portfolio_series = backtest(df, initial_cash=initial_cash)

    # Save globals for menu use
    df_global = df
    trades_df_global = trades_df
    portfolio_series_global = portfolio_series
    ticker_global = ticker

    # Stats
    print(trades_df.head())
    print(f"\nFinal portfolio value: ${final_portfolio_value:,.2f}")
    print(f"Total profit: ${trades_df['profit'].sum():,.2f}")
    print(f"Number of trades: {len(trades_df)}")
    avg_profit = trades_df['profit'].mean()
    print(f"Average profit per trade: ${avg_profit:,.2f}")
    win_rate = (trades_df['profit'] > 0).mean()
    print(f"Win rate: {win_rate:.2%}")
    sharpe = calculate_sharpe_ratio(portfolio_series, risk_free_rate)
    print(f"Sharpe Ratio: {sharpe:.3f}")

    # Open chart menu
    show_chart_menu()

def show_drawdown_chart(portfolio_series):
    drawdown = calculate_drawdown(portfolio_series)
    plt.figure(figsize=(14, 6))
    plt.plot(drawdown.index, drawdown.values, label='Drawdown', color='red')
    plt.title("Portfolio Drawdown Over Time")
    plt.xlabel("Date")
    plt.ylabel("Drawdown (%)")
    plt.axhline(0, linestyle='--', color='gray')
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
