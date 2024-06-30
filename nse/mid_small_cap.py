import yfinance as yf
import pandas as pd
import numpy as np
import sys
from PyQt5.QtWidgets import QApplication, QTableView
from PyQt5.QtCore import Qt
from tkinter import *

#tickers = ["ASHIANA.NS", "BEL.NS","AARTIDRUGS.NS", "AAVAS.NS", "ABMINTLTD.NS", "ACCELYA.NS", "ACE.NS", "ADANIGAS.NS", "ADANIGREEN.NS", "ADANIPOWER.NS", "ADANITRANS.NS", "ADFFOODS.NS", "ADL.NS", "ADORWELD.NS", "ADROITINFO.NS", "ADSL.NS", "ADVANIHOTR.NS", "ADVENZYMES.NS", "AEGISCHEM.NS", "AFFLE.NS", "AGARIND.NS", "AGCNET.NS", "AGRITECH.NS", "AGROPHOS.NS", "AHLEAST.NS", "AHLUCONT.NS", "AHLWEST.NS", "AIAENG.NS", "AIRAN.NS", "AJANTPHARM.NS", "AJMERA.NS", "AKASH.NS", "AKSHARCHEM.NS", "AKZOINDIA.NS", "ALANKIT.NS", "ALBERTDAVD.NS", "ALCHEM.NS", "ALEMBICLTD.NS", "ALICON.NS", "ALKEM.NS", "ALKYLAMINE.NS", "ALLCARGO.NS", "ALLSEC.NS", "ALMONDZ.NS", "ALOKINDS.NS", "AMARAJABAT.NS", "AMBER.NS", "AMBICAAGAR.NS", "AMBIKCO.NS", "AMBUJACEM.NS", "AMDIND.NS", "AMJLAND.NS", "AMRUTANJAN.NS", "ANANTRAJ.NS", "ANDHRABANK.NS", "ANDHRSUGAR.NS", "ANGIND.NS", "ANIKINDS.NS", "ANKITMETAL.NS", "ANSALAPI.NS", "ANSALHSG.NS", "ANUPAMRAS.NS", "APARINDS.NS", "APCL.NS", "APCOTEXIND.NS", "APEX.NS", "APLAPOLLO.NS", "APLLTD.NS", "APOLLO.NS", "APOLLOHOSP.NS", "APOLLOTYRE.NS", "APOLSINHOT.NS", "APTECHT.NS", "ARCHIDPLY.NS", "ARCHIES.NS", "ARCOTECH.NS", "ARENTERP.NS", "ARIES.NS", "ARIHANT.NS", "ARIHANTSUP.NS", "AROGRANITE.NS", 'ASAHIINDIA.NS',  'ASHAPURMIN.NS',  'ASHIANA.NS',  'ASHOKLEY.NS',  'ASIANPAINT.NS',  'ASTERDM.NS',  'ASTRAZEN.NS',  'ASTRAL.NS',  'ATUL.NS',  'AUROPHARMA.NS',  'AVANTIFEED.NS',  'DMART.NS',  'AXISBANK.NS',  'BALKRISIND.NS',  'BALMLAWRIE.NS',  'BALRAMCHIN.NS',  'BANDHANBNK.NS',  'BANKBARODA.NS',  'BANKINDIA.NS',  'BATAINDIA.NS',  'BAYERCROP.NS',  'BBL.NS',  'BEL.NS',  'BHARATFORG.NS',  'BHARATRAS.NS',  'BHARTIARTL.NS',  'BHEL.NS',  'BIGBLOC.NS',  'BIOCON.NS',  'BIRLACORPN.NS',  'BIRLAMONEY.NS',  'BLISSGVS.NS',  'BLUEDART.NS',  'BLUESTARCO.NS',  'BODALCHEM.NS',  'BOMDYEING.NS',  'BORORENEW.NS',  'BOSCHLTD.NS',  'BPCL.NS',  'BRIGADE.NS',  'BRITANNIA.NS',  'BRNL.NS',  'BSE.NS',  'CANBK.NS',  'CAMLINFINE.NS',  'CAMS.NS',  'CANFINHOME.NS',  'CAPLIPOINT.NS',  'CARBORUNIV.NS',  'CAREERP.NS',  'CARERATING.NS',  'CASTROLIND.NS',  'CCCL.NS',  'CCL.NS',  'CEATLTD.NS',  'CENTRALBK.NS',  'CENTURYPLY.NS',  "DALBHARAT.NS", "DCAL.NS","BANK.NS", "DECCANCE.NS", "DEEPAKFERT.NS", "DEEPAKNTR.NS", "DELTACORP.NS", "DELTAMAGNT.NS", "DEN.NS", "DENORA.NS", "DHAMPURSUG.NS", "DHANUKA.NS", "DHANUKAAGR.NS", "DHFL.NS", "DHUNINV.NS", "DIAPOWER.NS", "DICIND.NS", "DIGJAMLTD.NS", "DISHTV.NS", "DIVISLAB.NS", "DIXON.NS", "DLF.NS", "DLINKINDIA.NS", "DMART.NS", "DNAMEDIA.NS", "DOLLAR.NS", "DOLPHINOFF.NS", "DONEAR.NS", "DPSCLTD.NS", "DQE.NS", "DREDGECORP.NS", "DRREDDY.NS", "DSSL.NS", "DTIL.NS", "DUCON.NS", "DVL.NS", "DWARKESH.NS", "DYNAMATECH.NS", "DYNAMATIC.NS", "EASEMYTRIP.NS", "EBBETF0425.NS", "EBBETF0431.NS", "EBBETF0435.NS", "ECLERX.NS", "EDELWEISS.NS", "EDUCOMP.NS", "EICHERMOT.NS", "EIDPARRY.NS", "EIHAHOTELS.NS", "EIHOTEL.NS", "EIMCOELECO.NS", "EKC.NS", "ELAND.NS", "ELECON.NS", "ELECTCAST.NS", "ELECTHERM.NS", "ELGIEQUIP.NS", "ELGIRUBCO.NS", "EMAMILTD.NS", "EMAMIPAP.NS", "EMCO.NS", "EMKAY.NS", "EMMBI.NS", "ENDURANCE.NS", "ENERGYDEV.NS", "ENGINEERIN.NS", "ENGINERSIN.NS", "ENIL.NS", "EQUITAS.NS", "ERIS.NS", "EROSMEDIA.NS", "ESABINDIA.NS", "ESCORTS.NS", "ESSARSHPNG.NS", "ESTER.NS", "EUROMULTI.NS", "EUROTEXIND.NS", "EVEREADY.NS", "EVERESTIND.NS", "EXCEL.NS", "EXCELINDUS.NS", "EXIDEIND.NS", "FACT.NS", "FCL.NS", "FCONSUMER.NS", "FDC.NS", "FEDERALBNK.NS", "FIEMIND.NS", "FILATEX.NS", "FINCABLES.NS", "FINEORG.NS", "FINPIPE.NS", "FIRSTWIN.NS", "FLEXITUFF.NS", "FLFL.NS", "FLUOROCHEM.NS", "FMGOETZE.NS", "FMNL.NS", "FORCEMOT.NS", "FORTIS.NS", "FOSECOIND.NS", "FRETAIL", "HDFCBANK.NS", "RELIANCE.NS", "ICICIBANK.NS", "AXISBANK.NS", "SBIN.NS", "TATAMOTORS.NS", "KOTAKBANK.NS", "INFY.NS", "BAJFINANCE.NS", "INDUSINDBK.NS", "ADANIENT.NS", "TCS.NS", "LT.NS", "ITC.NS", "HINDUNILVR.NS", "TATASTEEL.NS", "HINDALCO.NS", "M_M.NS", "HDFC.NS", "HCLTECH.NS", "CIPLA.NS", "TITAN.NS", "MARUTI.NS", "INTELLECT.NS", "WIPRO.NS", "GLENMARK.NS", "BPCL.NS", "POLYCAB.NS", "BAJAJFINSV.NS", "DIVISLAB.NS", "BAJAJ_AUTO.NS", "BHARTIARTL.NS", "HAL.NS", "VEDL.NS", "HAVELLS.NS", "JSWSTEEL.NS", "TATAPOWER.NS", "TECHM.NS"]
tickers = [ 'MOREPENLAB.NS', 'PATELENG.NS', 'SKIPPER.NS', 'CAPACITE.NS', '360ONE.NS', 'AARTIIND.NS', 'AAVAS.NS', 'ACE.NS', 'AEGISLOG.NS', 'AETHER.NS', 'AFFLE.NS', 'APLLTD.NS', 'ALKYLAMINE.NS', 'ALLCARGO.NS', 'ALOKINDS.NS', 'ARE&M.NS', 'AMBER.NS', 'ANANDRATHI.NS', 'ANGELONE.NS', 'ANURAS.NS', 'APARINDS.NS', 'APTUS.NS', 'ACI.NS', 'ASAHIINDIA.NS', 'ASTERDM.NS', 'ASTRAZEN.NS', 'AVANTIFEED.NS', 'BEML.NS', 'BLS.NS', 'BALAMINES.NS', 'BALRAMCHIN.NS', 'BIKAJI.NS', 'BIRLACORPN.NS', 'BSOFT.NS', 'BLUEDART.NS', 'BLUESTARCO.NS', 'BBTC.NS', 'BORORENEW.NS', 'BRIGADE.NS', 'MAPMYINDIA.NS', 'CCL.NS', 'CESC.NS', 'CIEINDIA.NS', 'CSBBANK.NS', 'CAMPUS.NS', 'CANFINHOME.NS', 'CAPLIPOINT.NS', 'CGCL.NS', 'CASTROLIND.NS', 'CEATLTD.NS', 'CELLO.NS', 'CENTRALBK.NS', 'CDSL.NS', 'CENTURYPLY.NS', 'CENTURYTEX.NS', 'CERA.NS', 'CHALET.NS', 'CHAMBLFERT.NS', 'CHEMPLASTS.NS', 'CHENNPETRO.NS', 'CHOLAHLDNG.NS', 'CUB.NS', 'CLEAN.NS', 'COCHINSHIP.NS', 'CAMS.NS', 'CONCORDBIO.NS', 'CRAFTSMAN.NS', 'CREDITACC.NS', 'CROMPTON.NS', 'CYIENT.NS', 'DCMSHRIRAM.NS', 'DOMS.NS', 'DATAPATTNS.NS', 'DEEPAKFERT.NS', 'DUMMYSANOF.NS', 'EIDPARRY.NS', 'EIHOTEL.NS', 'EPL.NS', 'EASEMYTRIP.NS', 'ELECON.NS', 'ELGIEQUIP.NS', 'ENGINERSIN.NS', 'EQUITASBNK.NS', 'ERIS.NS', 'EXIDEIND.NS', 'FDC.NS', 'FINEORG.NS', 'FINCABLES.NS', 'FINPIPE.NS', 'FSL.NS', 'FIVESTAR.NS', 'GMMPFAUDLR.NS', 'GRSE.NS', 'GILLETTE.NS', 'GLS.NS', 'GLENMARK.NS', 'MEDANTA.NS', 'GPIL.NS', 'GODFRYPHLP.NS', 'GRANULES.NS', 'GRAPHITE.NS', 'GESHIP.NS', 'GAEL.NS', 'GMDCLTD.NS', 'GNFC.NS', 'GPPL.NS', 'GSFC.NS', 'GSPL.NS', 'HEG.NS', 'HBLPOWER.NS', 'HFCL.NS', 'HAPPSTMNDS.NS', 'HAPPYFORGE.NS', 'HSCL.NS', 'HINDCOPPER.NS', 'POWERINDIA.NS', 'HOMEFIRST.NS', 'HONASA.NS', 'HUDCO.NS', 'IDFC.NS', 'IIFL.NS', 'IRB.NS', 'IRCON.NS', 'ITI.NS', 'INDIACEM.NS', 'IBULHSGFIN.NS', 'INDIAMART.NS', 'IEX.NS', 'IOB.NS', 'INDIGOPNTS.NS', 'INOXWIND.NS', 'INTELLECT.NS', 'JBCHEPHARM.NS', 'JBMA.NS', 'JKLAKSHMI.NS', 'JKPAPER.NS', 'JMFINANCIL.NS', 'JAIBALAJI.NS', 'J&KBANK.NS', 'JINDALSAW.NS', 'JUBLINGREA.NS', 'JUBLPHARMA.NS', 'JWL.NS', 'JUSTDIAL.NS', 'JYOTHYLAB.NS', 'KNRCON.NS', 'KRBL.NS', 'KSB.NS', 'KPIL.NS', 'KARURVYSYA.NS', 'KAYNES.NS', 'KEC.NS', 'KFINTECH.NS', 'KIMS.NS', 'LATENTVIEW.NS', 'LXCHEM.NS', 'LEMONTREE.NS', 'MMTC.NS', 'MTARTECH.NS', 'MGL.NS', 'MAHSEAMLES.NS', 'MHRIL.NS', 'MAHLIFE.NS', 'MANAPPURAM.NS', 'MRPL.NS', 'MASTEK.NS', 'MEDPLUS.NS', 'METROPOLIS.NS', 'MINDACORP.NS', 'MOTILALOFS.NS', 'MCX.NS', 'NATCOPHARM.NS', 'NBCC.NS', 'NCC.NS', 'NLCINDIA.NS', 'NSLNISP.NS', 'NH.NS', 'NATIONALUM.NS', 'NAVINFLUOR.NS', 'NETWORK18.NS', 'NAM-INDIA.NS', 'NUVAMA.NS', 'NUVOCO.NS', 'OLECTRA.NS', 'PCBL.NS', 'PNBHOUSING.NS', 'PNCINFRA.NS', 'PVRINOX.NS', 'PPLPHARMA.NS', 'POLYMED.NS', 'PRAJIND.NS', 'PRINCEPIPE.NS', 'PRSMJOHNSN.NS', 'QUESS.NS', 'RRKABEL.NS', 'RBLBANK.NS', 'RHIM.NS', 'RITES.NS', 'RADICO.NS', 'RAILTEL.NS', 'RAINBOW.NS', 'RAJESHEXPO.NS', 'RKFORGE.NS', 'RCF.NS', 'RATNAMANI.NS', 'RTNINDIA.NS', 'RAYMOND.NS', 'REDINGTON.NS', 'RBA.NS', 'ROUTE.NS', 'SBFC.NS', 'SAFARI.NS', 'SANOFI.NS', 'SAPPHIRE.NS', 'SAREGAMA.NS', 'SCHNEIDER.NS', 'RENUKA.NS', 'SHYAMMETL.NS', 'SIGNATURE.NS', 'SOBHA.NS', 'SONATSOFTW.NS', 'SWSOLAR.NS', 'STLTECH.NS', 'SPARC.NS', 'SUNTECK.NS', 'SUVENPHAR.NS', 'SWANENERGY.NS', 'SYRMA.NS', 'TV18BRDCST.NS', 'TVSSCS.NS', 'TMB.NS', 'TANLA.NS', 'TATAINVEST.NS', 'TTML.NS', 'TEJASNET.NS', 'TITAGARH.NS', 'TRIDENT.NS', 'TRIVENI.NS', 'TRITURBINE.NS', 'UCOBANK.NS', 'UTIAMC.NS', 'UJJIVANSFB.NS', 'USHAMART.NS', 'VGUARD.NS', 'VIPIND.NS', 'VAIBHAVGBL.NS', 'VTL.NS', 'VARROC.NS', 'VIJAYA.NS', 'WELCORP.NS', 'WELSPUNLIV.NS', 'WESTLIFE.NS', 'WHIRLPOOL.NS', 'ZENSARTECH.NS', 'ECLERX.NS', 'ACC.NS', 'AUBANK.NS', 'ABCAPITAL.NS', 'ALKEM.NS', 'ASHOKLEY.NS', 'ASTRAL.NS', 'AUROPHARMA.NS', 'BALKRISIND.NS', 'BANDHANBNK.NS', 'BHARATFORG.NS', 'BHEL.NS', 'COFORGE.NS', 'CONCOR.NS', 'CUMMINSIND.NS', 'DALBHARAT.NS', 'DIXON.NS', 'ESCORTS.NS', 'FEDERALBNK.NS', 'GMRINFRA.NS', 'GODREJPROP.NS', 'GUJGASLTD.NS', 'HDFCAMC.NS', 'HINDPETRO.NS', 'IDFCFIRSTB.NS', 'INDHOTEL.NS', 'INDUSTOWER.NS', 'JUBLFOOD.NS', 'LTF.NS', 'LTTS.NS', 'LUPIN.NS', 'MRF.NS', 'M&MFIN.NS', 'MFSL.NS', 'MAXHEALTH.NS', 'MPHASIS.NS', 'NMDC.NS', 'OBEROIRLTY.NS', 'OFSS.NS', 'PIIND.NS', 'PAGEIND.NS', 'PERSISTENT.NS', 'PETRONET.NS', 'POLYCAB.NS', 'SAIL.NS', 'SUZLON.NS', 'TATACOMM.NS', 'TIINDIA.NS', 'UPL.NS', 'IDEA.NS', 'YESBANK.NS']
#tickers = ['ICICIBANK.NS', 'ADANIENT.NS']
start_date = "2011-11-01"
#end_date = "2024-02-04"
end_dates = ["2024-06-01","2024-06-02","2024-06-03","2024-06-04","2024-06-05","2024-06-06","2024-06-07","2024-06-08","2024-06-09","2024-06-10","2024-06-11","2024-06-12","2024-06-13","2024-06-14","2024-06-17","2024-06-18","2024-06-19","2024-06-20","2024-06-21","2024-06-22","2024-06-23","2024-06-24","2024-06-25","2024-06-26","2024-06-27","2024-06-28","2024-06-29","2024-06-30"]
#,"2024-03-23","2024-03-24","2024-03-25","2024-03-26","2024-03-27","2024-03-28","2024-03-29","2024-03-30","2024-02-01","2024-02-02","2024-02-03","2024-02-04","2024-02-05","2024-02-06","2024-02-07","2024-02-08","2024-02-09","2024-02-10","2024-02-11","2024-02-12","2024-02-13","2024-02-14","2024-02-15","2024-02-16","2024-02-17","2024-02-18","2024-02-19","2024-02-20"

