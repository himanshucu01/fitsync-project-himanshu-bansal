import pandas as pd

# Load the CSV file into a DataFrame
file_path = 'data/health_data.csv'
data = pd.read_csv(file_path)

# Print the first 5 rows
print("First 5 rows of the dataset:")
print(data.head())

# Count missing values in each column
missing_values_count = data.isnull().sum()

# Print the number of missing values for each column
print("\nNumber of missing values in each column:")
print(missing_values_count)