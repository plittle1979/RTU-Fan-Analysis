import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the database
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
conn = sqlite3.connect(db_path)

# Get just temperature data for all of June 2024
query = """
SELECT
    Date,
    Value AS Temp
FROM "RTU 2-1 General Data Trends SA Temp"
WHERE Date >= '6/1/2024' AND Date < '7/1/2024'
"""

df = pd.read_sql_query(query, conn)
conn.close()

# Parse and clean
df['Date'] = pd.to_datetime(df['Date'].str.replace(" EDT", "", regex=False), errors='coerce')
df['Temp'] = pd.to_numeric(df['Temp'], errors='coerce')

# Drop any bad rows
before = len(df)
df = df.dropna(subset=['Date', 'Temp'])
after = len(df)
print(f"Dropped {before - after} bad rows. Remaining: {after}")

# Sort chronologically
df = df.sort_values(by='Date')

# Plot
plt.figure(figsize=(14, 6))
plt.plot(df['Date'], df['Temp'], label='Temperature', linewidth=1.5)
plt.xlabel("Date")
plt.ylabel("Temperature (°F)")
plt.title("RTU 2-1 SA Temp – June 2024")
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()

# Y-axis scale
y_min = 0
y_max = df['Temp'].max() * 1.10
plt.ylim(y_min, y_max)

plt.show()
