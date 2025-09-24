from ib_insync import *
import pandas as pd

# ------------------------------ DATA HANDLING / FETCH, CONTRACT, API CONNECT ------------------------------
# CONNECT TO TWS
# ------------------------------
ib = IB()
try:
    ib.connect("127.0.0.1", 7497, clientId=1)
except Exception as e:
    print(f"Error connecting to TWS: {e}")
    exit()

# ------------------------------
# CONTRACT DEFINITION
# ------------------------------
contract = ContFuture('NQ', exchange='CME')

# ------------------------------
# CANDLES REQUEST - 5 MINUTE CANDLES, LAST 1 MONTH
# ------------------------------
try:
    bars = ib.reqHistoricalData(
        contract,
        endDateTime='',
        durationStr='1 M',
        barSizeSetting='5 mins',
        whatToShow='TRADES',
        useRTH=True,
        formatDate=1,
    )
except Exception as e:
    print(f"Error fetching historical data: {e}")
    ib.disconnect()
    exit()

if not bars:
    print("No historical data returned.")
    ib.disconnect()
    exit()

# ------------------------------
# CONVERT TO PANDAS DATAFRAME
# ------------------------------
df = util.df(bars)
if df.empty:
    print("Dataframe is empty.")
    ib.disconnect()
    exit()

# ------------------------------
# CONVERT TO DATETIME INDEX
# ------------------------------
df["date"] = pd.to_datetime(df["date"])
df.set_index('date', inplace=True)
# ------------------------------
# RIGHT TIMEZONE CHECK
# ------------------------------
try:
    df.index = df.index.tz_localize('US/Eastern') if df.index.tz is None else df.index.tz_convert('US/Eastern')
except Exception as e:
    print(f"Error handling timezone: {e}")

# ------------------------------
# GET DATA FROM 10:00 AM EST TO 10:55 AM EST
# ------------------------------
session_timeselect = df.between_time("10:00", "10:55")
if session_timeselect.empty:
    print("No data available for 10:00 to 10:55 sessions.")
    ib.disconnect()
    exit()

# ------------------------------
# COUNT 5-MINUTE CANDLES PER DAY
# ------------------------------
candles_in_range = session_timeselect.groupby(session_timeselect.index.date).size()
print(f"\nTotal number of candles across all days: {len(session_timeselect)}")