import streamlit as st
import pandas as pd
from modules.processor import process_data
import plotly.express as px

# Set the Streamlit page configuration
st.set_page_config(layout="wide", page_title="FitSync")

# Add a title to the dashboard
st.title("FitSync - Personal Health Analytics")

# Sidebar for dynamic filtering
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["Last 7 Days", "Last 30 Days", "All Time"],
    index=2
)

# Use a three-column layout
a1, a2, a3 = st.columns(3)

# Load and process the data
df = process_data()

# Filter the dataframe based on the selected time range
if time_range == "Last 7 Days":
    filtered_df = df[df['Date'] >= (df['Date'].max() - pd.Timedelta(days=7))]
elif time_range == "Last 30 Days":
    filtered_df = df[df['Date'] >= (df['Date'].max() - pd.Timedelta(days=30))]
else:
    filtered_df = df

# Calculate averages from the filtered dataframe
average_steps = filtered_df['Steps'].mean()
average_sleep_hours = filtered_df['Sleep_Hours'].mean()
average_recovery_score = filtered_df['Recovery_Score'].mean()

# Display updated metrics in the respective columns
a1.metric(label="Average Steps", value=f"{average_steps:.0f}", delta=None)
a2.metric(label="Average Sleep Hours", value=f"{average_sleep_hours:.1f}", delta=None)
a3.metric(label="Average Recovery Score", value=f"{average_recovery_score:.1f}", delta=None)

# Display sections of the dashboard

# Introduction section
st.write("""
Welcome to FitSync, your personal health analytics dashboard. This modern approach allows you to track and understand your health data with ease.
Below you'll find insights into your daily activities, including sleep patterns, steps, and heart rate analytics.
""")

# Display the processed DataFrame
# st.dataframe(df)

# Additional plots and analytics will be added here as needed
# For example, visualizations of steps, heart rate, and sleep trends

# Create two columns for visualizations
col1, col2 = st.columns(2)

# Plot 1: Dual Line Chart for Recovery Score and Sleep Hours
fig1 = px.line(
    filtered_df,
    x='Date',
    y=['Recovery_Score', 'Sleep_Hours'],
    labels={'value': 'Metrics', 'variable': 'Metric', 'Date': 'Date'},
    title='Recovery Score and Sleep Trend'
)
fig1.update_layout(legend_title_text='Metric')
col1.plotly_chart(fig1, use_container_width=True)

# Plot 2: Scatter Plot for Recovery Score vs Steps, colored by Sleep Hours
fig2 = px.scatter(
    filtered_df,
    x='Steps',
    y='Recovery_Score',
    color='Sleep_Hours',
    title='Recovery Score vs Daily Steps',
    labels={'Steps': 'Daily Steps', 'Recovery_Score': 'Recovery Score', 'Sleep_Hours': 'Sleep Hours'}
)
col2.plotly_chart(fig2, use_container_width=True)

# Create another two columns for more visualizations
col3, col4 = st.columns(2)

# Plot 3: Scatter plot for Recovery Score vs Heart_Rate_bpm
fig3 = px.scatter(
    filtered_df,
    x='Heart_Rate_bpm',
    y='Recovery_Score',
    title='Recovery Score vs Resting Heart Rate',
    labels={'Heart_Rate_bpm': 'Resting Heart Rate (bpm)', 'Recovery_Score': 'Recovery Score'}
)
col3.plotly_chart(fig3, use_container_width=True)

# Plot 4: Line Chart for Calories_Burned trend over time
fig4 = px.line(
    filtered_df,
    x='Date',
    y='Calories_Burned',
    title='Daily Calories Burned Trend',
    labels={'Calories_Burned': 'Calories Burned', 'Date': 'Date'}
)
col4.plotly_chart(fig4, use_container_width=True)


