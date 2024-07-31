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

def lower_band(data, num_std_dev = 2, period=20):
    SMA = calculate_SMA(data, period)
    rolling_std = data['Close'].rolling(window=period).std()
    lowerband = SMA - (rolling_std * num_std_dev)
    return lowerband

def upper_band(data, num_std_dev = 2, period=20):
    SMA = calculate_SMA(data, period)
    rolling_std = data['Close'].rolling(window=period).std()
    upperband = SMA + (rolling_std * num_std_dev)
    return upperband

def calculate_CCI(data, period=20):
    tp = (data['High'] + data['Low'] + data['Close']) / 3
    sma_tp = tp.rolling(window=period).mean()
    mean_deviation = tp.rolling(window=period).apply(lambda x: np.mean(np.abs(x - np.mean(x))))
    CCI = (tp - sma_tp) / (0.015 * mean_deviation)
    return CCI

def calculate_EMA(data, period=20):
    alpha = 2 / (period + 1)
    EMA = data['Close'].ewm(alpha=alpha, adjust=False).mean()
    return EMA

def calculate_MACD(data, slow_period=26, fast_period=12, signal_period=9):
    fast_EMA = calculate_EMA(data, period=fast_period)
    slow_EMA = calculate_EMA(data, period=slow_period)
    MACD = fast_EMA - slow_EMA
    signal = MACD.rolling(window=signal_period).mean()
    histogram = MACD - signal
    return MACD, signal, histogram

def calculate_parabolic_SAR(data, af=0.02, max_af=0.2):
    data['SAR'] = data['Close'][0]
    data['EP'] = data['High'][0]
    data['AF'] = af
    data['trend'] = 1  # 1 for uptrend, -1 for downtrend

    for i in range(1, len(data)):
        previous_SAR = data['SAR'][i-1]
        previous_AF = data['AF'][i-1]
        previous_EP = data['EP'][i-1]
        previous_trend = data['trend'][i-1]

        if previous_trend == 1:  # Uptrend
            current_SAR = previous_SAR + previous_AF * (previous_EP - previous_SAR)
            current_SAR = min(current_SAR, data['Low'][i-1], data['Low'][i])
            if data['High'][i] > previous_EP:
                current_EP = data['High'][i]
                current_AF = min(previous_AF + af, max_af)
            else:
                current_EP = previous_EP
                current_AF = previous_AF
            if data['Low'][i] < current_SAR:
                current_trend = -1
                current_SAR = previous_EP
                current_EP = data['Low'][i]
                current_AF = af
            else:
                current_trend = 1
        else:  # Downtrend
            current_SAR = previous_SAR + previous_AF * (previous_EP - previous_SAR)
            current_SAR = max(current_SAR, data['High'][i-1], data['High'][i])
            if data['Low'][i] < previous_EP:
                current_EP = data['Low'][i]
                current_AF = min(previous_AF + af, max_af)
            else:
                current_EP = previous_EP
                current_AF = previous_AF
            if data['High'][i] > current_SAR:
                current_trend = 1
                current_SAR = previous_EP
                current_EP = data['High'][i]
                current_AF = af
            else:
                current_trend = -1

        data.loc[i, 'SAR'] = current_SAR
        data.loc[i, 'EP'] = current_EP
        data.loc[i, 'AF'] = current_AF
        data.loc[i, 'trend'] = current_trend

    return data['SAR']

def calculate_rsi(data, period = 14):
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    RS = gain / loss
    RSI = 100 - (100/(1+RS))
    return RSI

def calculate_SMA(data, period = 20):
    SMA = data['Close'].rolling(window=period).mean()
    return SMA 

def calculate_STOCH(data, period=14):
    low_min = data['Low'].rolling(window=period).min()
    high_max = data['High'].rolling(window=period).max()
    K = 100 * ((data['Close'] - low_min) / (high_max - low_min))
    D = K.rolling(window=3).mean()  # 3-period moving average of %K
    return K, D

import pandas as pd
import yfinance as yf
import numpy as np

