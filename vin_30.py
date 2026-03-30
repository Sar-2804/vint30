import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# -------------------------------
# PAGE CONFIG
# -------------------------------
st.set_page_config(page_title="SIR Simulator", layout="wide")

# -------------------------------
# TITLE
# -------------------------------
st.title("🦠 Flu Outbreak Simulator (SIR Model)")
st.markdown("Interactive Epidemiology Dashboard")

# -------------------------------
# SIDEBAR
# -------------------------------
st.sidebar.header("🔧 Parameters")

population = st.sidebar.slider("Population", 100, 5000, 1000)
initial_infected = st.sidebar.slider("Initial Infected", 1, 100, 10)

beta = st.sidebar.slider("Infection Rate (β)", 0.0, 1.0, 0.3)
gamma = st.sidebar.slider("Recovery Rate (γ)", 0.01, 1.0, 0.1)
vaccination = st.sidebar.slider("Vaccination Rate", 0.0, 0.5, 0.05)

days = st.sidebar.slider("Days", 10, 200, 100)

# -------------------------------
# SIR MODEL
# -------------------------------
def run_sir(beta, gamma, v):
    S = population - initial_infected
    I = initial_infected
    R = 0

    S_list, I_list, R_list = [S], [I], [R]

    for _ in range(days):
        new_S = S - (beta * S * I / population) - (v * S)
        new_I = I + (beta * S * I / population) - (gamma * I)
        new_R = R + (gamma * I) + (v * S)

        # Fix negatives
        new_S = max(0, new_S)
        new_I = max(0, new_I)
        new_R = max(0, new_R)

        # Normalize population
        total = new_S + new_I + new_R
        if total > 0:
            new_S *= population / total
            new_I *= population / total
            new_R *= population / total

        S, I, R = new_S, new_I, new_R

        S_list.append(S)
        I_list.append(I)
        R_list.append(R)

    return S_list, I_list, R_list

# -------------------------------
# RUN MODEL
# -------------------------------
S, I, R = run_sir(beta, gamma, vaccination)

# -------------------------------
# GRAPH 1
# -------------------------------
st.subheader("📊 Infection Curve")

fig, ax = plt.subplots()
ax.plot(I, label="Infected", color="red")
ax.set_xlabel("Days")
ax.set_ylabel("People")
ax.legend()

st.pyplot(fig, use_container_width=True)

# -------------------------------
# GRAPH 2 (FULL SIR)
# -------------------------------
st.subheader("📊 SIR Model")

fig2, ax2 = plt.subplots()
ax2.plot(S, label="Susceptible", color="blue")
ax2.plot(I, label="Infected", color="red")
ax2.plot(R, label="Recovered", color="green")

ax2.legend()
st.pyplot(fig2, use_container_width=True)

# -------------------------------
# METRICS
# -------------------------------
st.subheader("📈 Metrics")

R0 = beta / gamma if gamma != 0 else 0
peak = max(I)
peak_day = int(np.argmax(I))

col1, col2, col3 = st.columns(3)
col1.metric("R₀", f"{R0:.2f}")
col2.metric("Peak Infected", round(peak))
col3.metric("Peak Day", peak_day)

# -------------------------------
# STATUS
# -------------------------------
st.subheader("📉 Outbreak Status")

if peak < population * 0.2:
    st.success("Curve Flattened ✅")
elif peak < population * 0.5:
    st.warning("Moderate Spread ⚠️")
else:
    st.error("Severe Outbreak ❌")

# -------------------------------
# DOWNLOAD DATA
# -------------------------------
df = pd.DataFrame({"S": S, "I": I, "R": R})
st.download_button("⬇️ Download Data", df.to_csv(index=False), "sir_data.csv")

# -------------------------------
# INFO
# -------------------------------
st.subheader("📘 About")

st.write("""
This app simulates disease spread using the SIR model.

- S → Susceptible  
- I → Infected  
- R → Recovered  

R₀ determines how fast the disease spreads.
""")