import yfinance as yf
import pandas as pd
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import Qt
from tkinter import *

#tickers = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'FB', 'TSLA', 'JPM', 'V', 'WMT', 'DIS', 'CSCO', 'INTC', 'NVDA', 'GS', 'IBM', 'NFLX', 'XOM', 'CAT', 'PG', 'CVX', 'MRK', 'KO', 'PFE', 'HD', 'C', 'VZ', 'MMM', 'GE', 'AXP', 'LMT', 'UNH', 'MCD', 'MO', 'BAC', 'GOOG', 'SLB', 'T', 'TXN', 'BK', 'MS', 'COST', 'PEP', 'BA', 'MMM', 'INTC', 'FDX', 'ABBV', 'USB', 'TWTR', 'DIS', 'BK', 'ADBE', 'BA', 'NKE', 'CSCO', 'PYPL']
tickers = [ 'AAPL' ]
start_date = "2011-11-01"
end_dates = ["2023-10-01","2023-10-02","2023-10-03","2023-10-04","2023-10-05","2023-10-06","2023-10-07","2023-10-08","2023-10-09","2023-10-10","2023-10-11","2023-10-12","2023-10-13","2023-10-14","2023-10-15","2023-10-16","2023-10-17","2023-10-18","2023-10-19","2023-10-20","2023-10-21","2023-10-22","2023-10-23","2023-10-24","2023-10-25","2023-10-26","2023-10-27","2023-10-28","2023-10-29","2023-10-30","2023-11-01","2023-11-02","2023-11-03","2023-11-04","2023-11-05","2023-11-06","2023-11-07","2023-11-08","2023-11-09","2023-11-10","2023-11-11","2023-11-12","2023-11-13","2023-11-14","2023-11-15","2023-11-16","2023-11-17","2023-11-18","2023-11-19","2023-11-20","2023-11-21","2023-11-22","2023-11-23","2023-11-24","2023-11-25","2023-11-26","2023-11-27","2023-11-28","2023-11-29","2023-11-30","2023-12-01","2023-12-02","2023-12-03","2023-12-04","2023-12-05","2023-12-06","2023-12-07","2023-12-08","2023-12-09"]

overall_data = []

for end_date in end_dates:
    for ticker in tickers:
        data = yf.download(ticker, start = start_date, end = end_date)
        
        data['symbol'] = ticker
        
        window_size = 20

        # Calculate the rolling mean and standard deviation of the Close price
        rolling_mean = data['Close'].rolling(window=window_size).mean()
        rolling_std = data['Close'].rolling(window=window_size).std()

        # Calculate the Upper and Lower Bollinger Bands
        data['upper_band'] = rolling_mean + (2 * rolling_std)
        data['lower_band'] = rolling_mean - (2 * rolling_std)
        data['middle_band'] = rolling_mean

        # Define the window size for Aroon Up and Aroon Down
        aroon_window = 14

        # Calculate the highest high and lowest low over the lookback period for Aroon Up and Aroon Down
        data['high_period'] = data['High'].rolling(window=aroon_window+1).apply(lambda x: np.argmax(x), raw=True) + 1
        data['low_period'] = data['Low'].rolling(window=aroon_window+1).apply(lambda x: np.argmin(x), raw=True) + 1

        # Calculate Aroon Up and Aroon Down
        data['aroon_up'] = ((aroon_window - data['high_period']) / aroon_window) * 100
        data['aroon_down'] = ((aroon_window - data['low_period']) / aroon_window) * 100

        # Define the window size for RSI
        rsi_window = 14

        # Calculate the daily price change
        delta = data['Close'].diff()

        # Define the gain and loss for up and down days
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # Calculate the rolling mean of gain and loss over the lookback period
        avg_gain = gain.rolling(window=rsi_window).mean()
        avg_loss = loss.rolling(window=rsi_window).mean()

        # Calculate the relative strength
        rs = avg_gain / avg_loss

        # Calculate the RSI
        data['rsi'] = 100 - (100 / (1 + rs))

        # Define BUY/SELL signals
        data['buy_signal'] = ((data['Close'] < data['lower_band']) & (data['aroon_up'] > data['aroon_down']) & (data['rsi'] < 30))
        data['sell_signal'] = ((data['Close'] > data['upper_band']) & (data['aroon_down'] > data['aroon_up']) & (data['rsi'] > 70))

        data = data.dropna()
        last_row = data.tail(1)

        overall_data.append(last_row)

    dfs = pd.concat(overall_data)

    datas = []
    datas = dfs
    datas = datas.drop([ 'Open', 'High', 'Low', 'Adj Close', 'symbol', 'upper_band', 'lower_band', 'middle_band', 'high_period', 'low_period', 'aroon_up', 'aroon_down'], axis = 1)


with pd.option_context('display.max_rows', None,
                    'display.max_columns', None,
                    'display.precision', 3,
                    ):
    print(datas)

buy_dataframe = datas[datas['buy_signal'] == True]
print("BUY:")
#buy_dataframe = buy_dataframe.drop(['buy_signal', 'sell_signal'], axis = 1)
buy_dataframe = [buy_dataframe]
#buy_d = buy_dataframe[buy_dataframe['Close'] >= 600]

sell_dataframe = datas[datas['sell_signal'] == True]
print("SELL:")
#sell_dataframe = sell_dataframe.drop(['Close', 'buy_signal', 'sell_signal'], axis = 1)
sell_dataframe = [sell_dataframe]


print()
with pd.option_context('display.max_rows', None,
                        'display.max_columns', None,
                        'display.precision', 3,
                        ):
        print(buy_dataframe)

print()
with pd.option_context('display.max_rows', None,
                        'display.max_columns', None,
                        'display.precision', 3,
                        ):
        print(sell_dataframe)


import tkinter as tk
from tkinter import ttk

# Create a tkinter window
root = tk.Tk()
root.title("Dataframe Viewer")

# Create a Treeview widget
tree = ttk.Treeview(root)

# Define columns for the Treeview widget
tree["columns"] = list(buy_dataframe[0].columns)

# Format column headers
for column in tree["columns"]:
    tree.heading(column, text=column)

# Add data to the Treeview widget
for index, row in buy_dataframe[0].iterrows():
    tree.insert("", "end", text=index, values=list(row))

# Pack the Treeview widget
tree.pack()

# Run the tkinter main loop
root.mainloop()
