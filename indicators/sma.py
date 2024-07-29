def calculate_SMA(data, period = 20):
    SMA = data['Close'].rolling(window=period).mean()
    return SMA 