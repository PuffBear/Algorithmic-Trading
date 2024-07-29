def calculate_EMA(data, period=20):
    alpha = 2 / (period + 1)
    EMA = data['Close'].ewm(alpha=alpha, adjust=False).mean()
    return EMA