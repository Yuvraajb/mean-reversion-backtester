# 📊 Mean Reversion Backtester

A simple, customizable backtesting framework in Python for testing mean-reversion trading strategies on historical stock price data using `yfinance`.

## 🚀 Features

- RSI-based mean-reversion strategy
- Trade-by-trade analysis
- Realistic entry/exit logic
- Volume filters
- Custom equity curve, drawdown, daily returns visualization
- Cross-stock comparison support
- Performance metrics: Sharpe Ratio, Win Rate, Avg Profit per Trade, etc.

## 🧠 Strategy Overview

This project implements a basic **mean-reversion** strategy:
- **Buy** when the stock is oversold (RSI < threshold)
- **Sell** when it reverts to the mean (RSI > exit threshold or price > moving average)
- Only enter trades when the volume is above its 20-day average

## 📁 Project Structure

```bash
📦 mean-reversion-backtester/
├── data_fetcher.py # Downloads and prepares stock data
├── backtester.py # Core backtesting logic
├── charting.py # Visualization functions
├── analysis.py # Performance evaluation
├── main.py # CLI entry point
├── requirements.txt # Python dependencies
└── README.md # This file

📈 Sample Output
Final portfolio value: $447,026.11
Total profit: $347,026.11
Number of trades: 6
Average profit per trade: $57,837.68
Win rate: 66.67%
Sharpe Ratio: 1.335

🛠️ Installation
git clone https://github.com/your-username/mean-reversion-backtester.git
cd mean-reversion-backtester
pip install -r requirements.txt

🧪 Usage
Edit main.py to change the ticker or tweak strategy logic.
python main.py

You’ll get a menu of charts to view after the simulation runs.
📉 To Do Next
Add support for multiple tickers from a list
Implement train/test split (in progress ✅)
Add support for other strategies (momentum, breakout)
Export trade log as CSV
📚 License
MIT

Built by Yuvraaj Bhatter 👨‍💻

---
