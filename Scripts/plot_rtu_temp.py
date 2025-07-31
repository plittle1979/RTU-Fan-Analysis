import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the database
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
conn = sqlite3.connect(db_path)

# SQL query to get data and calculate running average + deviation
query = """
SELECT
    Date,
    Value AS Temp,
    Notes,
    AVG(Value) OVER (
        ORDER BY Date
        ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
    ) AS RunningAvg,
    Value - AVG(Value) OVER (
        ORDER BY Date
        ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
    ) AS Deviation
FROM "RTU 2-1 Inside Air Fans IAF01 Fan Internal Temp"
WHERE Date >= '6/1/2024' AND Date < '7/1/2024'
"""

# Load the data
df = pd.read_sql_query(query, conn)
conn.close()

# Convert Date column to datetime
df['Date'] = pd.to_datetime(df['Date'].str.replace(" EDT", "", regex=False), errors='coerce')

# Convert Temp to numeric
df['Temp'] = pd.to_numeric(df['Temp'], errors='coerce')

# Plot
plt.figure(figsize=(14, 6))
plt.plot(df['Date'], df['Temp'], label='Temperature', linewidth=1.5)
plt.plot(df['Date'], df['RunningAvg'], label='Running Average (6 pts)', linewidth=1.5)

# Highlight deviations greater than ±5°F
plt.fill_between(df['Date'], df['Temp'], df['RunningAvg'],
                 where=abs(df['Deviation']) > 5,
                 color='red', alpha=0.3, label='Deviation > ±5°F')

plt.xlabel("Date")
plt.ylabel("Temperature (°F)")
plt.title("RTU 2-1 IAF01 Fan Internal Temp – June 2024")
plt.legend()
plt.grid(True)
plt.tight_layout()

# Smart y-axis scaling: 0 to 10% above max temp
y_min = 0
y_max = df['Temp'].max() * 1.10
plt.ylim(y_min, y_max)

plt.show()