tickers = ['EQUITASBNK.NS', 'AARTIIND.NS', 'ABB.NS', 'ABBOTINDIA.NS', 'ABCAPITAL.NS', 'ABFRL.NS', 'ACC.NS', 'ADANIENT.NS', 'ADANIPORTS.NS', 'AMBUJACEM.NS', 'APOLLOHOSP.NS', 'APOLLOTYRE.NS', 'ASHOKLEY.NS', 'ASIANPAINT.NS', 'ASTRAL.NS', 'ATUL.NS', 'AUBANK.NS', 'AUROPHARMA.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BALKRISIND.NS', 'BALRAMCHIN.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 'BATAINDIA.NS', 'BEL.NS', 'BERGEPAINT.NS', 'BHARATFORG.NS', 'BHARTIARTL.NS', 'BHEL.NS', 'BIOCON.NS', 'BOSCHLTD.NS', 'BPCL.NS', 'BRITANNIA.NS', 'BSOFT.NS', 'CANBK.NS', 'CANFINHOME.NS', 'CHAMBLFERT.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'COALINDIA.NS', 'COFORGE.NS', 'COLPAL.NS', 'CONCOR.NS', 'COROMANDEL.NS', 'CROMPTON.NS', 'CUMMINSIND.NS', 'DABUR.NS', 'DALBHARAT.NS', 'DEEPAKNTR.NS', 'DELTACORP.NS', 'DIVISLAB.NS', 'DIXON.NS', 'DLF.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'ESCORTS.NS', 'EXIDEIND.NS', 'FEDERALBNK.NS', 'GAIL.NS', 'GLENMARK.NS', 'GMRINFRA.NS', 'GNFC.NS', 'GODREJCP.NS', 'GODREJPROP.NS', 'GRANULES.NS', 'GRASIM.NS', 'GUJGASLTD.NS', 'HAL.NS', 'HAVELLS.NS', 'HCLTECH.NS', 'HDFC.NS', 'HDFCAMC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDCOPPER.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'ICICIPRULI.NS', 'IDEA.NS', 'IDFC.NS', 'IDFCFIRSTB.NS', 'IEX.NS', 'IGL.NS', 'INDHOTEL.NS', 'INDIACEM.NS', 'INDIAMART.NS', 'INDIGO.NS', 'INDUSINDBK.NS', 'INDUSTOWER.NS', 'INFY.NS', 'INTELLECT.NS', 'IOC.NS', 'IPCALAB.NS', 'IRCTC.NS', 'ITC.NS', 'JINDALSTEL.NS', 'JKCEMENT.NS', 'JSWSTEEL.NS', 'JUBLFOOD.NS', 'KOTAKBANK.NS', 'L&TFH.NS', 'LALPATHLAB.NS', 'LAURUSLABS.NS', 'LICHSGFIN.NS', 'LT.NS', 'LTIM.NS', 'LTTS.NS', 'LUPIN.NS', 'M&M.NS', 'M&MFIN.NS', 'MANAPPURAM.NS', 'MARICO.NS', 'MARUTI.NS', 'MCDOWELL-N.NS', 'MCX.NS', 'METROPOLIS.NS', 'MFSL.NS', 'MGL.NS', 'MOTHERSON.NS', 'MPHASIS.NS', 'MRF.NS', 'MUTHOOTFIN.NS', 'NATIONALUM.NS', 'NAUKRI.NS', 'NAVINFLUOR.NS', 'NESTLEIND.NS', 'NMDC.NS', 'NTPC.NS', 'OBEROIRLTY.NS', 'ONGC.NS', 'PAGEIND.NS', 'PEL.NS', 'PERSISTENT.NS', 'PFC.NS', 'PIDILITIND.NS', 'PIIND.NS', 'PNB.NS', 'POLYCAB.NS', 'POWERGRID.NS', 'PVRINOX.NS', 'RAIN.NS', 'RAMCOCEM.NS', 'RBLBANK.NS', 'RECLTD.NS', 'RELIANCE.NS', 'SAIL.NS', 'SBICARD.NS', 'SBILIFE.NS', 'SBIN.NS', 'SHREECEM.NS', 'SHRIRAMFIN.NS', 'SIEMENS.NS', 'SRF.NS', 'SUNPHARMA.NS', 'SUNTV.NS', 'SYNGENE.NS', 'TATACHEM.NS', 'TATACOMM.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TRENT.NS', 'TVSMOTOR.NS', 'UBL.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'VEDL.NS', 'VOLTAS.NS', 'WIPRO.NS', 'ZEEL.NS', 'ZYDUSLIFE.NS']
start_date = "2011-11-01"
end_dates = ["2024-07-01","2024-07-02","2024-07-03","2024-07-04","2024-07-05","2024-07-06","2024-07-11","2024-07-12","2024-07-15","2024-07-16","2024-07-17","2024-07-18","2024-07-19","2024-07-22","2024-07-23","2024-07-24","2024-07-25","2024-07-26","2024-07-27","2024-07-28","2024-07-29","2024-07-30"]


overall_data = []

for end_date in end_dates:
    for ticker in tickers:
        data = yf.download(ticker, start = start_date, end = end_date)
        data['symbol'] = ticker
        data['rsi'] = calculate_rsi(data, period=14)
        data['lower_band'] = lower_band(data, num_std_dev = 2, period=20)
        data['upper_band'] = upper_band(data, num_std_dev = 2, period=20)
        data['CCI'] = calculate_CCI(data, period=20)
        data['EMA'] = calculate_EMA(data, period=20)
        data['SMA'] = calculate_SMA(data, period=20)
        data['ADX'] = calculate_ADX(data, period=14)
        data['MACD'], data['signal'], data['histogram'] = calculate_MACD(data, slow_period=26, fast_period=12, signal_period=9)
        data['ParSAR'] = calculate_parabolic_SAR(data, af=0.02, max_af=0.2)
        data['K'], data['D'] = calculate_STOCH(data, period=14)
        
        data = data.dropna()
        last_row = data.tail(1)

        overall_data.append(last_row)

    dfs = pd.concat(overall_data)

    datas = []
    datas = dfs
    datas = datas.drop(['Open', 'High', 'Low', 'Adj Close', 'upper_band', 'lower_band'], axis = 1)

with pd.option_context('display.max_rows', None,
                        'display.max_columns', None,
                        'display.precision', 3,
                        ):
        print(datas)

'''
Extra lines of code:

data['ParSAR'] = calculate_parabolic_SAR(data, af=0.02, max_af=0.2)

signals code:
data['Buy_Signal'] = np.where(
            (data['rsi'] < 30) &
            (data['Close'] <= data['lower_band']) &
            (data['CCI'] < -100) &
            (data['EMA'] > data['SMA']),
            True, False)

        data['Sell_Signal'] = np.where(
            (data['rsi'] > 70) &
            (data['Close'] >= data['upper_band']) &
            (data['CCI'] > 100) &
            (data['EMA'] < data['SMA']),
            True, False)

'''