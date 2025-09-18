from ib_insync import *
import pandas as pd
from ib_insync import Future

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
def data_fetch(bars):
    if bars:
        df = util.df(bars)
        print(df)
    else:
        print("No data returned")

data_fetch(bars)