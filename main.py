import strat_logic
import data
import trade_exe

detected_gaps = strat_logic.session_gap_detect(data.session_timeselect)

# ------------------------------
# SUMMARY PRINT
# ------------------------------
print("\nSummary of detected gaps:")
if not detected_gaps:
    print("No gaps detected in any sessions.")
else:
    for date, gap_type, size, remark, start_time, end_time in detected_gaps:
        time_range = f" ({start_time} to {end_time})" if start_time else ""
        print(f"{date}: {gap_type} gap, Size: {size:.2f}, Remark: {remark}{time_range}")