from sma import calculate_SMA

def calculate_Bollinger_Bands(data, period=20, num_std_dev=2):
    SMA = calculate_SMA(data, period)
    rolling_std = data['Close'].rolling(window=period).std()
    upper_band = SMA + (rolling_std * num_std_dev)
    lower_band = SMA - (rolling_std * num_std_dev)
    return upper_band, lower_band