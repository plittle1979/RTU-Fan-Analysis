import sqlite3
import pandas as pd

# === CONFIG ===
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
table_name = "RTU 2-1 Inside Air Fans IAF01 Fan Internal Temp"
date_range = ("6/1/2024", "8/1/2024")
excel_output = "C:/sqlite/RTU_Fan_Analysis/rtu_2_1_IAF01_anomalies.xlsx"

# === CONNECT ===
conn = sqlite3.connect(db_path)

# === QUERY ONLY ANOMALOUS ROWS ===
query = f"""
SELECT Date, Value AS Temp,
       ROUND(AVG(Value) OVER (
           ORDER BY Date
           ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
       ), 2) AS RunningAvg,
       ROUND(Value - AVG(Value) OVER (
           ORDER BY Date
           ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
       ), 2) AS Deviation
FROM "{table_name}"
WHERE Date >= ? AND Date < ?
"""

df = pd.read_sql_query(query, conn, params=date_range)
conn.close()

# === FILTER ONLY ANOMALIES ===
df = df[pd.to_numeric(df['Deviation'], errors='coerce').abs() > 5]

# === EXPORT ===
df.to_excel(excel_output, index=False)
print(f"✅ Exported anomalies to: {excel_output}")
