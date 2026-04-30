import pandas as pd
import numpy as np

# Parameters
start_date = "2025-01-01"
num_days = 365

# Generate date range
dates = pd.date_range(start=start_date, periods=num_days)

# Generate data with normal distributions and realistic ranges
np.random.seed(0)  # for reproducible results
steps = np.random.normal(8500, 2500, num_days).clip(3000, 18000)
sleep_hours = np.random.normal(7.2, 1, num_days).clip(4.5, 9.5)
heart_rate = np.random.normal(68, 10, num_days).clip(48, 110)
calories_burned = np.random.randint(1800, 4201, num_days)
active_minutes = np.random.randint(20, 181, num_days)

# Create DataFrame
data = pd.DataFrame({
    'Date': dates,
    'Steps': steps,
    'Sleep_Hours': sleep_hours,
    'Heart_Rate_bpm': heart_rate,
    'Calories_Burned': calories_burned,
    'Active_Minutes': active_minutes
})

# Introduce 5 missing values in each column randomly
for col in data.columns[1:]:  # skip 'Date'
    indices = np.random.choice(data.index, size=5, replace=False)
    data.loc[indices, col] = np.nan

# Save to CSV
data.to_csv('data/health_data.csv', index=False)