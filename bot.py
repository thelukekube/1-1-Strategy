from ib_insync import *
import pandas as pd

# ------------------------------ DATA HANDLING / FETCH, CONTRACTS, API CONNECT ------------------------------
# CONNECT TO TWS
# ------------------------------ 
ib = IB()
ib.connect("127.0.0.1", 7497, clientId=1)

# ------------------------------ 
# CONTRACT DEFINITION
# ------------------------------ 
contract = ContFuture('NQ', exchange='CME')

# ------------------------------ 
# CANDLES REQUEST - 5 MINUTE CANDLES, LAST 1 MONTH
# ------------------------------ 
bars = ib.reqHistoricalData(
    contract,
    endDateTime='',
    durationStr='1 M',
    barSizeSetting='5 mins',
    whatToShow='TRADES',
    useRTH=True,
    formatDate=1,
)
# print(type(bars))

# ------------------------------ 
# CONVERT TO PANDAS DATAFRAME TO ACCESS THE COLUMNS I NEED + FIND NAN VALUES
# ------------------------------ 

df = util.df(bars)
# print(type(df))

# print(df.isna().sum()) # check isNan values, there are no Nan values

# ------------------------------ 
# CONVERT FROM RANGE INDEX TO DATE INDEX
# ------------------------------
df["date"] = pd.to_datetime(df["date"])
# print(type(df["date"]))
# print(df["date"].index)
df.set_index('date', inplace=True)

# ------------------------------
# GET JUST DATA FROM 10 AM EST TO 11 AM EST
# ------------------------------
session_timeselect = df.between_time("10:00", "10:55")
# print(type(session_timeselect))
# print(session_timeselect)

# -------------------------------------------------------- STRATEGY LOGIC ----------------------------------------------------------
## Looking for the first 3 candles formation - There needs to be gap between 1st and 3rd candle to be valid setup (downside/upside)
# ----------------------------------------------------------------------------------------------------------------------------------
# FUNCTION TO IDENTIFY FORMED GAP FROM 3 CANDLES
# ------------------------------
def detect_gap(df):
    # ------------------------------
    # CHECK IF THERE ARE AT LEAST 3 CANDLES TO CHECK THE SETUP
    # ------------------------------
    if len(df) < 3:
        print("Error: Fewer than 3 candles in the session. Cannot check gaps.")
        return False
    # ------------------------------
    # ACCESS THE 1ST AND 3RD CANDLE FROM THE SESSION
    # ------------------------------
    first_candle = df.iloc[0]
    third_candle = df.iloc[2]

    # ------------------------------
    # 1ST SCENARIO - BULLISH (UPSIDE) GAP FORMED
    # ------------------------------
    bullish_gap = first_candle["high"] - third_candle["low"]
    if bullish_gap > 0:
        print("Bullish gap detected.")
    else:
        print("Bullish gap NOT detected.")
    
    # ------------------------------
    # 2ND SCENARIO - BEARISH (DOWNSIDE) GAP FORMED
    # ------------------------------
    bearish_gap = third_candle["low"] - first_candle["high"]
    if bearish_gap > 0:
        print("Bearish gap detected.")
    else:
        print("Bearish gap NOT detected.")
    # ------------------------------
    # IF ANY GAP WAS FORMED RETURN TRUE
    # ------------------------------
    if bullish_gap or bearish_gap:
        return True
    else:
        return False

detect_gap(df)

# ------------------------------
# FUNCTION TO BE LOOKING FOR THE GAP IN WHOLE INTERVAL FROM 10 AM EST TO 10:55 EST
# ------------------------------



# OTEVŘENÍ POZICE - POKUD BUY - OTEVŘENÍ NA HIGH PŘEDCHOZÍ SVÍČKY PO UZAVŘENÍ DALŠÍ SVÍČKY
                    # POKUD SELL - OTEVŘENÍ NA LOW PŘEDCHOZÍ SVÍČKY PO UZAVŘENÍ DALŠÍ SVÍČKY
        
        # STOP LOSS - POKUD BUY - STOP LOSS O 1 PIP POD LOW PŘEDCHOZÍ NEBO DALŠÍ SVÍČKY (ZKONTROLOVAT OBOJÍ)  
                    # POKUD SELL - STOP LOSS O 1 PIP NAD HIGH PŘEDCHOZÍ NEBO DALŠÍ SVÍČKY (ZKONTROLOVAT OBOJÍ)

        # TAKE PROFIT - zatím neřešit