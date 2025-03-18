import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Load the uploaded CSV file
file_path = 'all_data.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the data to understand its structure
data.head(), data.info()
# Combine year, month, and day into a single datetime column
data['date'] = pd.to_datetime(data[['year', 'month', 'day']])

# Function to create a daily summary DataFrame
def create_daily_summary_df(df):
    daily_summary_df = df.resample('D', on='date').agg({
        'PM2.5': 'mean',
        'PM10': 'mean',
        'SO2': 'mean',
        'NO2': 'mean',
        'CO': 'mean',
        'O3': 'mean',
        'TEMP': 'mean',
        'PRES': 'mean',
        'WSPM': 'mean',
        'RAIN': 'sum'
    })
    daily_summary_df = daily_summary_df.reset_index()
    daily_summary_df.rename(columns={
        'PM2.5': 'PM2_5_avg',
        'PM10': 'PM10_avg',
        'SO2': 'SO2_avg',
        'NO2': 'NO2_avg',
        'CO': 'CO_avg',
        'O3': 'O3_avg',
        'TEMP': 'Temp_avg',
        'PRES': 'Pressure_avg',
        'WSPM': 'WindSpeed_avg',
        'RAIN': 'Total_Rainfall'
    }, inplace=True)
    return daily_summary_df

# Generate the daily summary DataFrame
daily_summary = create_daily_summary_df(data)

# Display the first few rows of the daily summary
daily_summary.head()
import matplotlib.pyplot as plt
import seaborn as sns

# Set up the style for the plots
sns.set_theme(style="whitegrid")

# Create a dashboard layout
fig, axes = plt.subplots(3, 2, figsize=(15, 12), constrained_layout=True)

# Plot PM2.5 average over time
sns.lineplot(data=daily_summary, x="date", y="PM2_5_avg", ax=axes[0, 0], color="red")
axes[0, 0].set_title("Daily PM2.5 Average")
axes[0, 0].set_ylabel("PM2.5 (µg/m³)")

# Plot PM10 average over time
sns.lineplot(data=daily_summary, x="date", y="PM10_avg", ax=axes[0, 1], color="orange")
axes[0, 1].set_title("Daily PM10 Average")
axes[0, 1].set_ylabel("PM10 (µg/m³)")

# Plot SO2 average over time
sns.lineplot(data=daily_summary, x="date", y="SO2_avg", ax=axes[1, 0], color="blue")
axes[1, 0].set_title("Daily SO2 Average")
axes[1, 0].set_ylabel("SO2 (µg/m³)")

# Plot NO2 average over time
sns.lineplot(data=daily_summary, x="date", y="NO2_avg", ax=axes[1, 1], color="green")
axes[1, 1].set_title("Daily NO2 Average")
axes[1, 1].set_ylabel("NO2 (µg/m³)")

# Plot temperature over time
sns.lineplot(data=daily_summary, x="date", y="Temp_avg", ax=axes[2, 0], color="purple")
axes[2, 0].set_title("Daily Temperature Average")
axes[2, 0].set_ylabel("Temperature (°C)")

# Plot rainfall over time
sns.barplot(data=daily_summary, x="date", y="Total_Rainfall", ax=axes[2, 1], color="cyan")
axes[2, 1].set_title("Daily Total Rainfall")
axes[2, 1].set_ylabel("Rainfall (mm)")

# Rotate x-axis labels for better readability
for ax in axes.flatten():
    ax.set_xlabel("Date")
    for label in ax.get_xticklabels():
        label.set_rotation(45)

# Display the dashboard
plt.show()
def create_sum_pm25_by_station_df(df):
    sum_pm25_station_df = (
        df.groupby("station")["PM2.5"]
        .mean()
        .sort_values(ascending=False)
        .reset_index()
    )
    sum_pm25_station_df.rename(columns={"PM2.5": "PM2_5_avg"}, inplace=True)
    return sum_pm25_station_df
# Function to calculate the number of data points by station
def create_bystation_df(df):
    bystation_df = df.groupby("station").size().reset_index(name="data_count")
    return bystation_df

# Apply the function to the dataset
bystation_summary = create_bystation_df(data)

# Display the resulting DataFrame
bystation_summary.head()
# Function to group data by temperature categories and count observations
def create_by_temp_group_df(df):
    # Define temperature categories
    bins = [-float('inf'), 10, 25, float('inf')]
    labels = ["Cold", "Moderate", "Hot"]
    df["temp_group"] = pd.cut(df["TEMP"], bins=bins, labels=labels)
    
    # Group by temperature categories
    by_temp_group_df = df.groupby("temp_group").size().reset_index(name="data_count")
    return by_temp_group_df

