# export_sa_temp_to_csv.py

import sqlite3
import pandas as pd

# Connect to the database
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
conn = sqlite3.connect(db_path)

# SQL query
query = """
SELECT
    Date,
    Value AS Temp
FROM "RTU 2-1 General Data Trends SA Temp"
WHERE Date >= '6/1/2024' AND Date < '7/1/2024'
"""

# Load and clean the data
df = pd.read_sql_query(query, conn)
conn.close()

df['Date'] = pd.to_datetime(df['Date'].str.replace(" EDT", "", regex=False), errors='coerce')
df['Temp'] = pd.to_numeric(df['Temp'], errors='coerce')
df.dropna(subset=['Date', 'Temp'], inplace=True)

# Export to CSV
df.to_csv("C:/sqlite/RTU_Fan_Analysis/2-1_GD_SA_Temp.csv", index=False)

print("✅ CSV export complete.")
