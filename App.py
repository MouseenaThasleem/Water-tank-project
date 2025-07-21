import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt

# App title
st.set_page_config(page_title="Water Tank Fill Time Calculator", layout="centered")
st.title("💧 Water Tank Fill Time Calculator")
st.markdown("Estimate how long it takes to fill a water tank using integration of a rate function R(t).")

# Input
rate_expr = st.text_input("📈 Enter rate function R(t) in liters/min (e.g. 4*t, 10, 3*sin(t)+5)", value="4*t")
capacity = st.number_input("🛢️ Enter tank capacity (liters)", min_value=1.0, value=100.0)

# Define symbol and parse expression
t = sp.symbols('t')
try:
    R = sp.sympify(rate_expr)
except (sp.SympifyError, TypeError):
    st.error("❌ Invalid function. Please enter a valid rate expression.")
    st.stop()

# Integration to get volume function
V = sp.integrate(R, t)

# Calculate time to fill tank
time_vals = np.linspace(0, 100, 1000)
R_func = sp.lambdify(t, R, 'numpy')
V_func = sp.lambdify(t, V, 'numpy')

volumes = V_func(time_vals)
valid_times = time_vals[np.where(volumes >= capacity)]

if valid_times.size > 0:
    fill_time = round(valid_times[0], 2)
    st.success(f"⏱️ Estimated time to fill the tank: **{fill_time} minutes**")

    # Plotting
    st.subheader("📊 Flow Rate Over Time")
    x_vals = np.linspace(0, fill_time + 2, 200)

    try:
        y_vals = R_func(x_vals)
        if np.isscalar(y_vals):
            y_vals = np.full_like(x_vals, y_vals)
    except Exception as e:
        y_vals = np.zeros_like(x_vals)
        st.error(f"Error evaluating rate function: {e}")

    fig, ax = plt.subplots()
    ax.plot(x_vals, y_vals, color='blue', label=f"R(t) = {rate_expr}")
    ax.set_xlabel("Time (t) [minutes]")
    ax.set_ylabel("Flow Rate [liters/min]")
    ax.set_title("Flow Rate vs Time")
    ax.grid(True)
    ax.legend()
    st.pyplot(fig)

else:
    st.warning("⚠️ No valid solution. Try adjusting the function or capacity.")










