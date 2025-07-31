import sqlite3
import pandas as pd

# === Setup ===
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
output_csv = "C:/sqlite/RTU_Fan_Analysis/rtu_2_1_gd_extended_june_july.csv"

# General Data Trend fields to extract
tables_to_include = {
    "SA Temp": "SA_Temp",
    "RAT": "RAT",
    "OAT": "OAT",
    "C1 Enable": "C1_Enable",
    "C1 Spd Reference": "C1_Spd_Ref",
    "C2 Spd Reference": "C2_Spd_Ref",
    "UPS Power Loss": "UPS_Power_Loss"
}

# Connect to SQLite
conn = sqlite3.connect(db_path)
all_data = pd.DataFrame()

for raw_name, clean_name in tables_to_include.items():
    table_name = f"RTU 2-1 General Data Trends {raw_name}"
    try:
        query = f"""
        SELECT Date, Value
        FROM "{table_name}"
        WHERE Date >= '6/1/2024' AND Date < '8/1/2024'
        """
        df = pd.read_sql_query(query, conn)
        df['Date'] = pd.to_datetime(df['Date'].str.replace(" EDT", "", regex=False), errors='coerce')
        df = df.rename(columns={'Value': clean_name})
        df.dropna(subset=['Date'], inplace=True)

        if all_data.empty:
            all_data = df
        else:
            all_data = pd.merge(all_data, df, on='Date', how='outer')

        print(f"✅ Loaded: {table_name} — {len(df)} rows")

    except Exception as e:
        print(f"⚠️ Failed to process {table_name}: {e}")

conn.close()

# Sort and Export
all_data = all_data.sort_values(by='Date')
all_data.to_csv(output_csv, index=False)
print(f"\n✅ Saved to: {output_csv}")
