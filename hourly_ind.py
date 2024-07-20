import yfinance as yf
import pandas as pd
import numpy as np

def calculate_indicators(tickers, start_date, end_dates, interval='5m'):
    overall_data = []

    for end_date in end_dates:
        for ticker in tickers:
            try:
                data = yf.download(ticker, start=start_date, end=end_date, interval=interval)
                if data.empty:
                    print(f"No data for {ticker} at interval {interval}")
                    continue
                data['symbol'] = ticker

                # Adjust window sizes for higher frequency data
                window_size = 20  # Example: same window size, can be adjusted based on the interval
                aroon_window = 14
                rsi_window = 14

                # Calculate the rolling mean and standard deviation of the Close price
                rolling_mean = data['Close'].rolling(window=window_size).mean()
                rolling_std = data['Close'].rolling(window=window_size).std()

                # Calculate the Upper and Lower Bollinger Bands
                data['upper_band'] = rolling_mean + (2 * rolling_std)
                data['lower_band'] = rolling_mean - (2 * rolling_std)
                data['middle_band'] = rolling_mean

                # Calculate Aroon Up and Aroon Down
                data['high_period'] = data['High'].rolling(window=aroon_window+1).apply(lambda x: np.argmax(x), raw=True) + 1
                data['low_period'] = data['Low'].rolling(window=aroon_window+1).apply(lambda x: np.argmin(x), raw=True) + 1
                data['aroon_up'] = ((aroon_window - data['high_period']) / aroon_window) * 100
                data['aroon_down'] = ((aroon_window - data['low_period']) / aroon_window) * 100

                # Calculate RSI
                delta = data['Close'].diff()
                gain = delta.where(delta > 0, 0)
                loss = -delta.where(delta < 0, 0)
                avg_gain = gain.rolling(window=rsi_window).mean()
                avg_loss = loss.rolling(window=rsi_window).mean()
                rs = avg_gain / avg_loss
                data['rsi'] = 100 - (100 / (1 + rs))

                # Define BUY/SELL signals
                data['buy_signal'] = ((data['Close'] < data['lower_band']) & (data['aroon_up'] > data['aroon_down']) & (data['rsi'] < 30))
                data['sell_signal'] = ((data['Close'] > data['upper_band']) & (data['aroon_down'] > data['aroon_up']) & (data['rsi'] > 70))

                data = data.dropna()
                last_row = data.tail(1)
                overall_data.append(last_row)
            except Exception as e:
                print(f"Error downloading data for {ticker}: {e}")
                continue

    if overall_data:
        dfs = pd.concat(overall_data)
        datas = dfs.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume', 'upper_band', 'lower_band', 'middle_band', 'high_period', 'low_period', 'aroon_up', 'aroon_down', 'rsi'], axis=1)

        buy_dataframe = datas[datas['buy_signal'] == True]
        sell_dataframe = datas[datas['sell_signal'] == True]

        return buy_dataframe, sell_dataframe
    else:
        return pd.DataFrame(), pd.DataFrame()

