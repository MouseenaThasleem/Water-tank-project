import streamlit as st
import sympy as sp
import matplotlib.pyplot as plt
import numpy as np

# Streamlit App Configuration
st.set_page_config(page_title="Water Tank Calculator", page_icon="💧", layout="centered")
st.title("💧 Water Tank Fill Time Calculator")
st.markdown("Estimate how long it takes to fill a water tank using integration of a rate function R(t).")

# Sidebar Flow Type Selection
with st.sidebar:
    st.header("🔧 Settings")
    flow_type = st.selectbox("Choose Flow Type", ["Constant Flow", "Increasing Flow", "Decreasing Flow", "Custom Function"])

    if flow_type == "Constant Flow":
        rate_expr = "5"
        st.caption("💡 Constant flow: R(t) = 5 liters/min")
    elif flow_type == "Increasing Flow":
        rate_expr = "2*t"
        st.caption("💡 Flow increases over time: R(t) = 2t")
    elif flow_type == "Decreasing Flow":
        rate_expr = "10 - t"
        st.caption("💡 Flow decreases over time: R(t) = 10 - t")
    else:
        rate_expr = st.text_input("Enter rate function R(t):", value="2*t")

    capacity = st.number_input("Tank capacity (liters):", min_value=0.0, value=50.0, step=1.0)

# Math Part
t = sp.Symbol('t')
try:
    R = sp.sympify(rate_expr)
    integral = sp.integrate(R, (t, 0, t))
    equation = sp.Eq(integral, capacity)
    solutions = sp.solve(equation, t)

    valid_times = [float(sol.evalf()) for sol in solutions if sol.is_real and sol.evalf() > 0]

    if valid_times:
        fill_time = round(valid_times[0], 2)
        st.success(f"⏱ Estimated time to fill the tank: **{fill_time} minutes**")

        # Plotting
        st.subheader("📊 Flow Rate Over Time")
        R_func = sp.lambdify(t, R, 'numpy')
        x_vals = np.linspace(0, fill_time + 2, 200)
        y_vals = R_func(x_vals)

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

except Exception as e:
    st.error(f"❌ Error in input: {e}")




