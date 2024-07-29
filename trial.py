import streamlit as st
import os
import yfinance as yf
import pandas as pd
import numpy as np

# Function to navigate between main pages
def main_navigation():
    st.sidebar.title("Navigation")
    main_page = st.sidebar.radio("Go to", ["Home", "NSE Equities", "NSE Options", "NYSE Equities", "Nifty50 Strats"])
    return main_page

# Function to navigate between subpages
def sub_navigation(main_page):
    if main_page == "NSE Equities":
        sub_page = st.sidebar.radio("NSE Equities", ["180 FNO Stocks' Signals", "Mid Cap and Small Cap Stocks", "One Stock Analysis", "NV20BEES Analysis"])
        return sub_page
    return None

# Main Pages
def home():
    st.title("Home")
    st.write("Hello, you have reached the home page.")

@st.cache_data(ttl=10800)  # Cache data for 3 hours (10800 seconds)
def calculate_indicators(tickers, start_date, end_dates):
    overall_data = []

    for end_date in end_dates:
        for ticker in tickers:
            data = yf.download(ticker, start=start_date, end=end_date)
            data['symbol'] = ticker
            window_size = 20

            # Calculate the rolling mean and standard deviation of the Close price
            rolling_mean = data['Close'].rolling(window=window_size).mean()
            rolling_std = data['Close'].rolling(window=window_size).std()

            # Calculate the Upper and Lower Bollinger Bands
            data['upper_band'] = rolling_mean + (2 * rolling_std)
            data['lower_band'] = rolling_mean - (2 * rolling_std)
            data['middle_band'] = rolling_mean

            # Define the window size for Aroon Up and Aroon Down
            aroon_window = 14
            data['high_period'] = data['High'].rolling(window=aroon_window+1).apply(lambda x: np.argmax(x), raw=True) + 1
            data['low_period'] = data['Low'].rolling(window=aroon_window+1).apply(lambda x: np.argmin(x), raw=True) + 1
            data['aroon_up'] = ((aroon_window - data['high_period']) / aroon_window) * 100
            data['aroon_down'] = ((aroon_window - data['low_period']) / aroon_window) * 100

            # Define the window size for RSI
            rsi_window = 14
            delta = data['Close'].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(window=rsi_window).mean()
            avg_loss = loss.rolling(window=rsi_window).mean()
            rs = avg_gain / avg_loss
            data['rsi'] = 100 - (100 / (1 + rs))

            # Define BUY/SELL signals
            data['buy_signal'] = ((data['Close'] < data['lower_band']) & (data['aroon_up'] > data['aroon_down']) & (data['rsi'] < 30))
            data['sell_signal'] = ((data['Close'] > data['upper_band']) & (data['aroon_down'] > data['aroon_up']) & (data['rsi'] > 70))

            data = data.dropna()
            last_row = data.tail(1)
            overall_data.append(last_row)

    dfs = pd.concat(overall_data)
    datas = dfs.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume', 'upper_band', 'lower_band', 'middle_band', 'high_period', 'low_period', 'aroon_up', 'aroon_down', 'rsi'], axis=1)

    buy_dataframe = datas[datas['buy_signal'] == True]
    sell_dataframe = datas[datas['sell_signal'] == True]

    return buy_dataframe, sell_dataframe

