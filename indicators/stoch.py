def calculate_STOCH(data, period=14):
    low_min = data['Low'].rolling(window=period).min()
    high_max = data['High'].rolling(window=period).max()
    K = 100 * ((data['Close'] - low_min) / (high_max - low_min))
    D = K.rolling(window=3).mean()  # 3-period moving average of %K
    return K, D