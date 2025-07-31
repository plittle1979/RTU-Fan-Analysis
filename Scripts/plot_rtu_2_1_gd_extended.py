import pandas as pd
import matplotlib.pyplot as plt

# === Load CSV ===
csv_path = "C:/sqlite/RTU_Fan_Analysis/rtu_2_1_gd_extended_june_july.csv"
df = pd.read_csv(csv_path, parse_dates=['Date'])

# === Clean/Prepare ===
df.sort_values('Date', inplace=True)

# Filter just the needed columns
temps = df[['Date', 'SA_Temp', 'RAT', 'OAT', 'UPS_Power_Loss']]

# === Plot ===
plt.figure(figsize=(18, 6))

# Plot temperature lines
plt.plot(temps['Date'], temps['SA_Temp'], label='SA Temp', linewidth=1)
plt.plot(temps['Date'], temps['RAT'], label='RAT', linewidth=1)
plt.plot(temps['Date'], temps['OAT'], label='OAT', linewidth=1)

# Overlay power loss as red dots (filter to when UPS_Power_Loss == 1)
if 'UPS_Power_Loss' in temps.columns:
    loss_events = temps[temps['UPS_Power_Loss'] == 1]
    plt.scatter(loss_events['Date'], [temps[['SA_Temp', 'RAT', 'OAT']].max().max() * 1.05] * len(loss_events),
                color='red', label='UPS Power Loss', marker='o', zorder=5)

# === Formatting ===
plt.title("RTU 2-1 Temperature Trends with UPS Power Loss Events (June–July)")
plt.xlabel("Date")
plt.ylabel("Temperature (°F)")
plt.legend()
plt.grid(True)
plt.tight_layout()

# === Show Plot ===
plt.show()

