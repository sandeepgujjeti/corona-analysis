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
st.markdown("1‑Year Analysis using **Streamlit + Python**")

# ---------------- THEME‑AWARE BACKGROUND ----------------
st.markdown(
    """
    <style>
    @media (prefers-color-scheme: light) {
        .stApp {
            background-color: #F2F2F2;
            color: #1F2937;
        }
    }
    @media (prefers-color-scheme: dark) {
        .stApp {
            background-color: #0E1117;
            color: #FAFAFA;
        }
    }
    </style>
    """,
    unsafe_allow_html=True
)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("india_covid_1year_vacination_sample_data.csv")
df["date"] = pd.to_datetime(df["date"])

# ---------------- DATA PREVIEW ----------------
with st.expander("📄 Dataset Preview"):
    st.dataframe(df, use_container_width=True)

# ---------------- KPI METRICS ----------------
total_cases = int(df["confirmed_cases"].sum())
total_deaths = int(df["total_deaths"].sum())
total_recovered = int(df["recovered_cases"].sum())

peak_deaths = int(df["total_deaths"].max())
peak_date = df.loc[df["total_deaths"].idxmax(), "date"].date()

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Cases", f"{total_cases:,}")
col2.metric("Total Deaths", f"{total_deaths:,}")
col3.metric("Recovered", f"{total_recovered:,}")
col4.metric("Peak Death Month", str(peak_date))

st.markdown("---")

# ---------------- HELPER FUNCTION ----------------
def small_plot(figsize=(5, 3)):
    fig, ax = plt.subplots(figsize=figsize)
    return fig, ax

# ---------------- ROW 1: MONTHLY CASES & DEATHS ----------------
st.subheader("📈 Monthly Trends")

col1, col2 = st.columns(2)

with col1:
    fig1, ax1 = small_plot()
    ax1.plot(df["date"], df["confirmed_cases"], color="#2563EB")
    ax1.set_title("Monthly Confirmed Cases", fontsize=10)
    ax1.tick_params(axis="x", rotation=45, labelsize=8)
    ax1.tick_params(axis="y", labelsize=8)
    st.pyplot(fig1)

with col2:
    fig2, ax2 = small_plot()
    ax2.bar(df["date"], df["total_deaths"], color="#DC2626")
    ax2.set_title("Monthly Deaths", fontsize=10)
    ax2.tick_params(axis="x", rotation=45, labelsize=8)
    ax2.tick_params(axis="y", labelsize=8)
    st.pyplot(fig2)

# ---------------- ROW 2: VACCINATION DEATH ANALYSIS ----------------
st.subheader("💉 Deaths by Vaccination Status")

fig3, ax3 = plt.subplots(figsize=(6, 3))

ax3.plot(df["date"], df["deaths_unvaccinated"], label="Unvaccinated", color="#7C23AB")
ax3.plot(df["date"], df["deaths_after_1_dose"], label="1 Dose", color="#F59E0B")
ax3.plot(df["date"], df["deaths_after_2_doses"], label="2 Doses", color="#16A34A")

ax3.set_title("Deaths by Vaccination Status", fontsize=11)
ax3.legend(fontsize=8)
ax3.tick_params(axis="x", rotation=45, labelsize=8)
ax3.tick_params(axis="y", labelsize=8)

st.pyplot(fig3)

# ---------------- ROW 3: ALIVE POPULATION ----------------
st.subheader("🧍 Alive Population by Vaccination Status")

fig4, ax4 = plt.subplots(figsize=(6, 3))

ax4.stackplot(
    df["date"],
    df["alive_unvaccinated"],
    df["alive_after_1_dose"],
    df["alive_after_2_doses"],
    labels=["Unvaccinated", "1 Dose", "2 Doses"],
    colors=["#94A3B8", "#60A5FA", "#22C55E"]
)

ax4.legend(loc="upper left", fontsize=8)
ax4.tick_params(axis="x", rotation=45, labelsize=8)
ax4.tick_params(axis="y", labelsize=8)

st.pyplot(fig4)

# ---------------- ROW 4: SURVIVAL VS DEATH ----------------
st.subheader("⚖ Survival vs Death Comparison")

fig5, ax5 = plt.subplots(figsize=(5, 3))
ax5.bar(
    ["Recovered", "Deaths"],
    [total_recovered, total_deaths],
    color=["#16A34A", "#DC2626"]
)
ax5.set_ylabel("People Count")
st.pyplot(fig5)

# ---------------- INSIGHT ----------------
st.success(
    f"📌 Insight: Highest deaths ({peak_deaths}) occurred around {peak_date}"
)

st.markdown("---")
st.caption(
    "Note: Vaccination analysis is based on aggregated / educational data."
)
st.markdown("👤 **Project by:** Gujjeti Sandeep")