# Define tickers and date range
tickers = ['EQUITASBNK.NS', 'AARTIIND.NS', 'ABB.NS', 'ABBOTINDIA.NS', 'ABCAPITAL.NS', 'ABFRL.NS', 'ACC.NS', 'ADANIENT.NS', 'ADANIPORTS.NS', 'AMBUJACEM.NS', 'APOLLOHOSP.NS', 'APOLLOTYRE.NS', 'ASHOKLEY.NS', 'ASIANPAINT.NS', 'ASTRAL.NS', 'ATUL.NS', 'AUBANK.NS', 'AUROPHARMA.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BALKRISIND.NS', 'BALRAMCHIN.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 'BATAINDIA.NS', 'BEL.NS', 'BERGEPAINT.NS', 'BHARATFORG.NS', 'BHARTIARTL.NS', 'BHEL.NS', 'BIOCON.NS', 'BOSCHLTD.NS', 'BPCL.NS', 'BRITANNIA.NS', 'BSOFT.NS', 'CANBK.NS', 'CANFINHOME.NS', 'CHAMBLFERT.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'COALINDIA.NS', 'COFORGE.NS', 'COLPAL.NS', 'CONCOR.NS', 'COROMANDEL.NS', 'CROMPTON.NS', 'CUMMINSIND.NS', 'DABUR.NS', 'DALBHARAT.NS', 'DEEPAKNTR.NS', 'DELTACORP.NS', 'DIVISLAB.NS', 'DIXON.NS', 'DLF.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'ESCORTS.NS', 'EXIDEIND.NS', 'FEDERALBNK.NS', 'GAIL.NS', 'GLENMARK.NS', 'GMRINFRA.NS', 'GNFC.NS', 'GODREJCP.NS', 'GODREJPROP.NS', 'GRANULES.NS', 'GRASIM.NS', 'GUJGASLTD.NS', 'HAL.NS', 'HAVELLS.NS', 'HCLTECH.NS', 'HDFC.NS', 'HDFCAMC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDCOPPER.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'ICICIPRULI.NS', 'IDEA.NS', 'IDFC.NS', 'IDFCFIRSTB.NS', 'IEX.NS', 'IGL.NS', 'INDHOTEL.NS', 'INDIACEM.NS', 'INDIAMART.NS', 'INDIGO.NS', 'INDUSINDBK.NS', 'INDUSTOWER.NS', 'INFY.NS', 'INTELLECT.NS', 'IOC.NS', 'IPCALAB.NS', 'IRCTC.NS', 'ITC.NS', 'JINDALSTEL.NS', 'JKCEMENT.NS', 'JSWSTEEL.NS', 'JUBLFOOD.NS', 'KOTAKBANK.NS', 'L&TFH.NS', 'LALPATHLAB.NS', 'LAURUSLABS.NS', 'LICHSGFIN.NS', 'LT.NS', 'LTIM.NS', 'LTTS.NS', 'LUPIN.NS', 'M&M.NS', 'M&MFIN.NS', 'MANAPPURAM.NS', 'MARICO.NS', 'MARUTI.NS', 'MCDOWELL-N.NS', 'MCX.NS', 'METROPOLIS.NS', 'MFSL.NS', 'MGL.NS', 'MOTHERSON.NS', 'MPHASIS.NS', 'MRF.NS', 'MUTHOOTFIN.NS', 'NATIONALUM.NS', 'NAUKRI.NS', 'NAVINFLUOR.NS', 'NESTLEIND.NS', 'NMDC.NS', 'NTPC.NS', 'OBEROIRLTY.NS', 'ONGC.NS', 'PAGEIND.NS', 'PEL.NS', 'PERSISTENT.NS', 'PFC.NS', 'PIDILITIND.NS', 'PIIND.NS', 'PNB.NS', 'POLYCAB.NS', 'POWERGRID.NS', 'PVRINOX.NS', 'RAIN.NS', 'RAMCOCEM.NS', 'RBLBANK.NS', 'RECLTD.NS', 'RELIANCE.NS', 'SAIL.NS', 'SBICARD.NS', 'SBILIFE.NS', 'SBIN.NS', 'SHREECEM.NS', 'SHRIRAMFIN.NS', 'SIEMENS.NS', 'SRF.NS', 'SUNPHARMA.NS', 'SUNTV.NS', 'SYNGENE.NS', 'TATACHEM.NS', 'TATACOMM.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TRENT.NS', 'TVSMOTOR.NS', 'UBL.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'VEDL.NS', 'VOLTAS.NS', 'WIPRO.NS', 'ZEEL.NS', 'ZYDUSLIFE.NS']
start_date = "2023-06-01"
end_dates = ["2024-07-11","2024-07-12","2024-07-15","2024-07-16","2024-07-18"]

# Calculate indicators
buy_dataframe, sell_dataframe = calculate_indicators(tickers, start_date, end_dates, interval='1h')

print(buy_dataframe)
print(sell_dataframe)
