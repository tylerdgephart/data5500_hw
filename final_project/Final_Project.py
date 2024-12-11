import alpaca_trade_api as tradeapi
import pandas as pd
import numpy as np
import json
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# Authentication and connection details
api_key = 'PKMM2FHADY54UU72SUH8'
api_secret = 'JhgvRu6qd1aBIY6KbUegsFV9ePFavuHvtfCt436c'
base_url = 'https://paper-api.alpaca.markets'

# Instantiate REST API
api = tradeapi.REST(api_key, api_secret, base_url, api_version='v2')

# Fetch stock data from Alpaca
def fetch_stock_data(symbol, start_date, end_date):
    bars = api.get_bars(symbol, tradeapi.TimeFrame.Day, start=start_date, end=end_date).df
    return bars

# Function to save stock data to CSV
def save_stock_data_to_csv(symbol, data):
    # Get the directory where the script is located
    script_directory = os.path.dirname(os.path.abspath(__file__))
    
    # Define the path for the 'data' folder in the same directory
    data_directory = os.path.join(script_directory, 'data')
    
    # Ensure the data directory exists
    if not os.path.exists(data_directory):
        os.makedirs(data_directory)
    
    # Save data to the CSV file in the correct folder
    data.to_csv(os.path.join(data_directory, f"{symbol}_data.csv"), mode='a', header=False)

# Define trading strategy functions (mean reversion, SMA, normal distribution)
def mean_reversion_strategy(data, window=20, z_score_threshold=2):
    data['rolling_mean'] = data['close'].rolling(window=window).mean()
    data['rolling_std'] = data['close'].rolling(window=window).std()
    data['z_score'] = (data['close'] - data['rolling_mean']) / data['rolling_std']
    
    # Mean reversion: Buy when z-score is below -2, sell when it's above 2
    data['signal'] = 0
    data.loc[data['z_score'] < -z_score_threshold, 'signal'] = 1  # Buy signal
    data.loc[data['z_score'] > z_score_threshold, 'signal'] = -1  # Sell signal
    return data

def sma_strategy(data, short_window=50, long_window=200):
    data['short_sma'] = data['close'].rolling(window=short_window).mean()
    data['long_sma'] = data['close'].rolling(window=long_window).mean()
    
    # Buy signal: short SMA crosses above long SMA
    data['signal'] = 0
    data.loc[data['short_sma'] > data['long_sma'], 'signal'] = 1
    data.loc[data['short_sma'] < data['long_sma'], 'signal'] = -1
    return data

def normal_distribution_strategy(data):
    mean = data['close'].mean()
    std_dev = data['close'].std()
    
    # Buy if price is below mean - 2 * std_dev, sell if above mean + 2 * std_dev
    data['signal'] = 0
    data.loc[data['close'] < (mean - 2 * std_dev), 'signal'] = 1  # Buy signal
    data.loc[data['close'] > (mean + 2 * std_dev), 'signal'] = -1  # Sell signal
    return data

def evaluate_strategy(data, initial_balance=100000):
    balance = initial_balance
    positions = 0
    profit = 0  # Variable to track profit
    trade_log = []

    for index, row in data.iterrows():
        if row['signal'] == 1 and positions == 0:  # Buy signal
            positions = balance / row['close']
            balance = 0
            trade_log.append(f"Buy at {row['close']} on {index}")
        elif row['signal'] == -1 and positions == 0:  # Short sell signal
            balance += row['close']  # Add sell to balance
            trade_log.append(f"Short sell at {row['close']} on {index}")
        elif row['signal'] == -1 and positions > 0:  # Sell signal
            balance = positions * row['close']  # Sell positions to convert to balance
            profit += balance - initial_balance  # Add profit from previous position
            positions = 0
            trade_log.append(f"Sell at {row['close']} on {index}")
        
    final_balance = balance if positions == 0 else positions * data.iloc[-1]['close']
    return final_balance + profit, trade_log  # Return profit along with final balance

# Run backtest for multiple strategies on multiple stocks
def run_backtest():
    stock_tickers = ["BV", "IBM", "MSFT", "NUE", "NOC", "NVDA", "SPY", "TSLA", "VNQ", "VOO"]
    start_date = "2023-01-01"
    end_date = "2024-01-01"
    
    results = {}

    for stock in stock_tickers:
        print(f"Processing {stock}...")

        # Fetch stock data
        stock_data = fetch_stock_data(stock, start_date, end_date)

        # Save stock data to CSV
        save_stock_data_to_csv(stock, stock_data)

        # Apply trading strategies
        mean_reversion_data = mean_reversion_strategy(stock_data.copy())
        sma_data = sma_strategy(stock_data.copy())
        normal_distribution_data = normal_distribution_strategy(stock_data.copy())

        # Evaluate strategies
        mean_reversion_balance, mean_reversion_log = evaluate_strategy(mean_reversion_data)
        sma_balance, sma_log = evaluate_strategy(sma_data)
        normal_distribution_balance, normal_distribution_log = evaluate_strategy(normal_distribution_data)

        # Store results
        results[stock] = {
            "mean_reversion": {
                "final_balance": mean_reversion_balance,
                "trade_log": mean_reversion_log
            },
            "sma": {
                "final_balance": sma_balance,
                "trade_log": sma_log
            },
            "normal_distribution": {
                "final_balance": normal_distribution_balance,
                "trade_log": normal_distribution_log
            }
        }

    # Output results to a JSON file
    script_dir = os.path.dirname(__file__)

    # Set the path for the JSON file to be in the same directory
    json_file_path = os.path.join(script_dir, 'results.json')

    with open(json_file_path, 'w') as json_file:
        json.dump(results, json_file, indent=4)

    print(f"Backtest completed. Results saved to {json_file_path}.")
    
    return results

# Analyze results
def analyze_results(results):
    # Convert results to DataFrame for analysis
    analysis_data = []
    for stock, strategies in results.items():
        for strategy, result in strategies.items():
            analysis_data.append({
                'stock': stock,
                'strategy': strategy,
                'final_balance': result['final_balance']
            })

    df = pd.DataFrame(analysis_data)

    print(df)

    # Identify the most profitable stock and strategy
    most_profitable = df.loc[df['final_balance'].idxmax()]

    print(f"The most profitable strategy is {most_profitable['strategy']} for {most_profitable['stock']} with a final balance of {most_profitable['final_balance']}.")

    # Create a clustered bar chart
    plt.figure(figsize=(12, 6))
    sns.barplot(data=df, x='stock', y='final_balance', hue='strategy')
    plt.title("Profit by Stock and Trading Strategy")
    plt.ylabel("Final Balance")
    plt.xlabel("Stock Ticker")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# Run backtest and analyze results
results = run_backtest()
analyze_results(results)
