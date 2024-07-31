import numpy as np
import pandas as pd
import yfinance as yf

# Function to calculate ADX
def calculate_ADX(data, period=14):
    def calculate_DM(data):
        up_move = data['High'].diff()
        down_move = data['Low'].diff()
        plus_dm = np.where((up_move > down_move) & (up_move > 0), up_move, 0)
        minus_dm = np.where((down_move > up_move) & (down_move > 0), down_move, 0)
        return plus_dm, minus_dm

    plus_dm, minus_dm = calculate_DM(data)
    tr = np.maximum(data['High'] - data['Low'], 
                    np.maximum(abs(data['High'] - data['Close'].shift()), 
                               abs(data['Low'] - data['Close'].shift())))
    atr = pd.Series(tr).rolling(window=period).mean()
    plus_dm = pd.Series(plus_dm)
    minus_dm = pd.Series(minus_dm)
    plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)
    dx = 100 * (abs(plus_di - minus_di) / (plus_di + minus_di))
    adx = dx.rolling(window=period).mean()
    return adx

# Define tickers and dates
tickers = ['EQUITASBNK.NS', 'AARTIIND.NS']
start_date = "2011-11-01"
end_dates = ["2024-07-01", "2024-07-02", "2024-07-03", "2024-07-04", "2024-07-05"]

overall_data = []

for end_date in end_dates:
    for ticker in tickers:
        data = yf.download(ticker, start=start_date, end=end_date)
        data['symbol'] = ticker
        data['ADX'] = calculate_ADX(data, period=14)
        data = data.dropna()
        overall_data.append(data)

    dfs = pd.concat(overall_data)
    dfs = dfs.dropna()

print(dfs.head())
