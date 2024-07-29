import numpy as np

def calculate_CCI(data, period=20):
    tp = (data['High'] + data['Low'] + data['Close']) / 3
    sma_tp = tp.rolling(window=period).mean()
    mean_deviation = tp.rolling(window=period).apply(lambda x: np.mean(np.abs(x - np.mean(x))))
    CCI = (tp - sma_tp) / (0.015 * mean_deviation)
    return CCI