import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

# Page settings
st.set_page_config(page_title="Water Tank Calculator", page_icon="💧", layout="centered")

# Title and description
st.title("💧 Water Tank Fill Time Calculator")
st.markdown("Estimate how long it takes to fill a water tank using **integration of a rate function** R(t).")

# Sidebar inputs
with st.sidebar:
    st.header("🔧 Inputs")
    rate_input = st.text_input("Enter rate function R(t):", "2*t")
    capacity = st.number_input("Tank capacity (liters):", min_value=0.0, value=50.0, step=1.0)

# Processing and calculation
t = sp.Symbol('t')
try:
    R = sp.sympify(rate_input)
    R_integrated = sp.integrate(R, (t, 0, t))

    # Solve ∫R(t)dt = Capacity
    eq = sp.Eq(R_integrated, capacity)
    sol = sp.solve(eq, t)

    valid_solutions = [float(s.evalf()) for s in sol if s.is_real and s.evalf() > 0]

    if valid_solutions:
        fill_time = round(valid_solutions[0], 2)
        st.success(f"⏱ Estimated time to fill the tank: **{fill_time} minutes**")

        # Plot the flow rate R(t)
        st.subheader("📊 Flow Rate vs Time")
        R_func = sp.lambdify(t, R, 'numpy')
        x_vals = np.linspace(0, fill_time + 2, 200)
        y_vals = R_func(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label=f"R(t) = {rate_input}", color='blue')
        ax.set_xlabel("Time (t) [minutes]")
        ax.set_ylabel("Rate [liters/min]")
        ax.set_title("Flow Rate Over Time")
        ax.grid(True)
        ax.legend()
        st.pyplot(fig)
    else:
        st.warning("No valid (positive) solution found. Try a different R(t) or increase the capacity.")

except Exception as e:
    st.error(f"⚠️ Invalid input: {e}")
