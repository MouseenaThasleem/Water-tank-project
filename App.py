import streamlit as st
from sympy import symbols, sympify, lambdify
from scipy.integrate import quad
import matplotlib.pyplot as plt
import numpy as np

st.set_page_config(page_title="Water Tank Fill Time Estimator", layout="centered")

st.title("🚰 Water Tank Fill Time Estimator (Using Integration)")

# Inputs
rate_input = st.text_input("Enter flow rate function R(t) (e.g. 4*t, 10 - t, 5*sin(t), 5):", "4*t")
capacity = st.number_input("Enter tank capacity (liters):", min_value=0.0, step=1.0, value=50.0)

# Explanation hint
with st.expander("📘 Examples & Help"):
    st.markdown("""
    - **4*t** → Flow increases over time  
    - **10 - t** → Flow decreases  
    - **5*sin(t)** → Oscillating flow  
    - **5** → Constant flow  
    - Time unit is in **minutes**, and flow is in **liters/min**
    """)

# Define symbols
t = symbols('t')

def compute_volume(upto_t, R_func):
    result, _ = quad(R_func, 0, upto_t)
    return result

def find_fill_time(capacity, R_func, tolerance=0.01):
    low = 0
    high = 1
    while compute_volume(high, R_func) < capacity:
        high *= 2  # Double until volume > capacity
    while high - low > tolerance:
        mid = (low + high) / 2
        volume = compute_volume(mid, R_func)
        if volume < capacity:
            low = mid
        else:
            high = mid
    return (low + high) / 2

# Action
if st.button("🧮 Calculate Fill Time"):
    try:
        R = sympify(rate_input)
        R_func = lambdify(t, R, modules=['numpy'])

        # Calculate time to fill
        time_required = find_fill_time(capacity, R_func)
        st.success(f"⏱️ Estimated time to fill the tank: **{time_required:.2f} minutes**")

        # Plotting the flow rate
        times = np.linspace(0, time_required, 300)
        try:
            rates = R_func(times)
            fig, ax = plt.subplots()
            ax.plot(times, rates, color='blue')
            ax.set_title("Flow Rate vs Time")
            ax.set_xlabel("Time (minutes)")
            ax.set_ylabel("Flow Rate R(t) (liters/min)")
            ax.grid(True)
            st.pyplot(fig)
        except Exception:
            st.info("Plotting skipped: function may not support array input.")

    except Exception as e:
        st.error(f"❌ Error: {e}")






