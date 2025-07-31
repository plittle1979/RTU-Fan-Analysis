# export_rtu_6_1_fan_temps_june_july.py

import sqlite3
import pandas as pd
import os

# === CONFIG ===
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
csv_output = "C:/sqlite/RTU_Fan_Analysis/rtu_6_1_fan_temps_june_july.csv"
excel_output = "C:/sqlite/RTU_Fan_Analysis/rtu_6_1_fan_temps_june_july.xlsx"

fan_types = [("Inside Air Fans", "IAF"), ("Outside Air Fans", "OAF")]
fan_ids = [f"{i:02}" for i in range(1, 9)]
date_range = ("6/1/2024", "8/1/2024")

# === CONNECT ===
conn = sqlite3.connect(db_path)
all_data = pd.DataFrame()

# === QUERY EACH FAN ===
for fan_type, fan_prefix in fan_types:
    for fan_id in fan_ids:
        table = f"RTU 6-1 {fan_type} {fan_prefix}{fan_id} Fan Internal Temp"
        try:
            query = f"""
                SELECT Date, Value AS Temp
                FROM "{table}"
                WHERE Date >= ? AND Date < ?
            """
            df = pd.read_sql_query(query, conn, params=date_range)
            df['Date'] = pd.to_datetime(df['Date'].str.replace(" EDT", "", regex=False), errors='coerce')
            df['Temp'] = pd.to_numeric(df['Temp'], errors='coerce')
            df.dropna(subset=['Date'], inplace=True)
            df = df.rename(columns={'Temp': f'{fan_prefix}{fan_id}'})
            if all_data.empty:
                all_data = df
            else:
                all_data = pd.merge(all_data, df, on='Date', how='outer')
            print(f"✅ Pulled: {table}")
        except Exception as e:
            print(f"⚠️ Failed: {table} — {e}")

conn.close()

# === EXPORT FILES ===
all_data.sort_values(by='Date', inplace=True)
all_data.to_csv(csv_output, index=False)
all_data.to_excel(excel_output, index=False)

print(f"\n✅ CSV Exported to: {csv_output}")
print(f"✅ Excel Exported to: {excel_output}")
