import sqlite3
import pandas as pd
import os

# === Setup ===
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
output_csv = "C:/sqlite/RTU_Fan_Analysis/rtu_2_1_gd_june_july_debugged.csv"

tables = [
    ("RTU 2-1 General Data Trends SA Temp", "SA_Temp"),
    ("RTU 2-1 General Data Trends RAT", "RAT"),
    ("RTU 2-1 General Data Trends OAT", "OAT")
]

conn = sqlite3.connect(db_path)
all_data = pd.DataFrame()

for table_name, column_alias in tables:
    print(f"🔍 Loading: {table_name}")

    query = f"""
        SELECT Date, Value
        FROM "{table_name}"
        WHERE Date LIKE '6/%/2024%' OR Date LIKE '7/%/2024%'
    """

    df = pd.read_sql_query(query, conn)

    # Clean and parse dates robustly
    original_count = len(df)
    df['Date'] = df['Date'].str.strip().str.replace("EDT", "", regex=False).str.replace("CDT", "", regex=False)
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

    # Convert value to numeric
    df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
    df = df.dropna(subset=['Date'])

    parsed_count = len(df)
    print(f"✅ {column_alias}: {parsed_count}/{original_count} rows parsed")

    # Rename and merge
    df = df.rename(columns={'Value': column_alias})
    if all_data.empty:
        all_data = df
    else:
        all_data = pd.merge(all_data, df, on='Date', how='outer')

# Final sort
all_data = all_data.sort_values(by='Date')
conn.close()

# Export
all_data.to_csv(output_csv, index=False)
print(f"\n✅ Exported fixed dataset to: {output_csv}")
