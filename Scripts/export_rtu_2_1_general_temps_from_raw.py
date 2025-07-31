import pandas as pd
import os

# === CONFIG ===
input_file = "C:/sqlite/RTU_Fan_Analysis/Raw Data/RTU 2-1 General Data Trends.xlsx"
csv_output = "C:/sqlite/RTU_Fan_Analysis/rtu_2_1_general_temps_june_july.csv"
excel_output = "C:/sqlite/RTU_Fan_Analysis/rtu_2_1_general_temps_june_july.xlsx"
sheets = {
    "OAT": "MCC1 / MCC1 Mechanical / 1st Floor Mechanical / Computer Rooms / Computer Room 2 / Cell 1 / CR2 RTU 1 / OAT",
    "RAT": "MCC1 / MCC1 Mechanical / 1st Floor Mechanical / Computer Rooms / Computer Room 2 / Cell 1 / CR2 RTU 1 / RAT",
    "SA Temp": "MCC1 / MCC1 Mechanical / 1st Floor Mechanical / Computer Rooms / Computer Room 2 / Cell 1 / CR2 RTU 1 / SA Temp",
}

# === PROCESS ===
all_data = pd.DataFrame()
for sheet_name, col_name in sheets.items():
    try:
        df = pd.read_excel(input_file, sheet_name=sheet_name, usecols=[0, 1])
        df.columns = ["Date", "Temp"]
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df['Temp'] = pd.to_numeric(df['Temp'], errors='coerce')
        df.dropna(subset=['Date', 'Temp'], inplace=True)
        df = df[(df['Date'] >= '2024-06-01') & (df['Date'] < '2024-08-01')]
        df.rename(columns={"Temp": sheet_name}, inplace=True)

        if all_data.empty:
            all_data = df
        else:
            all_data = pd.merge(all_data, df, on="Date", how="outer")

        print(f"✅ Pulled: {sheet_name}")
    except Exception as e:
        print(f"⚠️ Failed to process sheet '{sheet_name}': {e}")

# === SAVE ===
all_data.sort_values("Date", inplace=True)
all_data.to_csv(csv_output, index=False)
all_data.to_excel(excel_output, index=False)

print(f"\n✅ Saved to:\n  CSV:   {csv_output}\n  Excel: {excel_output}")
