import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# Setup
st.set_page_config(page_title="Water Tank Fill Time", layout="centered")
st.title("💧 Water Tank Fill Time Calculator")
st.markdown("Estimate how long it takes to fill a tank using a rate function R(t) in **liters/minute**.")

# Tank capacity input
capacity = st.number_input("🛢️ Tank Capacity (liters):", min_value=1.0, value=100.0)

# Function selection
preset = st.selectbox("📈 Choose Flow Rate Type", [
    "Constant (e.g. 5)",
    "Linear (e.g. 4*t)",
    "Decreasing (e.g. 10 - t)",
    "Sinusoidal (e.g. 5*sin(t))",
    "Custom Input"
])

# Choose expression based on preset
if preset == "Constant (e.g. 5)":
    rate_input = "5"
elif preset == "Linear (e.g. 4*t)":
    rate_input = "4*t"
elif preset == "Decreasing (e.g. 10 - t)":
    rate_input = "10 - t"
elif preset == "Sinusoidal (e.g. 5*sin(t))":
    rate_input = "5*sin(t)"
else:
    rate_input = st.text_input("✍️ Enter your flow rate function R(t):", "4*t")

# Symbol
t = sp.symbols('t')

# Try to parse the function
try:
    R = sp.sympify(rate_input)
    R_func = sp.lambdify(t, R, 'numpy')
except (sp.SympifyError, TypeError):
    st.error("❌ Invalid function. Please use math syntax like 5, 4*t, 10 - t.")
    st.stop()

# Volume integration
V = sp.integrate(R, t)
V_func = sp.lambdify(t, V, 'numpy')

# Time range and volumes
time_range = np.linspace(0, 100, 1000)
volumes = V_func(time_range)

# Estimate fill time
valid_times = time_range[volumes >= capacity]
if valid_times.size > 0:
    fill_time = round(valid_times[0], 2)
    st.success(f"⏱️ Estimated time to fill the tank: **{fill_time} minutes**")

    # Plotting
    st.subheader("📊 Flow Rate vs Time")
    x_vals = np.linspace(0, fill_time + 2, 200)

    try:
        y_vals = R_func(x_vals)
        if np.isscalar(y_vals):
            y_vals = np.full_like(x_vals, y_vals)
        elif len(y_vals) != len(x_vals):
            y_vals = np.resize(y_vals, x_vals.shape)
    except Exception as e:
        y_vals = np.zeros_like(x_vals)
        st.error(f"⚠️ Error evaluating flow function: {e}")

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, label=f"R(t) = {rate_input}", color='blue')
    ax.set_xlabel("Time [minutes]")
    ax.set_ylabel("Flow Rate [liters/min]")
    ax.set_title("Flow Rate Over Time")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)
else:
    st.warning("⚠️ The tank never fills within 100 minutes. Try a higher flow rate or different function.")






