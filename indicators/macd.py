from ema import calculate_EMA

def calculate_MACD(data, slow_period=26, fast_period=12, signal_period=9):
    fast_EMA = calculate_EMA(data, period=fast_period)
    slow_EMA = calculate_EMA(data, period=slow_period)
    MACD = fast_EMA - slow_EMA
    signal = MACD.rolling(window=signal_period).mean()
    histogram = MACD - signal
    return MACD, signal, histogram