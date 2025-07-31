import sqlite3
import pandas as pd
import os

# === Setup ===
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
output_csv = "C:/sqlite/RTU_Fan_Analysis/rtu_2_1_gd_june_july.csv"
gd_tables = {
    "SA Temp": "SA_Temp",
    "RAT": "RAT",
    "OAT": "OAT"
}

# === Connect ===
conn = sqlite3.connect(db_path)

# === Empty master dataframe ===
all_data = pd.DataFrame()

# === Loop through general data trend tables ===
for suffix, column_name in gd_tables.items():
    table_name = f"RTU 2-1 General Data Trends {suffix}"
    try:
        query = f"""
        SELECT Date, Value
        FROM "{table_name}"
        WHERE Date >= '6/1/2024' AND Date < '8/1/2024'
        """
        df = pd.read_sql_query(query, conn)
        df['Date'] = pd.to_datetime(df['Date'].str.replace(" EDT", "", regex=False), errors='coerce')
        df[column_name] = pd.to_numeric(df['Value'], errors='coerce')
        df = df.drop(columns=['Value'])
        df = df.dropna(subset=['Date'])

        # Merge
        if all_data.empty:
            all_data = df
        else:
            all_data = pd.merge(all_data, df, on='Date', how='outer')

        print(f"✅ Pulled: {table_name} — {len(df)} rows loaded")

    except Exception as e:
        print(f"⚠️ Failed: {table_name} — {e}")

conn.close()

# === Sort and forward-fill ===
all_data = all_data.sort_values(by='Date')
all_data.fillna(method='ffill', inplace=True)

# === Export ===
all_data.to_csv(output_csv, index=False)
print(f"\n✅ Saved to: {output_csv}")