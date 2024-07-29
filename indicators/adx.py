import numpy as np

def calculate_ADX(data, period = 14):
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
    atr = tr.rolling(window=period).mean()
    plus_di = 100 * (plus_dm.rolling(window=period).mean() / atr)
    minus_di = 100 * (minus_dm.rolling(window=period).mean() / atr)
    dx = 100 * (abs(plus_di - minus_di) / (plus_di + minus_di))
    adx = dx.rolling(window=period).mean()
    return adx