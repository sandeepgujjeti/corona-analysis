import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="COVID-19 Analysis Dashboard",
    layout="wide"
)

# ---------------- TITLE ----------------
st.title("🇮🇳 COVID-19 Analysis Dashboard (India)")
st.markdown("Clean, compact dashboard built using **Streamlit + Python**")

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F2F2F2;
    }
    </style>
    """,
    unsafe_allow_html=True
)


# ---------------- LOAD DATA ----------------
df = pd.read_csv("india_covid_sample_data.csv")
df["date"] = pd.to_datetime(df["date"])


# ---------------- DATA PREVIEW ----------------
with st.expander("📄 Dataset Preview"):
    st.dataframe(df.head())

# ---------------- KPI METRICS ----------------
total_cases = int(df["total_cases"].iloc[-1])
total_deaths = int(df["total_deaths"].iloc[-1])
peak_deaths = int(df["new_deaths"].max())
peak_date = df.loc[df["new_deaths"].idxmax(), "date"].date()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Cases", f"{total_cases:,}")
col2.metric("Total Deaths", f"{total_deaths:,}")
col3.metric("Peak Daily Deaths", f"{peak_deaths:,}")
col4.metric("Peak Death Date", str(peak_date))

st.markdown("---")

# ---------------- HELPER FUNCTION ----------------
def small_plot(figsize=(5, 3)):
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax

# ---------------- ROW 1 ----------------
st.subheader("📈 Daily Trends")

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = small_plot()
    ax1.plot(df["date"], df["new_cases"], color="#1F77B4")
    ax1.set_title("Daily New COVID-19 Cases", fontsize=10)
    ax1.tick_params(axis="x", rotation=45, labelsize=8)
    ax1.tick_params(axis="y", labelsize=8)
    st.pyplot(fig1)

with col2:
    fig2, ax2 = small_plot()
    ax2.bar(df["date"], df["new_deaths"], color="#D62728")
    ax2.set_title("Daily COVID-19 Deaths", fontsize=10)
    ax2.tick_params(axis="x", rotation=45, labelsize=8)
    ax2.tick_params(axis="y", labelsize=8)
    st.pyplot(fig2)

# ---------------- ROW 2 ----------------
st.subheader("📊 Cumulative Impact")

col3, col4 = st.columns(2)

with col3:
    fig3, ax3 = small_plot()
    ax3.fill_between(df["date"], df["total_cases"], alpha=0.6, color="#2CA02C")
    ax3.set_title("Cumulative Total Cases", fontsize=10)
    ax3.tick_params(axis="x", rotation=45, labelsize=8)
    ax3.tick_params(axis="y", labelsize=8)
    st.pyplot(fig3)

with col4:
    fig4, ax4 = small_plot()
    ax4.plot(df["date"], df["total_deaths"], color="#7F7F7F")
    ax4.set_title("Cumulative Total Deaths", fontsize=10)
    ax4.tick_params(axis="x", rotation=45, labelsize=8)
    ax4.tick_params(axis="y", labelsize=8)
    st.pyplot(fig4)

# ---------------- ROW 3 ----------------
st.subheader("📉 Trend Analysis")

df["death_7day_avg"] = df["new_deaths"].rolling(window=7).mean()

fig5, ax5 = plt.subplots(figsize=(6, 3))
ax5.plot(df["date"], df["death_7day_avg"], color="#9467BD")
ax5.set_title("7-Day Moving Average of Deaths", fontsize=11)
ax5.tick_params(axis="x", rotation=45, labelsize=8)
ax5.tick_params(axis="y", labelsize=8)
st.pyplot(fig5)

# ---------------- INSIGHT ----------------
st.success(
    f"📌 Insight: Highest number of deaths ({peak_deaths}) occurred on {peak_date}"
)

st.markdown("---")
st.markdown("👤 **Project by:** Gujjeti Sandeep")
