import pandas as pd
import streamlit as st

@st.cache_data
def load_data():
    # Read the CSV file into a DataFrame
    file_path = 'data/health_data.csv'
    data = pd.read_csv(file_path)

    # Handle missing values intelligently
    
    # Fill missing 'steps' with the median value of the 'steps' column
    data['Steps'].fillna(data['Steps'].median(), inplace=True)

    # Fill missing 'Sleep_Hours' with 7.0
    data['Sleep_Hours'].fillna(7.0, inplace=True)

    # Fill missing 'heart_rate_bpm' with 68
    data['Heart_Rate_bpm'].fillna(68, inplace=True)

    # Fill other columns with their median values
    for column in data.columns:
        if data[column].isnull().any():
            data[column].fillna(data[column].median(), inplace=True)

    # Convert the 'date' column to datetime objects
    data['Date'] = pd.to_datetime(data['Date'])

    # Return the cleaned DataFrame
    return data

def calculate_recovery_score(df):
    """
    Calculate a 'Recovery_Score' for each row in the DataFrame.

    The Recovery_Score is a simple metric that evaluates how well the person's body has recovered based on sleep, heart rate, and physical activity.
    """

    # Initialize a new column for Recovery_Score with default value as 50
    df['Recovery_Score'] = 50

    # Adjust score based on Sleep_Hours
    # Good sleep (7+ hours) improves recovery score significantly
    df.loc[df['Sleep_Hours'] >= 7, 'Recovery_Score'] += 20

    # Poor sleep (less than 6 hours) reduces recovery score heavily
    df.loc[df['Sleep_Hours'] < 6, 'Recovery_Score'] -= 20

    # Adjust score based on Heart_Rate_bpm
    # Lower resting heart rate (50-65) indicates better recovery
    df.loc[df['Heart_Rate_bpm'] <= 65, 'Recovery_Score'] += 15

    # Higher heart rate suggests less recovery
    df.loc[df['Heart_Rate_bpm'] > 80, 'Recovery_Score'] -= 10

    # Adjust score based on Steps
    # Moderate activity indicates better recovery, extremely high steps might suggest strain
    df.loc[df['Steps'] > 12000, 'Recovery_Score'] += 5

    # Very high steps from the previous day might reduce slightly due to strain
    df.loc[df['Steps'] > 16000, 'Recovery_Score'] -= 5

    # Ensure Recovery_Score stays within the range of 0 to 100
    df['Recovery_Score'] = df['Recovery_Score'].clip(0, 100)

    return df

def process_data():
    # Call load_data() to get the cleaned DataFrame
    df = load_data()

    # Call calculate_recovery_score() to add the Recovery Score
    df = calculate_recovery_score(df)

    # Return the final processed DataFrame
    return df

