
import pandas as pd

# === File Paths ===
input_file = "C:/sqlite/RTU_Fan_Analysis/Processed Data/CR02-RTU01_002.xlsx"
output_file = "C:/sqlite/RTU_Fan_Analysis/Processed Data/CR02-RTU01_002_minute_avg.xlsx"

# === Load Excel File ===
df = pd.read_excel(input_file)

# === Parse Timestamps ===
# Assumes first column contains timestamp data like "7/17/2025 7:41:56 AM"
df.columns = df.columns.str.strip()  # Remove accidental spaces in headers
df[df.columns[0]] = pd.to_datetime(df[df.columns[0]], errors='coerce')

# Drop rows with invalid timestamps
df = df.dropna(subset=[df.columns[0]])

# Set datetime column as index
df = df.set_index(df.columns[0])

# === Resample to 1-minute averages ===
minute_df = df.resample('1T').mean(numeric_only=True)

# Drop rows where all values are NaN (likely from minute gaps)
minute_df = minute_df.dropna(how='all')

# === Save to Excel ===
minute_df.to_excel(output_file)

print(f"\n✅ Averaged 1-minute file saved to:\n{output_file}")