overall_data = []

for end_date in end_dates:
    for ticker in tickers:
        data = yf.download(ticker, start = start_date, end = end_date)
        
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

        # Calculate the highest high and lowest low over the lookback period for Aroon Up and Aroon Down
        data['high_period'] = data['High'].rolling(window=aroon_window+1).apply(lambda x: np.argmax(x), raw=True) + 1
        data['low_period'] = data['Low'].rolling(window=aroon_window+1).apply(lambda x: np.argmin(x), raw=True) + 1

        # Calculate Aroon Up and Aroon Down
        data['aroon_up'] = ((aroon_window - data['high_period']) / aroon_window) * 100
        data['aroon_down'] = ((aroon_window - data['low_period']) / aroon_window) * 100

        # Define the window size for RSI
        rsi_window = 14

        # Calculate the daily price change
        delta = data['Close'].diff()

        # Define the gain and loss for up and down days
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        # Calculate the rolling mean of gain and loss over the lookback period
        avg_gain = gain.rolling(window=rsi_window).mean()
        avg_loss = loss.rolling(window=rsi_window).mean()

        # Calculate the relative strength
        rs = avg_gain / avg_loss

        # Calculate the RSI
        data['rsi'] = 100 - (100 / (1 + rs))

        # Define BUY/SELL signals
        data['buy_signal'] = ((data['Close'] < data['lower_band']) & (data['aroon_up'] > data['aroon_down']) & (data['rsi'] < 30))
        data['sell_signal'] = ((data['Close'] > data['upper_band']) & (data['aroon_down'] > data['aroon_up']) & (data['rsi'] > 70))

        data = data.dropna()
        last_row = data.tail(1)

        overall_data.append(last_row)

    dfs = pd.concat(overall_data)

    datas = []
    datas = dfs
    datas = datas.drop(['Open', 'High', 'Low', 'Adj Close', 'Volume', 'upper_band', 'lower_band', 'middle_band', 'high_period', 'low_period', 'aroon_up', 'aroon_down', 'rsi'], axis = 1)

    '''with pd.option_context('display.max_rows', None,
                        'display.max_columns', None,
                        'display.precision', 3,
                        ):
        print(datas)'''

    buy_dataframe = datas[datas['buy_signal'] == True]
    #print("BUY:")
    #buy_dataframe = buy_dataframe.drop(['buy_signal', 'sell_signal'], axis = 1)
    buy_dataframe = [buy_dataframe]
    #buy_d = buy_dataframe[buy_dataframe['Close'] >= 600]

    sell_dataframe = datas[datas['sell_signal'] == True]
    #print("SELL")
    #sell_dataframe = sell_dataframe.drop(['Close', 'buy_signal', 'sell_signal'], axis = 1)
    sell_dataframe = [sell_dataframe]


print()
with pd.option_context('display.max_rows', None,
                        'display.max_columns', None,
                        'display.precision', 3,
                        ):
        print(buy_dataframe)

print()
with pd.option_context('display.max_rows', None,
                        'display.max_columns', None,
                        'display.precision', 3,
                        ):
        print(sell_dataframe)