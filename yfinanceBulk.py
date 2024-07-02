import yfinance as yf
import pandas as pd
import time
import threading

# Define the list of tickers
tickers = [
    {'symbol': 'DIA'},
    {'symbol': 'MGV'},
    {'symbol': 'TNA'},
    {'symbol': 'IYY'},
    # Add more tickers as needed
]

# Function to get historical data from y finance
def get_historical_data(symbol, start_date, end_date, interval, data):
    try:
        stock = yf.Ticker(symbol)
        hist = stock.history(start=start_date, end=end_date, interval=interval)
        # Remove timezone information
        hist.index = hist.index.tz_convert(None)
        data[symbol] = hist
        print(f"Fetched data for {symbol}")
    except Exception as e:
        print(f"An error occurred for {symbol}: {e}")

# Request historical candles for each ticker4
start_date = '2024-01-01'
end_date = '2024-07-01'
interval = '1d'

# Dictionary to store the data
data = {}

# List to keep track of threads
threads = []

# Start a thread for each ticker
for ticker_info in tickers:
    symbol = ticker_info['symbol']
    thread = threading.Thread(target=get_historical_data, args=(symbol, start_date, end_date, interval, data))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()

# Working with Pandas DataFrames and writing to Excel
try:
    with pd.ExcelWriter('USA Dow Jones ETFs 1_day Data.xlsx') as writer:
        for symbol, hist_data in data.items():
            df = hist_data.reset_index()
            df.to_excel(writer, sheet_name=symbol, index=False)  # Save each DataFrame to a different sheet
    print("Data has been written to excel file")
except Exception as e:
    print(f"An error occurred while writing to Excel: {e}")
