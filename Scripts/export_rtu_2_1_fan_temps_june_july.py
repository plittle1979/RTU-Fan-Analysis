import sqlite3
import pandas as pd

# === Setup ===
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
csv_output = "C:/sqlite/RTU_Fan_Analysis/rtu_2_1_fan_temps_june_july.csv"
excel_output = "C:/sqlite/RTU_Fan_Analysis/rtu_2_1_fan_temps_june_july.xlsx"

fan_types = [("Inside Air Fans", "IAF"), ("Outside Air Fans", "OAF")]
fan_ids = [f"{i:02}" for i in range(1, 9)]  # IAF01–08 and OAF01–08

# === Connect ===
conn = sqlite3.connect(db_path)
all_data = pd.DataFrame()

# === Fan Data ===
for fan_type, fan_prefix in fan_types:
    for fan_id in fan_ids:
        table_name = f'RTU 2-1 {fan_type} {fan_prefix}{fan_id} Fan Internal Temp'
        try:
            query = f"""
            SELECT Date, Value AS Temp
            FROM "{table_name}"
            WHERE Date >= '6/1/2024' AND Date < '8/1/2024'
            """
            df = pd.read_sql_query(query, conn)
            df['Date'] = pd.to_datetime(df['Date'].str.replace(" EDT", "", regex=False), errors='coerce')
            df['Temp'] = pd.to_numeric(df['Temp'], errors='coerce')
            df = df.dropna(subset=['Date'])
            df = df.rename(columns={'Temp': f'{fan_prefix}{fan_id}'})
            if all_data.empty:
                all_data = df
            else:
                all_data = pd.merge(all_data, df, on='Date', how='outer')
            print(f"✅ Pulled: {table_name}")
        except Exception as e:
            print(f"⚠️ Failed: {table_name} — {e}")

conn.close()

# === Sort and Export ===
all_data = all_data.sort_values(by='Date')
all_data.to_csv(csv_output, index=False)
all_data.to_excel(excel_output, index=False)

print(f"\n✅ Saved to:\n  CSV:   {csv_output}\n  Excel: {excel_output}")