def nse_equities(sub_page):
    if sub_page == "180 FNO Stocks' Signals":
        st.title("180 FNO Stocks' Signals")
        
        # Define tickers and date range
        # Display description
        st.write("""
        ### How RSI-Bollinger Band-Aroon Indicator Works
        The RSI-Bollinger Band-Aroon indicator is a combination of three technical indicators used in stock analysis:
        - **RSI (Relative Strength Index)**: Measures the magnitude of recent price changes to evaluate overbought or oversold conditions.
        - **Bollinger Bands**: Consist of a middle band (SMA) and an upper and lower band that are standard deviations away from the SMA, indicating volatility.
        - **Aroon Indicator**: Identifies trends and their strength over a given period.

        This indicator is used to generate buy and sell signals based on the conditions of these three indicators. It is a trailing indicator, meaning it follows the trend rather than predicting future movements. It is generally advised to wait for confirmation from 2-3 signals before acting.
        """)
        tickers = ['EQUITASBNK.NS', 'AARTIIND.NS', 'ABB.NS', 'ABBOTINDIA.NS', 'ABCAPITAL.NS', 'ABFRL.NS', 'ACC.NS', 'ADANIENT.NS', 'ADANIPORTS.NS', 'AMBUJACEM.NS', 'APOLLOHOSP.NS', 'APOLLOTYRE.NS', 'ASHOKLEY.NS', 'ASIANPAINT.NS', 'ASTRAL.NS', 'ATUL.NS', 'AUBANK.NS', 'AUROPHARMA.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BALKRISIND.NS', 'BALRAMCHIN.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 'BATAINDIA.NS', 'BEL.NS', 'BERGEPAINT.NS', 'BHARATFORG.NS', 'BHARTIARTL.NS', 'BHEL.NS', 'BIOCON.NS', 'BOSCHLTD.NS', 'BPCL.NS', 'BRITANNIA.NS', 'BSOFT.NS', 'CANBK.NS', 'CANFINHOME.NS', 'CHAMBLFERT.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'COALINDIA.NS', 'COFORGE.NS', 'COLPAL.NS', 'CONCOR.NS', 'COROMANDEL.NS', 'CROMPTON.NS', 'CUMMINSIND.NS', 'DABUR.NS', 'DALBHARAT.NS', 'DEEPAKNTR.NS', 'DELTACORP.NS', 'DIVISLAB.NS', 'DIXON.NS', 'DLF.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'ESCORTS.NS', 'EXIDEIND.NS', 'FEDERALBNK.NS', 'GAIL.NS', 'GLENMARK.NS', 'GMRINFRA.NS', 'GNFC.NS', 'GODREJCP.NS', 'GODREJPROP.NS', 'GRANULES.NS', 'GRASIM.NS', 'GUJGASLTD.NS', 'HAL.NS', 'HAVELLS.NS', 'HCLTECH.NS', 'HDFC.NS', 'HDFCAMC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDCOPPER.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'ICICIPRULI.NS', 'IDEA.NS', 'IDFC.NS', 'IDFCFIRSTB.NS', 'IEX.NS', 'IGL.NS', 'INDHOTEL.NS', 'INDIACEM.NS', 'INDIAMART.NS', 'INDIGO.NS', 'INDUSINDBK.NS', 'INDUSTOWER.NS', 'INFY.NS', 'INTELLECT.NS', 'IOC.NS', 'IPCALAB.NS', 'IRCTC.NS', 'ITC.NS', 'JINDALSTEL.NS', 'JKCEMENT.NS', 'JSWSTEEL.NS', 'JUBLFOOD.NS', 'KOTAKBANK.NS', 'L&TFH.NS', 'LALPATHLAB.NS', 'LAURUSLABS.NS', 'LICHSGFIN.NS', 'LT.NS', 'LTIM.NS', 'LTTS.NS', 'LUPIN.NS', 'M&M.NS', 'M&MFIN.NS', 'MANAPPURAM.NS', 'MARICO.NS', 'MARUTI.NS', 'MCDOWELL-N.NS', 'MCX.NS', 'METROPOLIS.NS', 'MFSL.NS', 'MGL.NS', 'MOTHERSON.NS', 'MPHASIS.NS', 'MRF.NS', 'MUTHOOTFIN.NS', 'NATIONALUM.NS', 'NAUKRI.NS', 'NAVINFLUOR.NS', 'NESTLEIND.NS', 'NMDC.NS', 'NTPC.NS', 'OBEROIRLTY.NS', 'ONGC.NS', 'PAGEIND.NS', 'PEL.NS', 'PERSISTENT.NS', 'PFC.NS', 'PIDILITIND.NS', 'PIIND.NS', 'PNB.NS', 'POLYCAB.NS', 'POWERGRID.NS', 'PVRINOX.NS', 'RAIN.NS', 'RAMCOCEM.NS', 'RBLBANK.NS', 'RECLTD.NS', 'RELIANCE.NS', 'SAIL.NS', 'SBICARD.NS', 'SBILIFE.NS', 'SBIN.NS', 'SHREECEM.NS', 'SHRIRAMFIN.NS', 'SIEMENS.NS', 'SRF.NS', 'SUNPHARMA.NS', 'SUNTV.NS', 'SYNGENE.NS', 'TATACHEM.NS', 'TATACOMM.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TRENT.NS', 'TVSMOTOR.NS', 'UBL.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'VEDL.NS', 'VOLTAS.NS', 'WIPRO.NS', 'ZEEL.NS', 'ZYDUSLIFE.NS']
        start_date = "2011-11-01"
        end_dates = ["2024-07-15","2024-07-16","2024-07-18","2024-07-19","2024-07-22"]
# extra dates: ,"2024-07-23","2024-07-24","2024-07-25"
        # Calculate indicators
        buy_dataframe, sell_dataframe = calculate_indicators(tickers, start_date, end_dates)

        # Display dataframes
        st.write("### Buy Signals DataFrame")
        st.dataframe(buy_dataframe)

        st.write("### Sell Signals DataFrame")
        st.dataframe(sell_dataframe)

    elif sub_page == "Mid Cap and Small Cap Stocks":
        st.title("Mid Cap and Small Cap Stocks")

        tickers = ['MOREPENLAB.NS', 'PATELENG.NS', 'SKIPPER.NS', 'CAPACITE.NS', '360ONE.NS', 'AARTIIND.NS', 'AAVAS.NS', 'ACE.NS', 'AETHER.NS', 'AFFLE.NS', 'APLLTD.NS', 'ALKYLAMINE.NS', 'ALLCARGO.NS', 'ALOKINDS.NS', 'ARE&M.NS', 'AMBER.NS', 'ANANDRATHI.NS', 'ANGELONE.NS', 'ANURAS.NS', 'APARINDS.NS', 'APTUS.NS', 'ACI.NS', 'ASAHIINDIA.NS', 'ASTERDM.NS', 'ASTRAZEN.NS', 'AVANTIFEED.NS', 'BEML.NS', 'BLS.NS', 'BALAMINES.NS', 'BALRAMCHIN.NS', 'BIKAJI.NS', 'BIRLACORPN.NS', 'BSOFT.NS', 'BLUEDART.NS', 'BLUESTARCO.NS', 'BORORENEW.NS', 'BRIGADE.NS', 'MAPMYINDIA.NS', 'CCL.NS', 'CESC.NS', 'CIEINDIA.NS', 'CSBBANK.NS', 'CAMPUS.NS', 'CANFINHOME.NS', 'CAPLIPOINT.NS', 'CGCL.NS', 'CASTROLIND.NS', 'CEATLTD.NS', 'CELLO.NS', 'CENTRALBK.NS', 'CDSL.NS', 'CENTURYPLY.NS', 'CENTURYTEX.NS', 'CERA.NS', 'CHALET.NS', 'CHAMBLFERT.NS', 'CHEMPLASTS.NS', 'CHENNPETRO.NS', 'CHOLAHLDNG.NS', 'CUB.NS', 'CLEAN.NS', 'COCHINSHIP.NS', 'CAMS.NS', 'CONCORDBIO.NS', 'CRAFTSMAN.NS', 'CREDITACC.NS', 'CROMPTON.NS', 'CYIENT.NS', 'DCMSHRIRAM.NS', 'DOMS.NS', 'DATAPATTNS.NS', 'DEEPAKFERT.NS', 'EIDPARRY.NS', 'EIHOTEL.NS', 'EPL.NS', 'EASEMYTRIP.NS', 'ELECON.NS', 'ELGIEQUIP.NS', 'ENGINERSIN.NS', 'EQUITASBNK.NS', 'ERIS.NS', 'EXIDEIND.NS', 'FDC.NS', 'FINEORG.NS', 'FINPIPE.NS', 'FSL.NS', 'FIVESTAR.NS', 'GMMPFAUDLR.NS', 'GRSE.NS', 'GILLETTE.NS', 'GLS.NS', 'GLENMARK.NS', 'MEDANTA.NS', 'GPIL.NS', 'GODFRYPHLP.NS', 'GRANULES.NS', 'GRAPHITE.NS', 'GESHIP.NS', 'GAEL.NS', 'GMDCLTD.NS', 'GNFC.NS', 'GPPL.NS', 'GSFC.NS', 'GSPL.NS', 'HEG.NS', 'HBLPOWER.NS', 'HFCL.NS', 'HAPPSTMNDS.NS', 'HAPPYFORGE.NS', 'HSCL.NS', 'HINDCOPPER.NS', 'POWERINDIA.NS', 'HOMEFIRST.NS', 'HONASA.NS', 'HUDCO.NS', 'IDFC.NS', 'IIFL.NS', 'IRB.NS', 'IRCON.NS', 'ITI.NS', 'INDIACEM.NS', 'IBULHSGFIN.NS', 'INDIAMART.NS', 'IEX.NS', 'IOB.NS', 'INDIGOPNTS.NS', 'INOXWIND.NS', 'INTELLECT.NS', 'JBCHEPHARM.NS', 'JBMA.NS', 'JKLAKSHMI.NS', 'JKPAPER.NS', 'JMFINANCIL.NS', 'JAIBALAJI.NS', 'J&KBANK.NS', 'JINDALSAW.NS', 'JUBLINGREA.NS', 'JUBLPHARMA.NS', 'JWL.NS', 'JUSTDIAL.NS', 'JYOTHYLAB.NS', 'KNRCON.NS', 'KRBL.NS', 'KSB.NS', 'KPIL.NS', 'KARURVYSYA.NS', 'KAYNES.NS', 'KEC.NS', 'KFINTECH.NS', 'KIMS.NS', 'LATENTVIEW.NS', 'LXCHEM.NS', 'LEMONTREE.NS', 'MMTC.NS', 'MTARTECH.NS', 'MGL.NS', 'MAHSEAMLES.NS', 'MHRIL.NS', 'MAHLIFE.NS', 'MANAPPURAM.NS', 'MRPL.NS', 'MASTEK.NS', 'MEDPLUS.NS', 'METROPOLIS.NS', 'MINDACORP.NS', 'MOTILALOFS.NS', 'MCX.NS', 'NATCOPHARM.NS', 'NBCC.NS', 'NCC.NS', 'NLCINDIA.NS', 'NSLNISP.NS', 'NH.NS', 'NATIONALUM.NS', 'NAVINFLUOR.NS', 'NETWORK18.NS', 'NAM-INDIA.NS', 'NUVAMA.NS', 'NUVOCO.NS', 'OLECTRA.NS', 'PCBL.NS', 'PNBHOUSING.NS', 'PNCINFRA.NS', 'PVRINOX.NS', 'PPLPHARMA.NS', 'POLYMED.NS', 'PRAJIND.NS', 'PRINCEPIPE.NS', 'PRSMJOHNSN.NS', 'QUESS.NS', 'RRKABEL.NS', 'RBLBANK.NS', 'RHIM.NS', 'RITES.NS', 'RADICO.NS', 'RAILTEL.NS', 'RAINBOW.NS', 'RAJESHEXPO.NS', 'RKFORGE.NS', 'RCF.NS', 'RATNAMANI.NS', 'RTNINDIA.NS', 'RAYMOND.NS', 'REDINGTON.NS', 'RBA.NS', 'ROUTE.NS', 'SBFC.NS', 'SAFARI.NS', 'SANOFI.NS', 'SAPPHIRE.NS', 'SAREGAMA.NS', 'SCHNEIDER.NS', 'RENUKA.NS', 'SHYAMMETL.NS', 'SIGNATURE.NS', 'SOBHA.NS', 'SONATSOFTW.NS', 'SWSOLAR.NS', 'STLTECH.NS', 'SPARC.NS', 'SUNTECK.NS', 'SWANENERGY.NS', 'SYRMA.NS', 'TV18BRDCST.NS', 'TVSSCS.NS', 'TMB.NS', 'TANLA.NS', 'TATAINVEST.NS', 'TTML.NS', 'TEJASNET.NS', 'TITAGARH.NS', 'TRIDENT.NS', 'TRIVENI.NS', 'TRITURBINE.NS', 'UCOBANK.NS', 'UTIAMC.NS', 'UJJIVANSFB.NS', 'USHAMART.NS', 'VGUARD.NS', 'VIPIND.NS', 'VAIBHAVGBL.NS', 'VTL.NS', 'VARROC.NS', 'VIJAYA.NS', 'WELCORP.NS', 'WELSPUNLIV.NS', 'WESTLIFE.NS', 'WHIRLPOOL.NS', 'ZENSARTECH.NS', 'ECLERX.NS', 'ACC.NS', 'AUBANK.NS', 'ABCAPITAL.NS', 'ALKEM.NS', 'ASHOKLEY.NS', 'ASTRAL.NS', 'AUROPHARMA.NS', 'BALKRISIND.NS', 'BANDHANBNK.NS', 'BHARATFORG.NS', 'BHEL.NS', 'COFORGE.NS', 'CONCOR.NS', 'CUMMINSIND.NS', 'DALBHARAT.NS', 'DIXON.NS', 'ESCORTS.NS', 'FEDERALBNK.NS', 'GMRINFRA.NS', 'GODREJPROP.NS', 'GUJGASLTD.NS', 'HDFCAMC.NS', 'HINDPETRO.NS', 'IDFCFIRSTB.NS', 'INDUSTOWER.NS', 'JUBLFOOD.NS', 'LTF.NS', 'LTTS.NS', 'LUPIN.NS', 'MRF.NS', 'M&MFIN.NS', 'MFSL.NS', 'MAXHEALTH.NS', 'MPHASIS.NS', 'NMDC.NS', 'OBEROIRLTY.NS', 'OFSS.NS', 'PIIND.NS', 'PAGEIND.NS', 'PERSISTENT.NS', 'PETRONET.NS', 'POLYCAB.NS', 'SAIL.NS', 'SUZLON.NS', 'TATACOMM.NS', 'TIINDIA.NS', 'UPL.NS', 'IDEA.NS', 'YESBANK.NS', 'CAPACITE.NS', 'EQUITASBNK.NS', 'AARTIIND.NS', 'ABB.NS', 'ABBOTINDIA.NS', 'ABCAPITAL.NS', 'ABFRL.NS', 'ACC.NS', 'ADANIENT.NS', 'ADANIPORTS.NS', 'AMBUJACEM.NS', 'APOLLOHOSP.NS', 'APOLLOTYRE.NS', 'ASHOKLEY.NS', 'ASIANPAINT.NS', 'ASTRAL.NS', 'ATUL.NS', 'AUBANK.NS', 'AUROPHARMA.NS', 'AXISBANK.NS', 'BAJAJ-AUTO.NS', 'BAJAJFINSV.NS', 'BAJFINANCE.NS', 'BALKRISIND.NS', 'BALRAMCHIN.NS', 'BANDHANBNK.NS', 'BANKBARODA.NS', 'BATAINDIA.NS', 'BEL.NS', 'BERGEPAINT.NS', 'BHARATFORG.NS', 'BHARTIARTL.NS', 'BHEL.NS', 'BIOCON.NS', 'BOSCHLTD.NS', 'BPCL.NS', 'BRITANNIA.NS', 'BSOFT.NS', 'CANBK.NS', 'CANFINHOME.NS', 'CHAMBLFERT.NS', 'CHOLAFIN.NS', 'CIPLA.NS', 'COALINDIA.NS', 'COFORGE.NS', 'COLPAL.NS', 'CONCOR.NS', 'COROMANDEL.NS', 'CROMPTON.NS', 'CUMMINSIND.NS', 'DABUR.NS', 'DALBHARAT.NS', 'DEEPAKNTR.NS', 'DELTACORP.NS', 'DIVISLAB.NS', 'DIXON.NS', 'DLF.NS', 'DRREDDY.NS', 'EICHERMOT.NS', 'ESCORTS.NS', 'EXIDEIND.NS', 'FEDERALBNK.NS', 'GAIL.NS', 'GLENMARK.NS', 'GMRINFRA.NS', 'GNFC.NS', 'GODREJCP.NS', 'GODREJPROP.NS', 'GRANULES.NS', 'GRASIM.NS', 'GUJGASLTD.NS', 'HAL.NS', 'HAVELLS.NS', 'HCLTECH.NS', 'HDFCAMC.NS', 'HDFCBANK.NS', 'HDFCLIFE.NS', 'HEROMOTOCO.NS', 'HINDALCO.NS', 'HINDCOPPER.NS', 'HINDPETRO.NS', 'HINDUNILVR.NS', 'ICICIBANK.NS', 'ICICIPRULI.NS', 'IDEA.NS', 'IDFC.NS', 'IDFCFIRSTB.NS', 'IEX.NS', 'IGL.NS', 'INDHOTEL.NS', 'INDIACEM.NS', 'INDIAMART.NS', 'INDIGO.NS', 'INDUSINDBK.NS', 'INDUSTOWER.NS', 'INFY.NS', 'INTELLECT.NS', 'IOC.NS', 'IPCALAB.NS', 'IRCTC.NS', 'ITC.NS', 'JINDALSTEL.NS', 'JKCEMENT.NS', 'JSWSTEEL.NS', 'JUBLFOOD.NS', 'KOTAKBANK.NS', 'LALPATHLAB.NS', 'LAURUSLABS.NS', 'LICHSGFIN.NS', 'LT.NS', 'LTIM.NS', 'LTTS.NS', 'LUPIN.NS', 'M&M.NS', 'M&MFIN.NS', 'MANAPPURAM.NS', 'MARICO.NS', 'MARUTI.NS', 'MCDOWELL-N.NS', 'MCX.NS', 'METROPOLIS.NS', 'MFSL.NS', 'MGL.NS', 'MOTHERSON.NS', 'MPHASIS.NS', 'MRF.NS', 'MUTHOOTFIN.NS', 'NATIONALUM.NS', 'NAUKRI.NS', 'NAVINFLUOR.NS', 'NESTLEIND.NS', 'NMDC.NS', 'NTPC.NS', 'OBEROIRLTY.NS', 'ONGC.NS', 'PAGEIND.NS', 'PEL.NS', 'PERSISTENT.NS', 'PFC.NS', 'PIDILITIND.NS', 'PIIND.NS', 'PNB.NS', 'POLYCAB.NS', 'POWERGRID.NS', 'PVRINOX.NS', 'RAIN.NS', 'RAMCOCEM.NS', 'RBLBANK.NS', 'RECLTD.NS', 'RELIANCE.NS', 'SAIL.NS', 'SBICARD.NS', 'SBILIFE.NS', 'SBIN.NS', 'SHREECEM.NS', 'SHRIRAMFIN.NS', 'SIEMENS.NS', 'SRF.NS', 'SUNPHARMA.NS', 'SUNTV.NS', 'SYNGENE.NS', 'TATACHEM.NS', 'TATACOMM.NS', 'TATACONSUM.NS', 'TATAMOTORS.NS', 'TATAPOWER.NS', 'TATASTEEL.NS', 'TCS.NS', 'TECHM.NS', 'TITAN.NS', 'TORNTPHARM.NS', 'TRENT.NS', 'TVSMOTOR.NS', 'UBL.NS', 'ULTRACEMCO.NS', 'UPL.NS', 'VEDL.NS', 'VOLTAS.NS', 'WIPRO.NS', 'ZEEL.NS', 'ZYDUSLIFE.NS']
        start_date = "2011-11-01"
        end_dates = ["2024-07-15","2024-07-16","2024-07-18","2024-07-19","2024-07-22"]

        buy_dataframe, sell_dataframe = calculate_indicators(tickers, start_date, end_dates)

        # Display dataframes
        st.write("### Buy Signals DataFrame")
        st.dataframe(buy_dataframe)

        st.write("### Sell Signals DataFrame")
        st.dataframe(sell_dataframe)

    elif sub_page == "One Stock Analysis":
        st.title("One Stock Analysis")

    elif sub_page == "NV20BEES Analysis":
        st.title("NV20BEES Analysis")

        tickers = ['NV20BEES.NS', 'DRREDDY.NS', 'HEROMOTOCO.NS', 'WIPRO.NS', 'BRITANNIA.NS', 'TATASTEEL.NS', 'COALINDIA.NS', 'BAJAJ-AUTO.NS', 'ONGC.NS', 'HINDALCO.NS', 'INDUSINDBK.NS', 'GRASIM.NS', 'TECHM.NS', 'ICICIBANK.NS', 'INFY.NS', 'ITC.NS', 'TCS.NS', 'SBIN.NS', 'NTPC.NS', 'POWERGRID.NS', 'HCLTECH.NS']
        start_date = "2011-11-01"
        end_dates = ["2024-07-15","2024-07-16","2024-07-18","2024-07-19"]

        buy_dataframe, sell_dataframe = calculate_indicators(tickers, start_date, end_dates)

        # Display dataframes
        st.write("### Buy Signals DataFrame")
        st.dataframe(buy_dataframe)

        st.write("### Sell Signals DataFrame")
        st.dataframe(sell_dataframe)

def nse_options():
    st.title("NSE Options")

def nyse_equities():
    st.title("NYSE Equities")

def nifty50_strats():
    st.title("Nifty50 Strats")

# Main function to control the navigation
def main():
    main_page = main_navigation()
    sub_page = sub_navigation(main_page)
    
    if main_page == "Home":
        home()
    elif main_page == "NSE Equities":
        nse_equities(sub_page)
    elif main_page == "NSE Options":
        nse_options()
    elif main_page == "NYSE Equities":
        nyse_equities()
    elif main_page == "Nifty50 Strats":
        nifty50_strats()

if __name__ == "__main__":
    main()
