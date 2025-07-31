import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import os

# Setup paths
base_dir = "C:/sqlite/RTU_Fan_Analysis"
db_path = os.path.join(base_dir, "rtu-fan_analysis.db")
sql_path = os.path.join(base_dir, "scripts/query_template.sql")

# Read SQL from file
with open(sql_path, "r") as file:
    query = file.read()

# Run the query
conn = sqlite3.connect(db_path)
df = pd.read_sql_query(query, conn)
conn.close()

# Convert and clean
df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna()

# Plot it
plt.figure(figsize=(12, 5))
plt.plot(df["Date"], df["AvgTemp"], label="Avg Temp")
plt.xlabel("Date")
plt.ylabel("Temperature (°F)")
plt.title("Average Fan Temperature – June 2024")
plt.grid(True)
plt.tight_layout()
plt.legend()
plt.show()

print(f"✅ Plotted {len(df)} rows.")
