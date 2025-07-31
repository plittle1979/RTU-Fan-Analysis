# plot_all_fans_temp_only.py

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# === Setup ===
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
output_dir = "C:/sqlite/RTU_Fan_Analysis/Fan_Temp_Charts_Only"
os.makedirs(output_dir, exist_ok=True)

# === Configuration ===
rtus = ["2-1", "3-4", "6-1"]
fan_types = [("Inside Air Fans", "IAF"), ("Outside Air Fans", "OAF")]
fan_ids = [f"{i:02}" for i in range(1, 9)]  # 01 through 08

# === Connect to DB ===
conn = sqlite3.connect(db_path)

# === Loop through all RTUs and Fans ===
for rtu in rtus:
    for fan_type, fan_prefix in fan_types:
        for fan_id in fan_ids:
            table_name = f'RTU {rtu} {fan_type} {fan_prefix}{fan_id} Fan Internal Temp'

            try:
                # SQL query to get just temperature data
                query = f"""
                SELECT
                    Date,
                    Value AS Temp
                FROM "{table_name}"
                WHERE Date >= '6/1/2024' AND Date < '8/1/2024'
                """

                df = pd.read_sql_query(query, conn)

                # Clean up data
                df['Date'] = pd.to_datetime(df['Date'].str.replace(" EDT", "", regex=False), errors='coerce')
                df['Temp'] = pd.to_numeric(df['Temp'], errors='coerce')
                df = df.dropna(subset=['Date', 'Temp'])

                # Plot
                plt.figure(figsize=(14, 6))
                plt.plot(df['Date'], df['Temp'], label='Temperature', linewidth=1.5)

                plt.xlabel("Date")
                plt.ylabel("Temperature (°F)")
                plt.title(f"RTU {rtu} {fan_prefix}{fan_id} Internal Temp – June 2024")
                plt.grid(True)
                plt.tight_layout()

                # Y-axis scaling: 0 to 10% above max temp
                y_min = 0
                y_max = df['Temp'].max() * 1.10
                plt.ylim(y_min, y_max)

                # Save chart
                filename = f"RTU_{rtu.replace('-', '_')}_{fan_prefix}{fan_id}_TempOnly.png"
                plt.savefig(os.path.join(output_dir, filename))
                plt.close()

                print(f"✅ Saved: {filename}")

            except Exception as e:
                print(f"⚠️ Skipped: {table_name} — {e}")

# === Done ===
conn.close()
print("\nAll temperature-only charts generated.")
