import sqlite3
import pandas as pd
import os

# === Setup ===
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
output_csv = "C:/sqlite/RTU_Fan_Analysis/rtu_fan_analysis_all_internal_temps.csv"

rtus = ["2-1", "3-4", "6-1"]
fan_types = [("Inside Air Fans", "IAF"), ("Outside Air Fans", "OAF")]
fan_ids = [f"{i:02}" for i in range(1, 9)]

conn = sqlite3.connect(db_path)
all_data = []

for rtu in rtus:
    for fan_type, fan_prefix in fan_types:
        for fan_id in fan_ids:
            table_name = f'RTU {rtu} {fan_type} {fan_prefix}{fan_id} Fan Internal Temp'
            try:
                query = f"""
                SELECT Date, Value AS Temp
                FROM "{table_name}"
                WHERE Date >= '6/1/2024' AND Date < '7/1/2024'
                """
                df = pd.read_sql_query(query, conn)
                df['RTU'] = rtu
                df['FanType'] = fan_type
                df['FanID'] = f"{fan_prefix}{fan_id}"
                all_data.append(df)
            except Exception as e:
                print(f"Skipped {table_name} — {e}")

conn.close()

combined_df = pd.concat(all_data, ignore_index=True)
combined_df['Date'] = pd.to_datetime(combined_df['Date'].str.replace(" EDT", "", regex=False), errors='coerce')
combined_df['Temp'] = pd.to_numeric(combined_df['Temp'], errors='coerce')
combined_df.dropna(subset=['Date', 'Temp'], inplace=True)

combined_df.to_csv(output_csv, index=False)
print(f"✅ Saved to: {output_csv}")
