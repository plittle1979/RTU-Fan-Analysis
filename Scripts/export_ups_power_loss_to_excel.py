import sqlite3
import pandas as pd

# === CONFIG ===
db_path = "C:/sqlite/RTU_Fan_Analysis/rtu-fan_analysis.db"
output_excel = "C:/sqlite/RTU_Fan_Analysis/ups_power_loss_summary.xlsx"
date_range = ("6/1/2024", "8/1/2024")

tables = {
    "RTU 2-1": "RTU 2-1 General Data Trends UPS Power Loss",
    "RTU 3-4": "RTU 3-4 General Data Trends UPS Power Loss",
    "RTU 6-1": "RTU 6-1 General Data Trends UPS Power Loss",
}

# === CONNECT AND PROCESS ===
conn = sqlite3.connect(db_path)
writer = pd.ExcelWriter(output_excel, engine="openpyxl")

for rtu_name, table_name in tables.items():
    try:
        query = f"""
        SELECT Date, Value
        FROM "{table_name}"
        WHERE Date >= ? AND Date < ? AND Value = 1
        """
        df = pd.read_sql_query(query, conn, params=date_range)
        df['Date'] = pd.to_datetime(df['Date'].str.replace(" EDT", "", regex=False), errors='coerce')
        df = df.dropna(subset=["Date"])
        df = df.sort_values("Date")

        if not df.empty:
            df.to_excel(writer, sheet_name=rtu_name.replace(" ", "_"), index=False)
            print(f"✅ Wrote {rtu_name}")
        else:
            print(f"⛔ No events for {rtu_name}")
    except Exception as e:
        print(f"⚠️ Failed: {rtu_name} — {e}")

# === FINALIZE ===
writer.close()
conn.close()
print(f"\n✅ UPS Power Loss report saved to:\n  {output_excel}")
