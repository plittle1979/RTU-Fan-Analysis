import pandas as pd

# === File path ===
file_path = r"C:\sqlite\RTU_Fan_Analysis\Processed Data\CR02-RTU01_002.xlsx"

# === Load file ===
df = pd.read_excel(file_path)

# === Identify MX columns ===
mx_columns = [col for col in df.columns if "MX" in str(col)]

# === Container for anomalies ===
deviations = {}

for col in mx_columns:
    series = pd.to_numeric(df[col], errors='coerce')
    rolling_avg = series.rolling(window=5).mean()
    diff = (series - rolling_avg).abs()
    outliers = df[diff > 1]
    
    if not outliers.empty:
        deviations[col] = outliers[[col]]

# === Output results ===
if deviations:
    with pd.ExcelWriter(r"C:\sqlite\RTU_Fan_Analysis\Processed Data\CR02-RTU01_002_MX_Anomalies.xlsx") as writer:
        for col, outlier_df in deviations.items():
            outlier_df.to_excel(writer, sheet_name=col[:31], index=False)
    print("✅ Deviations saved to: CR02-RTU01_002_MX_Anomalies.xlsx")
else:
    print("✅ No deviations > 1 found in any MX column.")
