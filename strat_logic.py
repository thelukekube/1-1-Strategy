import data
import pandas as pd


# -------------------------------------------------------- STRATEGY LOGIC ----------------------------------------------------------
# FUNCTION TO IDENTIFY GAPS IN ANY THREE CONSECUTIVE CANDLES OF EACH DAY'S SESSION
# ---------------------------------------------------------------------------------
"""class Strategy:
    def __init__(self, df, bullish_gap, bearish_gap, gap_detected):
        self.df = df
        self.bullish_gap = bullish_gap
        self.bearish_gap = bearish_gap
        self.gap_detected = gap_detected
"""
def session_gap_detect(df):
    one_day_gap = df.groupby(df.index.date)
    results = []

    print(f"\nTotal days to process: {len(one_day_gap)}")
    for date, gap in one_day_gap:
        # print(f"\nProcessing session for date: {date} ({data.candles_in_range[date]} candles)")
        # -----------------------------------------------------------
        # CHECK IF THERE ARE AT LEAST 3 CANDLES = FORMATION NECESSITY
        # -----------------------------------------------------------
        if len(gap) < 3:
            print(f"Error: Fewer than 3 candles in session for {date}. Skipping.")
            results.append((date, 'no_gap', 0, "Insufficient candles", None, None))
            continue
        else:
            gap_detected = False
        # -----------------------------------------------
        # ITERATION TO GO THROUGH ALL POSSIBLE FORMATIONS
        # -----------------------------------------------
        for i in range(len(gap) - 2):
            first_candle = gap.iloc[i]
            third_candle = gap.iloc[i+2]
            first_time = gap.index[i]
            third_time = gap.index[i+2]
            # ---------------
            # CANDLE DETAILS
            # ---------------
            #print(f"Checking formation starting at candle {i+1} (times: {first_time} to {third_time})")
            #print(f"First candle: High={first_candle['high']:.2f}, Low={first_candle['low']:.2f}")
            #print(f"Third candle: High={third_candle['high']:.2f}, Low={third_candle['low']:.2f}")

            # --------------
            # GAPS VARIABLES
            # --------------
            bullish_gap = third_candle["low"] > first_candle["high"]
            bearish_gap = third_candle["high"] < first_candle["low"]
            
            # --------------------
            # BULLISH GAP (UPSIDE)
            # --------------------
            if bullish_gap:
                gap_size = third_candle["low"] - first_candle["high"]
                print(f"Bullish gap detected with size {gap_size:.2f} at {first_time} to {third_time}.")
                results.append((date, 'bullish', gap_size, "Valid gap", first_time, third_time))
                gap_detected = True
                break
            # ----------------------
            # BEARISH GAP (DOWNSIDE)
            # ----------------------
            elif bearish_gap:
                gap_size = first_candle["low"] - third_candle["high"]
                print(f"Bearish gap detected with size {gap_size:.2f} at {first_time} to {third_time}.")
                results.append((date, 'bearish', gap_size, "Valid gap", first_time, third_time))
                gap_detected = True
                break

        if not gap_detected:
            print("No gaps detected in any formations for this day.")
            results.append((date, 'no_gap', 0, "No gaps found", None, None))

    print("\nFinished processing all dates.")
    return results

detected_gaps = session_gap_detect(data.session_timeselect)

# ----------------------------------------
# CONVERT CREATED GAPS TO PANDAS DATAFRAME
# ----------------------------------------
dataframe_detected_gaps = pd.DataFrame(detected_gaps)
print(type(dataframe_detected_gaps))
print(dataframe_detected_gaps[1])

# ----------------------------------------------------------------------------------------------------------
# AFTER THE GAP IS FORMED -> CHECK IF WAS FORMED OR NOT -> IF YES THAN IT WILL ACT BASED ON THE TYPE OF GAP
# ----------------------------------------------------------------------------------------------------------
