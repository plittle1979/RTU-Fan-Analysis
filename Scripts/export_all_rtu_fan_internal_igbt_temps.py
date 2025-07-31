import sqlite3
import pandas as pd

# === Setup ===
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
output_base = "C:/sqlite/RTU_Fan_Analysis"

rtus = ["RTU 2-1", "RTU 3-4", "RTU 6-1"]
fan_types = [("Inside Air Fans", "IAF"), ("Outside Air Fans", "OAF")]
fan_ids = [f"{i:02}" for i in range(1, 9)]
suffixes = [("Fan Internal Temp", "Internal"), ("Fan IGBT Temp", "IGBT")]

# === Connect ===
conn = sqlite3.connect(db_path)

for rtu in rtus:
    all_data = pd.DataFrame()
    for fan_type, fan_prefix in fan_types:
        for fan_id in fan_ids:
            for suffix, label in suffixes:
                table_name = f'{rtu} {fan_type} {fan_prefix}{fan_id} {suffix}'
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
                    col_name = f'{fan_prefix}{fan_id} {label}'
                    df = df.rename(columns={'Temp': col_name})
                    df = df[['Date', col_name]]
                    if all_data.empty:
                        all_data = df
                    else:
                        all_data = pd.merge(all_data, df, on='Date', how='outer')
                    print(f"✅ Pulled: {table_name}")
                except Exception as e:
                    print(f"⚠️ Failed: {table_name} — {e}")

    all_data = all_data.sort_values(by='Date')
    base_name = rtu.replace(" ", "_").lower()
    csv_output = f"{output_base}/{base_name}_fan_internal_igbt_temps_june_july.csv"
    excel_output = f"{output_base}/{base_name}_fan_internal_igbt_temps_june_july.xlsx"
    all_data.to_csv(csv_output, index=False)
    all_data.to_excel(excel_output, index=False)

    print(f"\n✅ {rtu} Saved to:\n  CSV:   {csv_output}\n  Excel: {excel_output}")

conn.close()
