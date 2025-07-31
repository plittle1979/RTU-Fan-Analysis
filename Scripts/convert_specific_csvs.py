import pandas as pd
import os

# === CONFIG ===
source_dir = "C:/sqlite/RTU_Fan_Analysis"
filenames = [
    "CR03-RTU04.csv",
    "CR03-RTU04_005.csv",
    "CR03-RTU04_006.csv",
    "CR03-RTU04_008.csv",
    "CR06-RTU01.csv",
    "CR06-RTU01_004.csv",
    "CR06-RTU01_005.csv",
    "CR06-RTU01_007pressure comparison.csv",
    "CR02-RTU01_002.csv",
    "CR02-RTU01_007.csv"
]

# === PROCESS SPECIFIED FILES ONLY ===
for fname in filenames:
    csv_path = os.path.join(source_dir, fname)
    xlsx_path = os.path.splitext(csv_path)[0] + ".xlsx"

    try:
        df = pd.read_csv(csv_path, skiprows=[1])
        df.to_excel(xlsx_path, index=False)
        print(f"✅ Converted: {fname} → {os.path.basename(xlsx_path)}")
    except Exception as e:
        print(f"⚠️ Failed: {fname} — {e}")
