import sqlite3
import os
import csv

# Configuration
DATABASE_NAME = "rtu-fan_analysis.db"
CSV_FOLDER = "C:/sqlite/RTU_Fan_Analysis"

# Connect to SQLite
conn = sqlite3.connect(DATABASE_NAME)
cursor = conn.cursor()

# Get all CSV files
csv_files = [f for f in os.listdir(CSV_FOLDER) if f.endswith(".csv")]

# Define columns
columns = ["Date", "Excel Time", "Value", "Notes"]

for filename in csv_files:
    file_path = os.path.join(CSV_FOLDER, filename)
    table_name = os.path.splitext(filename)[0]

    print(f"Processing: {filename}")

    # Drop table if it already exists
    cursor.execute(f'DROP TABLE IF EXISTS "{table_name}"')

    # Create table
    col_defs = ', '.join([f'"{col}" TEXT' for col in columns])
    cursor.execute(f'CREATE TABLE "{table_name}" ({col_defs})')

    # Read and import CSV
    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # Skip header
        for row in reader:
            row = row + [None] * (4 - len(row))  # Pad missing columns
            cursor.execute(
                f'INSERT INTO "{table_name}" (Date, "Excel Time", Value, Notes) VALUES (?, ?, ?, ?)',
                row[:4]
            )

conn.commit()
conn.close()
print("✅ All data imported successfully.")
