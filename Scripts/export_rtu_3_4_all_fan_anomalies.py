import sqlite3
import pandas as pd

# === CONFIG ===
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
fan_types = [("Inside Air Fans", "IAF"), ("Outside Air Fans", "OAF")]
fan_ids = [f"{i:02}" for i in range(1, 9)]
output_excel = "C:/sqlite/RTU_Fan_Analysis/rtu_3_4_all_fan_anomalies.xlsx"
date_range = ("6/1/2024", "8/1/2024")

# === CONNECT ===
conn = sqlite3.connect(db_path)
writer = pd.ExcelWriter(output_excel, engine='openpyxl')

# === LOOP OVER FANS ===
for fan_type, fan_prefix in fan_types:
    for fan_id in fan_ids:
        table_name = f"RTU 3-4 {fan_type} {fan_prefix}{fan_id} Fan Internal Temp"
        try:
            query = f"""
            SELECT Date, Value AS Temp
            FROM (
                SELECT
                    Date,
                    Value,
                    ROUND(AVG(Value) OVER (
                        ORDER BY Date
                        ROWS BETWEEN 5 PRECEDING AND CURRENT ROW
                    ), 2) AS RunningAvg
                FROM "{table_name}"
                WHERE Date >= ? AND Date < ?
            )
            WHERE ABS(Value - RunningAvg) > 5
            """
            df = pd.read_sql_query(query, conn, params=date_range)
            df['Date'] = pd.to_datetime(df['Date'].str.replace(" EDT", "", regex=False), errors='coerce')
            df['Temp'] = pd.to_numeric(df['Temp'], errors='coerce')
            df.dropna(subset=['Date', 'Temp'], inplace=True)

            if not df.empty:
                sheet_name = f"{fan_prefix}{fan_id}"
                df.to_excel(writer, sheet_name=sheet_name, index=False)
                print(f"✅ Anomalies found: {table_name}")
            else:
                print(f"⛔ No anomalies: {table_name}")
        except Exception as e:
            print(f"⚠️ Failed: {table_name} — {e}")

# === SAVE & CLOSE ===
writer.close()
conn.close()
print(f"\n✅ All anomaly sheets saved to: {output_excel}")
