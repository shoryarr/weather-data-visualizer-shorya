import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("weather.csv")
print(df.head())
print(df.info())
print(df.describe())

df.columns = df.columns.str.lower()

df['date'] = pd.to_datetime(df['date'], errors='coerce')
df = df.dropna(subset=['date'])

df['temperature'] = df['temperature'].fillna(df['temperature'].mean())
df['humidity'] = df['humidity'].fillna(method='ffill')
df['rainfall'] = df['rainfall'].fillna(0)

df = df[['date', 'temperature', 'humidity, 'rainfall']]

daily_mean = np.mean(df['temperature'])
daily_min = np.min(df['temperature'])
daily_max = np.max(df['temperature'])
daily_std = np.std(df['temperature'])

df['month'] = df['date'].dt.month
df['year'] = df['date'].dt.year

monthly_avg_temp = df.groupby('month')['temperature'].mean()
yearly_rainfall = df.groupby('year')['rainfall'].sum()

print(daily_mean)
print(daily_std)
print(monthly_avg_temp)

plt.figure(figsize=(10,5))
plt.plot(df['date'], df['temperature'])
plt.title("Daily Temperature Trend")
plt.xlabel("Date")
plt.ylabel("Temperature")
plt.tight_layout()
plt.savefig("daily_temperature.png")
plt.close()

plt.figure(figsize=(10,5))
plt.bar(monthly_avg_temp.index, df.groupby('month')['rainfall'].sum())
plt.title("Monthly Rainfall Totals")
plt.xlabel("Month")
plt.ylabel("Rainfall")
plt.tight_layout()
plt.savefig("monthly_rainfall.png")
plt.close()

plt.figure(figsize=(7,5))
plt.scatter(df['temperature'], df['humidity'])
plt.title("Humidity vs Temperature")
plt.xlabel("Temperature")
plt.ylabel("Humidity")
plt.tight_layout()
plt.savefig("humidity_vs_temp.png")
plt.close()

fig, axes = plt.subplots(1, 2, figsize=(12,5))
axes[0].plot(df['date'], df['temperature'])
axes[0].set_title("Daily Temperature")
axes[1].bar(monthly_avg_temp.index, df.groupby('month')['rainfall'].sum())
axes[1].set_title("Monthly Rainfall")
plt.tight_layout()
plt.savefig("combined_plots.png")
plt.close()

season_map = {
    12: "Winter", 1: "Winter", 2: "Winter",
    3: "Spring", 4: "Spring", 5: "Spring",
    6: "Summer", 7: "Summer", 8: "Summer",
    9: "Autumn", 10: "Autumn", 11: "Autumn"
}

df['season'] = df['month'].map(season_map)

season_summary = df.groupby('season').agg({
    'temperature': 'mean',
    'humidity': 'mean',
    'rainfall': 'sum'
})

print(season_summary)

df.to_csv("cleaned_weather.csv", index=False)
season_summary.to_csv("season_summary.csv")
print("Done.")
