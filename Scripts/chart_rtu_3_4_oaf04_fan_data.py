import sqlite3
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# === Setup ===
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
output_path = "C:/sqlite/RTU_Fan_Analysis/Charts/RTU_3_4_OAF04_Fan_Data_June_July.png"

rtu = "RTU 3-4"
fan = "Outside Air Fans"
fan_id = "OAF04"
suffixes = [
    ("Discrete Alarm 1", "Alarm 1", True),
    ("Discrete Alarm 2", "Alarm 2", True),
    ("Fan IGBT Temp", "IGBT Temp", False),
    ("Fan Internal Temp", "Internal Temp", False)
]

start_date = '6/1/2024'
end_date = '8/1/2024'

# === Connect and fetch data ===
conn = sqlite3.connect(db_path)
all_data = pd.DataFrame()

for suffix, label, is_alarm in suffixes:
    table_name = f"{rtu} {fan} {fan_id} {suffix}"
    try:
        query = f"""
        SELECT Date, Value
        FROM "{table_name}"
        WHERE Date >= '{start_date}' AND Date < '{end_date}'
        """
        df = pd.read_sql_query(query, conn)
        df['Date'] = pd.to_datetime(df['Date'].str.replace(" EDT", "", regex=False), errors='coerce')
        df['Value'] = pd.to_numeric(df['Value'], errors='coerce')
        df = df.dropna()

        if is_alarm:
            # Display 25 when the alarm is on, NaN when it's off
            df['Value'] = df['Value'].apply(lambda x: 25 if x != 0 else np.nan)

        df = df.rename(columns={'Value': label})

        if all_data.empty:
            all_data = df
        else:
            all_data = pd.merge(all_data, df, on='Date', how='outer')

        print(f"✅ Pulled: {table_name}")
    except Exception as e:
        print(f"⚠️ Failed: {table_name} — {e}")

conn.close()

# === Plotting ===
plt.figure(figsize=(15, 8))
for label in all_data.columns[1:]:
    plt.plot(all_data['Date'], all_data[label], label=label)

plt.title(f"{rtu} {fan_id} Fan Data (June–July 2024)")
plt.xlabel("Date")
plt.ylabel("Value")
plt.legend()
plt.grid(True)
plt.tight_layout()

# === Save figure ===
plt.savefig(output_path)
plt.close()

print(f"\n✅ Chart saved to: {output_path}")
