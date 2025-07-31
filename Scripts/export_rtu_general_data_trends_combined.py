import os
import pandas as pd

# === Setup ===
import os
import pandas as pd

# === Setup ===
base_path = "C:/sqlite/RTU_Fan_Analysis/Processed Data"
rtu_files = [
    "RTU 2-1 General Data Trends.xlsx",
    "RTU 3-4 General Data Trends.xlsx",
    "RTU 6-1 General Data Trends.xlsx"
]
output_path = "C:/sqlite/RTU_Fan_Analysis"

# === Process each file ===
for file in rtu_files:
    file_path = os.path.join(base_path, file)
    xl = pd.ExcelFile(file_path)
    combined = pd.DataFrame()
    
    for sheet in xl.sheet_names:
        try:
            df = xl.parse(sheet)
            date_col = pd.to_datetime(df['Date'].astype(str).str.replace("EDT", "", regex=False), errors='coerce')
            value_col = pd.to_numeric(df['Value'], errors='coerce')
            out_df = pd.DataFrame({
                f"{sheet} Date": date_col,
                f"{sheet} Value": value_col
            })
            combined = pd.concat([combined, out_df], axis=1)
            print(f"✅ Pulled: {file} — {sheet}")
        except Exception as e:
            print(f"⚠️ Skipped: {file} — {sheet} due to error: {e}")

    # === Save output ===
    base_name = file.replace(" General Data Trends.xlsx", "").replace(" ", "_").lower()
    csv_path = os.path.join(output_path, f"{base_name}_gdt_combined_unaligned.csv")
    xlsx_path = os.path.join(output_path, f"{base_name}_gdt_combined_unaligned.xlsx")

    combined.to_csv(csv_path, index=False)
    combined.to_excel(xlsx_path, index=False)

    print(f"\n✅ Saved:\n  CSV:   {csv_path}\n  Excel: {xlsx_path}\n")
