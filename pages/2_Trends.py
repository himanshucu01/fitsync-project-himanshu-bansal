import streamlit as st
import pandas as pd
import plotly.express as px
from modules.processor import process_data

# Set the Streamlit page configuration
st.set_page_config(layout="wide", page_title="FitSync - Trends and Insights")

# Add a title to the page
st.title("Trends and Insights")

# Sidebar for dynamic filtering
st.sidebar.header("Filters")
time_range = st.sidebar.selectbox(
    "Select Time Range",
    options=["Last 7 Days", "Last 30 Days", "All Time"],
    index=2
)

# Load and process the data
df = process_data()

# Filter the dataframe based on the selected time range
if time_range == "Last 7 Days":
    filtered_df = df[df['Date'] >= (df['Date'].max() - pd.Timedelta(days=7))]
elif time_range == "Last 30 Days":
    filtered_df = df[df['Date'] >= (df['Date'].max() - pd.Timedelta(days=30))]
else:
    filtered_df = df

# Calculate and display summary statistics
st.subheader("Summary Statistics")
summary_stats = filtered_df[['Recovery_Score', 'Sleep_Hours', 'Steps', 'Calories_Burned']].describe().T
# Display only mean, min and max statistics
st.write(summary_stats[['mean', 'min', 'max']])

# Ensure 'Month' is converted to a string for JSON serialization
filtered_df['Month'] = filtered_df['Date'].dt.to_period('M').astype(str)
# Recalculate monthly average with 'Month' as a string
monthly_avg_recovery = filtered_df.groupby('Month')['Recovery_Score'].mean().reset_index()

# Plot: Monthly Average Recovery Score with Month now as a string
st.subheader("Monthly Average Recovery Score")
fig1 = px.line(
    monthly_avg_recovery,
    x='Month',
    y='Recovery_Score',
    title='Average Recovery Score by Month'
)
fig1.update_xaxes(type='category')
st.plotly_chart(fig1, use_container_width=True)

# Plots: Histograms
hist_cols = st.columns(2)

# Histogram for Steps
fig2 = px.histogram(
    filtered_df,
    x='Steps',
    title='Distribution of Daily Steps'
)
hist_cols[0].plotly_chart(fig2, use_container_width=True)

# Histogram for Calories Burned
fig3 = px.histogram(
    filtered_df,
    x='Calories_Burned',
    title='Distribution of Calories Burned'
)
hist_cols[1].plotly_chart(fig3, use_container_width=True)

# Another set of histograms
hist_cols2 = st.columns(2)

# Histogram for Recovery Score
fig4 = px.histogram(
    filtered_df,
    x='Recovery_Score',
    title='Distribution of Recovery Scores'
)
hist_cols2[0].plotly_chart(fig4, use_container_width=True)

# Histogram for Sleep Hours
fig5 = px.histogram(
    filtered_df,
    x='Sleep_Hours',
    title='Distribution of Sleep Hours'
)
hist_cols2[1].plotly_chart(fig5, use_container_width=True)



