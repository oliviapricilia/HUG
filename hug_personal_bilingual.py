import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="HUG – Personalized Mood Simulation", layout="centered")
st.title("HUG – Holding Us Great")
st.subheader("🔁 Personalized Mood Trajectory Simulator")

# Input: personalization sliders
st.markdown("### 🧠 Tell us about yourself")

mu_slider = st.slider("I recover quickly from emotional setbacks.", 0.0, 1.0, 0.5)
sigma_slider = st.slider("My mood changes a lot even without a reason.", 1.0, 10.0, 5.0)
muJ_slider = st.slider("When I get bad news, I spiral hard.", -30.0, 0.0, -15.0)

# Mood baseline
mood0 = st.slider("Your mood right now:", 0, 100, 50)

# Simulation parameters
T = 50
dt = 1
sigma_J = 5
p_jump = 0.1
collapse_threshold = 30

# Run simulation
if st.button("Run My Personalized Simulation"):
    mu = mu_slider
    sigma = sigma_slider
    mu_J = muJ_slider

    mood = [mood0]
    np.random.seed(42)

    for t in range(T):
        dW = np.random.normal() * np.sqrt(dt)
        jump = np.random.normal(mu_J, sigma_J) if np.random.rand() < p_jump else 0
        dM = mu * dt + sigma * dW + jump
        M_t = max(0, min(100, mood[-1] + dM))
        mood.append(M_t)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(mood, label="Mood", color="blue", linewidth=2)
    ax.axhline(collapse_threshold, color='red', linestyle='--', label="Collapse Threshold")
    ax.set_xlabel("Time")
    ax.set_ylabel("Mood Level")
    ax.set_title("Your Personalized Mood Trajectory")
    ax.legend()
    st.pyplot(fig)

    # Output message
    if any([m < collapse_threshold for m in mood]):
        st.error("⚠️ Your emotional trajectory shows collapse risk. Consider seeking support.")
    else:
        st.success("✅ Your mood trajectory looks stable and adaptive.")

    st.caption("This simulation is not a diagnostic tool. It’s a personalized model based on your responses.")
