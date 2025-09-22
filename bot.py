from ib_insync import *
import pandas as pd

# ---------- FETCH AND CLEAN DATA FOR NAS100

# CONNECT TO TWS
ib = IB()
ib.connect("127.0.0.1", 7497, clientId=1)

# CONTRACT DEFINITION
contract = ContFuture('NQ', exchange='CME')

# CANDLES REQUEST - 5 MINUTE CANDLES, LAST 1 MONTH
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

# CONVERT TO PANDAS DATAFRAME TO ACCESS THE COLUMNS I NEED + FIND NAN VALUES
df = util.df(bars)
# print(type(df))

# print(df.isna().sum()) # check isNan values, there are no Nan values

# ------------------------------ STRAT LOGIC ------------------------------

# CONVERT FROM RANGE INDEX TO DATE INDEX
df["date"] = pd.to_datetime(df["date"])
print(type(df["date"]))
print(df["date"].index)
df.set_index('date', inplace=True)

# GET JUST DATA FROM 10 AM EST TO 11 AM EST
session_timeselect = df.between_time("10:00", "10:55")
print(type(session_timeselect))
print(session_timeselect)

# FIND GAPS BETWEEN HIGH AND LOW OF 1 AND 3 CANDLE, POKUD JE > 0 VRÁTÍ TRUE

# OMEZIT ČAS NA LOOP NA 10 AM EST - 11 AM EST

# POKUD CENA PO VYTVOŘENÍ TÉTO MEZERY DOSÁHNE HIGH CENY OR LOW CENY TÉTO MEZERY = TRUE
    
        #POKUD JE LOW PRICE VĚTŠÍ JAK HIGH PRICE = BUY

        # JINAK SELL 

# POKUD BUY = ČEKÁME AŽ CLOSE DALŠÍ SVÍČKY BUDE VĚTŠÍ NEŽ HIGH PŘEDCHOZÍ SVÍČKY
# POKUD SELL = ČEKÁME AŽ CLOSE DALŠÍ SVÍČKY BUDE MENŠÍ NEŽ LOW PŘEDCHOZÍ SVÍČKY

# OTEVŘENÍ POZICE - POKUD BUY - OTEVŘENÍ NA HIGH PŘEDCHOZÍ SVÍČKY PO UZAVŘENÍ DALŠÍ SVÍČKY
                    # POKUD SELL - OTEVŘENÍ NA LOW PŘEDCHOZÍ SVÍČKY PO UZAVŘENÍ DALŠÍ SVÍČKY
        
        # STOP LOSS - POKUD BUY - STOP LOSS O 1 PIP POD LOW PŘEDCHOZÍ NEBO DALŠÍ SVÍČKY (ZKONTROLOVAT OBOJÍ)  
                    # POKUD SELL - STOP LOSS O 1 PIP NAD HIGH PŘEDCHOZÍ NEBO DALŠÍ SVÍČKY (ZKONTROLOVAT OBOJÍ)

        # TAKE PROFIT - zatím neřešit