import pandas as pd

input_file = "C:/sqlite/RTU_Fan_Analysis/Raw Data/RTU 2-1 General Data Trends.xlsx"

# Load workbook and list sheet names
xls = pd.ExcelFile(input_file)
print("📄 Found Sheets:", xls.sheet_names)

# Show column names for each sheet
for sheet in ["OAT", "RAT", "SA Temp"]:
    try:
        df = xls.parse(sheet, nrows=1)
        print(f"\n🧾 Sheet: {sheet}")
        print("🔍 Columns:", df.columns.tolist())
    except Exception as e:
        print(f"⚠️ Could not read sheet '{sheet}': {e}")
