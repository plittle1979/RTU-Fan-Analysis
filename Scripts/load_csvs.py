import sqlite3
import pandas as pd
import os

# Set up the path and CSV file list
data_dir = "C:/sqlite/RTU_Fan_Analysis"
csv_files = [
   "CR03-RTU04.csv",
 "CR03-RTU04_005.csv",
 "CR03-RTU04_006.csv",
 "CR03-RTU04_008.csv",
 "CR06-RTU01.csv",
 "CR06-RTU01_004.csv",
 "CR06-RTU01_005.csv",
 "CR06-RTU01_007pressure comparison.csv"
]

# Connect to your SQLite database
conn = sqlite3.connect(os.path.join(data_dir, "rtu-fan_analysis.db"))

# Loop through and load each file
for filename in csv_files:
    table_name = os.path.splitext(filename)[0].replace(" ", "_")
    csv_path = os.path.join(data_dir, filename)
    print("Loading", filename, "into table", table_name)

    try:
        df = pd.read_csv(csv_path)
        df.columns = [col.strip().replace(" ", "_") for col in df.columns]
        df.to_sql(table_name, conn, if_exists="replace", index=False)
        print("Loaded", len(df), "rows into", table_name)
    except Exception as e:
        print("Error loading", filename, ":", str(e))

conn.close()
print("All files processed.")
