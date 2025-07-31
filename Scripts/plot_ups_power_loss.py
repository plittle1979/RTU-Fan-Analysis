import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# === Setup ===
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
tables = {
    "RTU 2-1": "RTU 2-1 General Data Trends UPS Power Loss",
    "RTU 3-4": "RTU 3-4 General Data Trends UPS Power Loss",
    "RTU 6-1": "RTU 6-1 General Data Trends UPS Power Loss",
}
date_range = ("6/1/2024", "8/1/2024")

# === Connect ===
conn = sqlite3.connect(db_path)

# === Pull and Filter Data ===
plot_data = []
for label, table in tables.items():
    query = f"""
        SELECT Date, Value
        FROM "{table}"
        WHERE Date >= ? AND Date < ? AND Value = 1
    """
    df = pd.read_sql_query(query, conn, params=date_range)
    df['Date'] = pd.to_datetime(df['Date'].str.replace(" EDT", "", regex=False), errors='coerce')
    df.dropna(subset=['Date'], inplace=True)
    df['Label'] = label
    plot_data.append(df)

conn.close()

# === Combine and Plot ===
full_data = pd.concat(plot_data)
plt.figure(figsize=(12, 6))

for label, group in full_data.groupby('Label'):
    plt.scatter(group['Date'], [1.0]*len(group), label=label, s=40)

plt.ylim(0, 1.5)
plt.yticks([0, 1])
plt.title("UPS Power Loss Events (Only '1' Values Shown)")
plt.xlabel("Date")
plt.ylabel("UPS Power Loss (1 = Event)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.xticks(rotation=45)

plt.show()
