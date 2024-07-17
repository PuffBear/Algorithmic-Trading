import yfinance as yf
import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

Time = float(input(f"Enter Time in decimals in terms of years for analysis: "))

# Function to calculate historical volatility
def calculate_volatility(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    prices = data['Close']
    returns = prices.pct_change().dropna()
    daily_return_variance = np.var(returns)
    daily_volatility = np.sqrt(daily_return_variance)
    annual_volatility = daily_volatility * np.sqrt(252)
    return annual_volatility

# Error function for normal distribution
def erf(x):
    A1 = 0.254829592
    A2 = -0.284496736
    A3 = 1.421413741
    A4 = -1.453152027
    A5 = 1.061405429
    P = 0.3275911

    sign = 1 if x >= 0 else -1
    x = abs(x)

    t = 1.0 / (1.0 + P * x)
    y = 1.0 - (((((A5 * t + A4) * t) + A3) * t + A2) * t + A1) * t * math.exp(-x * x)

    return sign * y

# Cumulative standard normal distribution function
def CSN(value):
    return 0.5 * (1.0 + erf(value / math.sqrt(2.0)))

# d1 and d2 for Black-Scholes model
def d1(S_0, strike, risk_free_rate, volatility, time_to_maturity):
    return (math.log(S_0 / strike) + (risk_free_rate + (volatility ** 2) / 2) * time_to_maturity) / (volatility * math.sqrt(time_to_maturity))

def d2(S_0, strike, risk_free_rate, volatility, time_to_maturity):
    return d1(S_0, strike, risk_free_rate, volatility, time_to_maturity) - (volatility * math.sqrt(time_to_maturity))

# Black-Scholes Pricing Model
def BlackScholesPricingModel(S, X, risk_free, vol, time, isCallOption):
    dte = time * 365.2425

    if isCallOption:
        d_1 = d1(S, X, risk_free, vol, time)
        d_2 = d2(S, X, risk_free, vol, time)

        premium = S * CSN(d_1) - X * math.exp(-risk_free * time) * CSN(d_2)
        delta = CSN(d_1)
        gamma = CSN(d_1) / (S * vol * math.sqrt(time))
        theta = -(S * CSN(d_1) * vol) / (2 * math.sqrt(time)) - risk_free * X * math.exp(-risk_free * time) * CSN(d_2)
        vega = S * CSN(d_1) * math.sqrt(time)
        rho = X * time * math.exp(-risk_free * time) * CSN(d_2)
        implied_volatility = vol - ((premium - (premium - 0.01)) / vega)
        intrinsic_value = max(S - X, 0.0)
    else:
        d_1 = d1(S, X, risk_free, vol, time)
        d_2 = d2(S, X, risk_free, vol, time)
        premium = X * math.exp(-risk_free * time) * CSN(-d_2) - S * CSN(-d_1)
        delta = CSN(d_1) - 1
        gamma = CSN(d_1) / (S * vol * math.sqrt(time))
        theta = -(S * CSN(d_1) * vol) / (2 * math.sqrt(time)) - risk_free * X * math.exp(-risk_free * time) * CSN(-d_2)
        vega = S * CSN(d_1) * math.sqrt(time)
        rho = -X * time * math.exp(-risk_free * time) * CSN(-d_2)
        implied_volatility = vol - ((premium - 0.01 - premium) / vega)
        intrinsic_value = max(X - S, 0.0)

    return {
        "Premium": premium,
        "Delta": delta,
        "Gamma": gamma,
        "Theta": theta,
        "Vega": vega,
        "Rho": rho,
        "Implied Volatility": implied_volatility,
        "Intrinsic Value": intrinsic_value
    }

def initial_strike_price(S0):
    if S0 < 500:
        K = S0 - 25
        K -= K % 2.5
    elif S0 < 1000:
        K = S0 - 50
        K -= K % 5
    elif S0 < 2000:
        K = S0 - 100
        K -= K % 10
    elif S0 < 4000:
        K = S0 - 250
        K -= K % 25
    else:
        K = S0 - 500
        K -= K % 50
    return K

# Main code to get data and calculate signals
tickers = ['EQUITASBNK.NS', 'AARTIIND.NS', 'ABB.NS', 'ABBOTINDIA.NS', 'ABCAPITAL.NS', 'ABFRL.NS', 'ACC.NS', 'ADANIENT.NS', 'ADANIPORTS.NS', 'AMBUJACEM.NS', 'APOLLOHOSP.NS', 'APOLLOTYRE.NS', 'ASHOKLEY.NS', 'ASIANPAINT.NS', 'ASTRAL.NS', 'ATUL.NS', 'AUBANK.NS', 'AUROPHARMA.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BALKRISIND.NS', 'BALRAMCHIN.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 'BATAINDIA.NS', 'BEL.NS', 'BERGEPAINT.NS', 'BHARATFORG.NS', 'BHARTIARTL.NS', 'BHEL.NS', 'BIOCON.NS', 'BOSCHLTD.NS', 'BPCL.NS', 'BRITANNIA.NS', 'BSOFT.NS', 'CANBK.NS', 'CANFINHOME.NS', 'CHAMBLFERT.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'COALINDIA.NS', 'COFORGE.NS', 'COLPAL.NS', 'CONCOR.NS', 'COROMANDEL.NS', 'CROMPTON.NS', 'CUMMINSIND.NS', 'DABUR.NS', 'DALBHARAT.NS', 'DEEPAKNTR.NS', 'DELTACORP.NS', 'DIVISLAB.NS', 'DIXON.NS', 'DLF.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'ESCORTS.NS', 'EXIDEIND.NS', 'FEDERALBNK.NS', 'GAIL.NS', 'GLENMARK.NS', 'GMRINFRA.NS', 'GNFC.NS', 'GODREJCP.NS', 'GODREJPROP.NS', 'GRANULES.NS', 'GRASIM.NS', 'GUJGASLTD.NS', 'HAL.NS', 'HAVELLS.NS', 'HCLTECH.NS', 'HDFC.NS', 'HDFCAMC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDCOPPER.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'ICICIPRULI.NS', 'IDEA.NS', 'IDFC.NS', 'IDFCFIRSTB.NS', 'IEX.NS', 'IGL.NS', 'INDHOTEL.NS', 'INDIACEM.NS', 'INDIAMART.NS', 'INDIGO.NS', 'INDUSINDBK.NS', 'INDUSTOWER.NS', 'INFY.NS', 'INTELLECT.NS', 'IOC.NS', 'IPCALAB.NS', 'IRCTC.NS', 'ITC.NS', 'JINDALSTEL.NS', 'JKCEMENT.NS', 'JSWSTEEL.NS', 'JUBLFOOD.NS', 'KOTAKBANK.NS', 'L&TFH.NS', 'LALPATHLAB.NS', 'LAURUSLABS.NS', 'LICHSGFIN.NS', 'LT.NS', 'LTIM.NS', 'LTTS.NS', 'LUPIN.NS', 'M&M.NS', 'M&MFIN.NS', 'MANAPPURAM.NS', 'MARICO.NS', 'MARUTI.NS', 'MCDOWELL-N.NS', 'MCX.NS', 'METROPOLIS.NS', 'MFSL.NS', 'MGL.NS', 'MOTHERSON.NS', 'MPHASIS.NS', 'MRF.NS', 'MUTHOOTFIN.NS', 'NATIONALUM.NS', 'NAUKRI.NS', 'NAVINFLUOR.NS', 'NESTLEIND.NS', 'NMDC.NS', 'NTPC.NS', 'OBEROIRLTY.NS', 'ONGC.NS', 'PAGEIND.NS', 'PEL.NS', 'PERSISTENT.NS', 'PFC.NS', 'PIDILITIND.NS', 'PIIND.NS', 'PNB.NS', 'POLYCAB.NS', 'POWERGRID.NS', 'PVRINOX.NS', 'RAIN.NS', 'RAMCOCEM.NS', 'RBLBANK.NS', 'RECLTD.NS', 'RELIANCE.NS', 'SAIL.NS', 'SBICARD.NS', 'SBILIFE.NS', 'SBIN.NS', 'SHREECEM.NS', 'SHRIRAMFIN.NS', 'SIEMENS.NS', 'SRF.NS', 'SUNPHARMA.NS', 'SUNTV.NS', 'SYNGENE.NS', 'TATACHEM.NS', 'TATACOMM.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TRENT.NS', 'TVSMOTOR.NS', 'UBL.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'VEDL.NS', 'VOLTAS.NS', 'WIPRO.NS', 'ZEEL.NS', 'ZYDUSLIFE.NS']
start_date = "2011-11-01"
end_dates = ["2024-07-11","2024-07-12","2024-07-15","2024-07-16","2024-07-17"]

overall_data = []

for end_date in end_dates:
    for ticker in tickers:
        data = yf.download(ticker, start=start_date, end=end_date)
        data['Volatility'] = calculate_volatility(ticker, start_date, end_date)
        data['symbol'] = ticker

        window_size = 20
        rolling_mean = data['Close'].rolling(window=window_size).mean()
        rolling_std = data['Close'].rolling(window=window_size).std()
        data['upper_band'] = rolling_mean + (2 * rolling_std)
        data['lower_band'] = rolling_mean - (2 * rolling_std)
        data['middle_band'] = rolling_mean

        aroon_window = 14
        data['high_period'] = data['High'].rolling(window=aroon_window + 1).apply(lambda x: np.argmax(x), raw=True) + 1
        data['low_period'] = data['Low'].rolling(window=aroon_window + 1).apply(lambda x: np.argmin(x), raw=True) + 1
        data['aroon_up'] = ((aroon_window - data['high_period']) / aroon_window) * 100
        data['aroon_down'] = ((aroon_window - data['low_period']) / aroon_window) * 100

        rsi_window = 14
        delta = data['Close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)
        avg_gain = gain.rolling(window=rsi_window).mean()
        avg_loss = loss.rolling(window=rsi_window).mean()
        rs = avg_gain / avg_loss
        data['rsi'] = 100 - (100 / (1 + rs))

        data['buy_signal'] = ((data['Close'] < data['lower_band']) & (data['aroon_up'] > data['aroon_down']) & (data['rsi'] < 30))
        data['sell_signal'] = ((data['Close'] > data['upper_band']) & (data['aroon_down'] > data['aroon_up']) & (data['rsi'] > 70))

        data = data.dropna()
        last_row = data.tail(1)
        overall_data.append(last_row)

dfs = pd.concat(overall_data)

datas = dfs.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume', 'upper_band', 'lower_band', 'middle_band', 'high_period', 'low_period', 'aroon_up', 'aroon_down', 'rsi'], axis=1)

buy_dataframe = datas[datas['buy_signal'] == True]
sell_dataframe = datas[datas['sell_signal'] == True]

def calculate_and_collect_option_prices(dataframe, option_type, T):
    results = []
    for _, row in dataframe.iterrows():
        S0 = row['Close']
        r = 0.069
        sigma = row['Volatility']
        isCallOption = (option_type == "CALL")
        K = initial_strike_price(S0)

        for i in range(21):
            result = BlackScholesPricingModel(S0, K, r, sigma, T, isCallOption)
            result['Strike Price'] = K
            result['Symbol'] = row['symbol']
            results.append(result)
            if S0 < 500:
                K += 2.5
            elif S0 < 1000:
                K += 5
            elif S0 < 2000:
                K += 10
            elif S0 < 4000:
                K += 25
            else:
                K += 50
    return results

buy_option_prices = calculate_and_collect_option_prices(buy_dataframe, "CALL", Time)
buy_df = pd.DataFrame(buy_option_prices)

sell_option_prices = calculate_and_collect_option_prices(sell_dataframe, "PUT", Time)
sell_df = pd.DataFrame(sell_option_prices)

# Function to create sub-plots for each stock
def create_premium_vs_strike_subplots(df, option_type):
    unique_symbols = df['Symbol'].unique()
    num_symbols = len(unique_symbols)
    fig, axs = plt.subplots(num_symbols, 1, figsize=(10, 6 * num_symbols))

    for i, symbol in enumerate(unique_symbols):
        symbol_df = df[df['Symbol'] == symbol]
        axs[i].plot(symbol_df['Strike Price'].to_numpy(), symbol_df['Premium'].to_numpy(), marker='o')
        axs[i].set_title(f'{symbol} - {option_type} Option: Premium vs Strike Price')
        axs[i].set_xlabel('Strike Price')
        axs[i].set_ylabel('Premium')
        axs[i].grid(True)

    plt.tight_layout()
    plt.show()

# Create sub-plots for buy and sell signal options
create_premium_vs_strike_subplots(buy_df, "CALL")
create_premium_vs_strike_subplots(sell_df, "PUT")
