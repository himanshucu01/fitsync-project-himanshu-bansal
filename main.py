import streamlit as st
import pandas as pd
import plotly.express as px
from modules.processor import process_data

# ─────────────────────────────────────────────
# PAGE CONFIG
# ─────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="FitSync Dashboard",
    page_icon="💪"
)

# ─────────────────────────────────────────────
# THEMES (SEXY + READABLE)
# ─────────────────────────────────────────────
THEMES = {
    "Default": {"bg": "#0f1117", "card": "#1a1d25", "text": "#f5f7ff", "muted": "#a1a1aa", "accent": "#6366f1"},
    "Light": {"bg": "#f7f7fb", "card": "#ffffff", "text": "#111827", "muted": "#6b7280", "accent": "#2563eb"},
    "Dark": {"bg": "#0b0d12", "card": "#151823", "text": "#ffffff", "muted": "#9ca3af", "accent": "#22c55e"},
    "Blue": {"bg": "#0b1220", "card": "#111a2e", "text": "#e0f2fe", "muted": "#7dd3fc", "accent": "#38bdf8"},
}

if "theme" not in st.session_state:
    st.session_state.theme = "Default"

# ─────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────
st.sidebar.title("⚙️ Controls")

st.sidebar.subheader("🎨 Theme")

cols = st.sidebar.columns(2)
theme_keys = list(THEMES.keys())

for i, name in enumerate(theme_keys):
    if cols[i % 2].button(name):
        st.session_state.theme = name
        st.rerun()

st.sidebar.markdown(f"**Current Theme:** {st.session_state.theme}")

time_range = st.sidebar.selectbox(
    "📅 Time Range",
    ["Last 7 Days", "Last 30 Days", "All Time"]
)

# ─────────────────────────────────────────────
# APPLY THEME (FIXED UI + TEXT VISIBILITY)
# ─────────────────────────────────────────────
theme = THEMES[st.session_state.theme]

st.markdown(f"""
<style>
.stApp {{
    background: {theme['bg']} !important;
    color: {theme['text']} !important;
    font-family: 'Inter', sans-serif;
}}

h1, h2, h3, h4, h5, p, span, label {{
    color: {theme['text']} !important;
}}

[data-testid="stSidebar"] {{
    background: {theme['card']} !important;
    border-right: 1px solid rgba(255,255,255,0.06);
}}

div[data-testid="metric-container"] {{
    background: {theme['card']} !important;
    border-radius: 16px;
    padding: 18px;
    border: 1px solid rgba(255,255,255,0.06);
}}

[data-testid="stMetricValue"] {{
    color: {theme['text']} !important;
    font-size: 22px !important;
    font-weight: 700;
}}

.stButton>button {{
    background: transparent;
    color: {theme['text']} !important;
    border: 1px solid rgba(255,255,255,0.15);
    border-radius: 10px;
}}

.stButton>button:hover {{
    border-color: {theme['accent']};
    transform: scale(1.02);
}}

</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────
# TITLE
# ─────────────────────────────────────────────
st.title("FitSync - Advanced Health Analytics Dashboard")
st.markdown("Smart fitness insights powered by your data 🚀")

# ─────────────────────────────────────────────
# LOAD DATA
# ─────────────────────────────────────────────
df = process_data()

# ─────────────────────────────────────────────
# CLEAN DATA
# ─────────────────────────────────────────────
df.columns = df.columns.str.lower()
df["date"] = pd.to_datetime(df["date"], errors="coerce")
df = df.dropna(subset=["date"])

# ─────────────────────────────────────────────
# FILTERING (SAFE)
# ─────────────────────────────────────────────
today = df["date"].max()

if time_range == "Last 7 Days":
    start_date = today - pd.Timedelta(days=7)
elif time_range == "Last 30 Days":
    start_date = today - pd.Timedelta(days=30)
else:
    start_date = df["date"].min()

filtered_df = df[df["date"] >= start_date]

if filtered_df.empty:
    st.warning("No data available for selected filter.")
    st.stop()

# ─────────────────────────────────────────────
# METRICS
# ─────────────────────────────────────────────
avg_steps = filtered_df["steps"].mean()
avg_sleep = filtered_df["sleep_hours"].mean()
avg_recovery = filtered_df["recovery_score"].mean()

col1, col2, col3 = st.columns(3)

col1.metric("👣 Steps", f"{avg_steps:.0f}")
col2.metric("😴 Sleep", f"{avg_sleep:.1f} hrs")
col3.metric("⚡ Recovery", f"{avg_recovery:.0f}")

st.markdown("---")

# ─────────────────────────────────────────────
# CHARTS
# ─────────────────────────────────────────────
c1, c2 = st.columns(2)

with c1:
    st.subheader("📈 Recovery Trend")
    fig1 = px.line(filtered_df, x="date", y="recovery_score", markers=True)
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    st.subheader("😴 Sleep vs Recovery")

    fig2 = px.scatter(
        filtered_df,
        x="sleep_hours",
        y="recovery_score",
        color="steps",
        size="steps"
    )
    st.plotly_chart(fig2, use_container_width=True)

c3, c4 = st.columns(2)

# ─────────────────────────────────────────────
# SAFE TRENDLINE (NO CRASH EVER)
# ─────────────────────────────────────────────
with c3:
    st.subheader("👣 Steps vs Recovery")

    try:
        fig3 = px.scatter(
            filtered_df,
            x="steps",
            y="recovery_score",
            trendline="ols"   # requires statsmodels
        )
    except:
        fig3 = px.scatter(
            filtered_df,
            x="steps",
            y="recovery_score"
        )

    st.plotly_chart(fig3, use_container_width=True)

with c4:
    st.subheader("❤️ Heart Rate vs Recovery")

    if "heart_rate_bpm" in filtered_df.columns:
        fig4 = px.scatter(
            filtered_df,
            x="heart_rate_bpm",
            y="recovery_score"
        )
        st.plotly_chart(fig4, use_container_width=True)

# ─────────────────────────────────────────────
# DATA VIEW
# ─────────────────────────────────────────────
with st.expander("📊 View Raw Data"):
    st.dataframe(filtered_df)