# Apply the function to the dataset
by_temp_group_summary = create_by_temp_group_df(data)

# Display the resulting DataFrame
by_temp_group_summary
# Function to calculate average PM2.5 by station (as a substitute for "state")
def create_bystate_df(df):
    bystate_df = (
        df.groupby("station")["PM2.5"]
        .mean()
        .reset_index()
        .rename(columns={"PM2.5": "PM2_5_avg"})
    )
    return bystate_df

# Apply the function to the dataset
bystate_summary = create_bystate_df(data)

# Display the resulting DataFrame
bystate_summary.head()
    # Corrected function to create RFM metrics for stations
def create_rfm_station_df_corrected(df):
    rfm_df = df.groupby("station").agg({
        "date": "max",           # Most recent date recorded for the station
        "PM2.5": "mean"          # Average PM2.5 value
    }).reset_index()
    rfm_df.rename(columns={"date": "max_date", "PM2.5": "pm25_avg"}, inplace=True)
    
    # Add frequency (count of observations)
    frequency = df.groupby("station").size().reset_index(name="frequency")
    rfm_df = rfm_df.merge(frequency, on="station")
    
    # Calculate recency (days since last recorded date)
    recent_date = df["date"].max()
    rfm_df["recency"] = (recent_date - rfm_df["max_date"]).dt.days
    rfm_df.drop("max_date", axis=1, inplace=True)
    
    return rfm_df

# Apply the corrected function to the dataset
rfm_station_summary_corrected = create_rfm_station_df_corrected(data)

# Display the resulting DataFrame
rfm_station_summary_corrected.head()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Load Data
data = pd.read_csv("all_data.csv")
data['date'] = pd.to_datetime(data[['year', 'month', 'day']])

# Generate Daily Summary
def create_daily_summary_df(df):
    daily_summary_df = df.resample('D', on='date').agg({
        'PM2.5': 'mean', 'PM10': 'mean', 'SO2': 'mean',
        'NO2': 'mean', 'CO': 'mean', 'O3': 'mean',
        'TEMP': 'mean', 'PRES': 'mean', 'WSPM': 'mean', 'RAIN': 'sum'
    }).reset_index()
    daily_summary_df.rename(columns={'PM2.5': 'PM2_5_avg', 'PM10': 'PM10_avg', 'SO2': 'SO2_avg',
                                     'NO2': 'NO2_avg', 'CO': 'CO_avg', 'O3': 'O3_avg',
                                     'TEMP': 'Temp_avg', 'PRES': 'Pressure_avg',
                                     'WSPM': 'WindSpeed_avg', 'RAIN': 'Total_Rainfall'}, inplace=True)
    return daily_summary_df

daily_summary = create_daily_summary_df(data)

# Streamlit Dashboard
st.title("📊 Dashboard Analisis Kualitas Udara")

# Line Plots
st.subheader("Tren Polusi Harian")
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=daily_summary, x="date", y="PM2_5_avg", label="PM2.5", ax=ax, color="red")
sns.lineplot(data=daily_summary, x="date", y="PM10_avg", label="PM10", ax=ax, color="orange")
ax.set_title("Tren PM2.5 & PM10")
ax.set_ylabel("Konsentrasi (µg/m³)")
st.pyplot(fig)

# Bar Chart untuk Rata-rata PM2.5 per Stasiun
st.subheader("Rata-rata PM2.5 per Stasiun")
sum_pm25_station_df = data.groupby("station")["PM2.5"].mean().sort_values(ascending=False).reset_index()
fig, ax = plt.subplots(figsize=(12, 6))
sns.barplot(data=sum_pm25_station_df, x="station", y="PM2.5", ax=ax, palette="coolwarm")
ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
ax.set_ylabel("Rata-rata PM2.5")
ax.set_title("PM2.5 per Stasiun")
st.pyplot(fig)

# Heatmap Korelasi
st.subheader("Korelasi antara Variabel")
fig, ax = plt.subplots(figsize=(10, 6))
sns.heatmap(daily_summary.corr(), annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5, ax=ax)
st.pyplot(fig)

# Scatter Plot
st.subheader("Hubungan antara Temperatur dan PM2.5")
fig, ax = plt.subplots(figsize=(8, 5))
sns.scatterplot(data=data, x="TEMP", y="PM2.5", alpha=0.5, color="blue")
ax.set_title("Scatter Plot: Temperatur vs PM2.5")
ax.set_xlabel("Temperatur (°C)")
ax.set_ylabel("PM2.5 (µg/m³)")
st.pyplot(fig)

st.write("Sumber Data: Dataset Kualitas Udara")



