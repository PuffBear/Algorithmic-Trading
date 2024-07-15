import yfinance as yf
import numpy as np

# Step 1: Collect Historical Price Data
ticker = 'ABCAPITAL.NS'
data = yf.download(ticker, start='2023-01-01', end='2023-12-31')
prices = data['Close']

# Step 2: Calculate Daily Returns
returns = prices.pct_change().dropna()

# Step 3: Compute Average Daily Return
average_daily_return = np.mean(returns)

# Step 4: Calculate Daily Return Variance
daily_return_variance = np.var(returns)

# Step 5: Convert Daily Volatility to Annual Volatility
daily_volatility = np.sqrt(daily_return_variance)
annual_volatility = daily_volatility * np.sqrt(252)

print(f"Annual Volatility (σ): {annual_volatility:.4f}")
