# Save your Streamlit app code as a .py file

code = '''
import streamlit as st
from sympy import symbols, sympify, lambdify
from scipy.integrate import quad

st.title("🚰 Water Tank Fill Time Calculator (Using Calculus)")

rate_input = st.text_input("Enter rate function R(t) (e.g. 4*t or 10 - t):", "4*t")
capacity = st.number_input("Enter tank capacity (liters):", min_value=0.0, step=1.0, value=50.0)

if st.button("Calculate Fill Time"):
    t = symbols('t')
    try:
        R = sympify(rate_input)
        R_func = lambdify(t, R, modules=['numpy'])

        def compute_volume(upto_t):
            result, _ = quad(R_func, 0, upto_t)
            return result

        def find_fill_time(capacity, max_time=100, tolerance=0.01):
            low = 0
            high = max_time
            while high - low > tolerance:
                mid = (low + high) / 2
                volume = compute_volume(mid)
                if volume < capacity:
                    low = mid
                else:
                    high = mid
            return (low + high) / 2

        time_required = find_fill_time(capacity)
        st.success(f"⏱️ Estimated time to fill the tank: **{time_required:.2f} minutes**")

    except Exception as e:
        st.error(f"Error: {e}")
'''

with open("tank_simulator.py", "w") as f:
    f.write(code)
