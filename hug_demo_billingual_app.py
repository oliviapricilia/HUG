import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# Language toggle
lang = st.radio("Choose Language / Pilih Bahasa", ["English", "Bahasa Indonesia"])

# Text dictionary
TEXT = {
    "title": {
        "English": "HUG – Holding Us Great",
        "Bahasa Indonesia": "HUG – Merangkul Kita Hebat"
    },
    "subtitle": {
        "English": "Mood & Crisis Trajectory Simulator",
        "Bahasa Indonesia": "Simulasi Mood & Krisis Emosional"
    },
    "mood_slider": {
        "English": "How are you feeling right now?",
        "Bahasa Indonesia": "Bagaimana perasaanmu sekarang?"
    },
    "bullying_check": {
        "English": "Have you experienced bullying or social stress recently?",
        "Bahasa Indonesia": "Apakah kamu mengalami bullying atau stres sosial baru-baru ini?"
    },
    "simulate_button": {
        "English": "Run Simulation",
        "Bahasa Indonesia": "Jalankan Simulasi"
    },
    "outcome_ok": {
        "English": "Trajectory appears stable. Keep supporting yourself.",
        "Bahasa Indonesia": "Trajektori terlihat stabil. Terus dukung dirimu."
    },
    "outcome_risk": {
        "English": "Trajectory indicates emotional collapse risk. Reach out or seek help.",
        "Bahasa Indonesia": "Trajektori menunjukkan risiko kejatuhan emosi. Hubungi seseorang atau cari bantuan."
    }
}

# App title
st.title(TEXT["title"][lang])
st.subheader(TEXT["subtitle"][lang])

# Mood input
mood0 = st.slider(TEXT["mood_slider"][lang], 0, 100, 50)

# Bullying check
bullying_input = st.selectbox(TEXT["bullying_check"][lang], ["No", "Maybe", "Yes"])
stress_modifier = {"No": 0.05, "Maybe": 0.1, "Yes": 0.2}[bullying_input]

# Simulation parameters
# Parameters
T = 50
mu = 0.5  # small positive drift (mood tends to recover)
theta = 5
kappa = 0.3
eta = 1.0
sigma_J = 5
p_jump = 0.05 + stress_modifier  # more realistic jump frequency

# Simulation
if st.button(TEXT["simulate_button"][lang]):
    mood = [mood0]
    vol = [theta]
    dt = 1
    collapse_threshold = 30
    np.random.seed(42)

    for t in range(T):
        d_sigma = kappa * (theta - vol[-1]) * dt + eta * np.random.normal()
        sigma_t = max(0.1, vol[-1] + d_sigma)
        dW = np.random.normal() * np.sqrt(dt)

        # Jump: sometimes negative, sometimes positive
        if np.random.rand() < p_jump:
            jump_direction = np.random.choice([-15, 10], p=[0.7, 0.3])
            jump = np.random.normal(jump_direction, sigma_J)
        else:
            jump = 0

        dM = mu * dt + sigma_t * dW + jump
        M_t = max(0, min(100, mood[-1] + dM))
        vol.append(sigma_t)
        mood.append(M_t)
   
    # Plotting
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 6), sharex=True)
    ax1.plot(mood, label="Mood", color="blue", linewidth=2)
    ax1.axhline(collapse_threshold, color='red', linestyle='--', label="Collapse Threshold")
    ax1.set_ylabel("Mood Level")
    ax1.set_title("Mood Trajectory")
    ax1.legend()

    ax2.plot(vol, label="Volatility", color="purple", linewidth=2)
    ax2.set_xlabel("Time")
    ax2.set_ylabel("Volatility")
    ax2.set_title("Volatility Over Time")
    ax2.legend()

    st.pyplot(fig)

    if any([m < collapse_threshold for m in mood]):
        st.error(TEXT["outcome_risk"][lang])
    else:
        st.success(TEXT["outcome_ok"][lang])

    st.markdown("---")
    st.caption("HUG demo – not a diagnostic tool. / demo HUG – bukan alat diagnosis.")
