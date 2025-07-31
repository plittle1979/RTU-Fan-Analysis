import sqlite3
import pandas as pd
import os

# Connect to the database
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
conn = sqlite3.connect(db_path)

# Configuration
fan_types = [("Inside Air Fans", "IAF"), ("Outside Air Fans", "OAF")]
fan_ids = [f"{i:02}" for i in range(1, 9)]  # 01–08
rtu = "2-1"

# Dictionary to hold each fan's DataFrame
fan_dataframes = []

for fan_type, prefix in fan_types:
    for fan_id in fan_ids:
        table_name = f'RTU {rtu} {fan_type} {prefix}{fan_id} Fan Internal Temp'
        try:
            query = f"""
            SELECT Date, Value AS Temp
            FROM "{table_name}"
            WHERE Date >= '6/1/2024' AND Date < '7/1/2024'
            """
            df = pd.read_sql_query(query, conn)

            # Clean and rename columns
            df['Date'] = pd.to_datetime(df['Date'].str.replace(" EDT", "", regex=False), errors='coerce')
            df['Temp'] = pd.to_numeric(df['Temp'], errors='coerce')
            df = df.dropna(subset=['Date'])
            df = df.rename(columns={'Temp': f'{prefix}{fan_id} Temp'})

            # Drop duplicate dates if any
            df = df.drop_duplicates(subset='Date')

            fan_dataframes.append(df[['Date', f'{prefix}{fan_id} Temp']])

        except Exception as e:
            print(f"⚠️ Skipped: {table_name} — {e}")

# Merge all dataframes on Date
from functools import reduce
df_merged = reduce(lambda left, right: pd.merge(left, right, on='Date', how='outer'), fan_dataframes)

# Sort by Date
df_merged = df_merged.sort_values('Date')

# Save to CSV
output_path = "C:/sqlite/RTU_Fan_Analysis/RTU_2_1_AllFans_Temps_Wide.csv"
df_merged.to_csv(output_path, index=False)
print(f"✅ Exported: {output_path}")

# Close DB
conn.close()
