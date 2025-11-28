# weather_lab.py
# Weather Data Visualizer - Basic Version (No config changes needed)

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# This script expects a file named 'weather.csv' in the same folder
# with columns: date, temp, rain, humidity

# ---------- Task 1: Load Data ----------
print("=== Task 1: Data Loading ===")
df = pd.read_csv("weather.csv")

print("\nHead:")
print(df.head())

print("\nInfo:")
print(df.info())

print("\nDescribe:")
print(df.describe(include="all"))

# ---------- Task 2: Cleaning & Processing ----------
print("\n=== Task 2: Cleaning & Processing ===")

# Convert date column
df["date"] = pd.to_datetime(df["date"], errors="coerce")

# Keep only required columns
df = df[["date", "temp", "rain", "humidity"]]

# Drop rows with missing values
df = df.dropna()

# Sort by date
df = df.sort_values(by="date")

print("\nAfter cleaning:")
print(df.head())

# ---------- Prepare for resampling ----------
df = df.set_index("date")

# ---------- Task 3: Statistical Analysis ----------
print("\n=== Task 3: Statistical Analysis ===")

# Daily stats (mean temp per day)
daily_mean_temp = df["temp"].resample("D").mean()
print("\nDaily mean temperature (first 5):")
print(daily_mean_temp.head())

# Monthly stats
monthly_stats = df.resample("M").agg({
    "temp": ["mean", "min", "max", "std"],
    "rain": ["sum", "mean"],
    "humidity": ["mean"]
})
print("\nMonthly stats (first 5):")
print(monthly_stats.head())

# Yearly stats
yearly_stats = df.resample("Y").agg({
    "temp": ["mean", "min", "max", "std"],
    "rain": ["sum", "mean"],
    "humidity": ["mean"]
})
print("\nYearly stats:")
print(yearly_stats)

# ---------- Task 4: Visualization ----------
print("\n=== Task 4: Visualization (PNG files will be saved) ===")

# 1. Line chart – daily temperature
plt.figure()
plt.plot(df.index, df["temp"])
plt.title("Daily Temperature")
plt.xlabel("Date")
plt.ylabel("Temperature")
plt.tight_layout()
plt.savefig("daily_temperature.png")

# 2. Bar chart – monthly rainfall totals
monthly_rain_sum = monthly_stats["rain"]["sum"]
plt.figure()
plt.bar(monthly_rain_sum.index.strftime("%Y-%m"), monthly_rain_sum)
plt.title("Monthly Rainfall Total")
plt.xlabel("Month")
plt.ylabel("Rainfall")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("monthly_rainfall.png")

# 3. Scatter – humidity vs temperature
plt.figure()
plt.scatter(df["temp"], df["humidity"])
plt.title("Humidity vs Temperature")
plt.xlabel("Temperature")
plt.ylabel("Humidity")
plt.tight_layout()
plt.savefig("humidity_vs_temperature.png")

# 4. Combined figure – temp line + monthly rain bar
fig, axes = plt.subplots(2, 1)
axes[0].plot(df.index, df["temp"])
axes[0].set_title("Daily Temperature")
axes[0].set_ylabel("Temp")

axes[1].bar(monthly_rain_sum.index.strftime("%Y-%m"), monthly_rain_sum)
axes[1].set_title("Monthly Rainfall Total")
axes[1].set_xlabel("Month")
axes[1].set_ylabel("Rainfall")
for label in axes[1].get_xticklabels():
    label.set_rotation(45)

plt.tight_layout()
plt.savefig("combined_temp_rain.png")

# ---------- Task 5: Grouping & Aggregation ----------
print("\n=== Task 5: Grouping & Aggregation ===")

# Add month column
df["month"] = df.index.month

# Group by month
month_group = df.groupby("month").agg({
    "temp": "mean",
    "rain": "sum",
    "humidity": "mean"
})
print("\nGrouped by month:")
print(month_group)

# Simple season function
def get_season(m):
    if m in [12, 1, 2]:
        return "Winter"
    elif m in [3, 4, 5]:
        return "Spring"
    elif m in [6, 7, 8]:
        return "Summer"
    else:
        return "Autumn"

df["season"] = df["month"].apply(get_season)

season_group = df.groupby("season").agg({
    "temp": "mean",
    "rain": "sum",
    "humidity": "mean"
})
print("\nGrouped by season:")
print(season_group)

# ---------- Task 6: Export & Storytelling ----------
print("\n=== Task 6: Export & Report ===")

# Export cleaned data
df.to_csv("weather_cleaned.csv")
print("Cleaned data saved to weather_cleaned.csv")

# Write simple text report
with open("weather_report.txt", "w") as f:
    f.write("Weather Data Report\n")
    f.write("===================\n\n")
    f.write("Total records after cleaning: " + str(len(df)) + "\n\n")

    f.write("Monthly stats (first few rows):\n")
    f.write(str(monthly_stats.head()) + "\n\n")

    f.write("Yearly stats:\n")
    f.write(str(yearly_stats) + "\n\n")

    f.write("Grouped by month:\n")
    f.write(str(month_group) + "\n\n")

    f.write("Grouped by season:\n")
    f.write(str(season_group) + "\n\n")

    f.write("Interpretation (fill in by yourself):\n")
    f.write("- Comment on temperature trends.\n")
    f.write("- Comment on rainfall trends.\n")
    f.write("- Mention any extreme values / anomalies.\n")

print("Report saved to weather_report.txt")
print("All plots saved as PNG files: daily_temperature.png, monthly_rainfall.png, humidity_vs_temperature.png, combined_temp_rain.png")
print("\nDone ✅")
