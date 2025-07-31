# 2-1_GD_SA_Temp.py

import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the database
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
conn = sqlite3.connect(db_path)

# SQL query to get just temperature data
query = """
SELECT
    Date,
    Value AS Temp
FROM "RTU 2-1 General Data Trends SA Temp"
WHERE Date >= '6/1/2024' AND Date < '7/1/2024'
"""

# Load the data
df = pd.read_sql_query(query, conn)
conn.close()

# Convert columns
df['Date'] = pd.to_datetime(df['Date'].str.replace(" EDT", "", regex=False), errors='coerce')
df['Temp'] = pd.to_numeric(df['Temp'], errors='coerce')

# Plot
plt.figure(figsize=(14, 6))
plt.plot(df['Date'], df['Temp'], label='Temperature', linewidth=1.5)

plt.xlabel("Date")
plt.ylabel("Temperature (°F)")
plt.title("RTU 2-1 General Data – SA Temp (June 2024)")
plt.grid(True)
plt.tight_layout()

# Y-axis: 0 to 10% above max
y_min = 0
y_max = df['Temp'].max() * 1.10
plt.ylim(y_min, y_max)

plt.show()
