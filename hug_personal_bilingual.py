import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="HUG – Personalized Mood Simulator", layout="centered")

# Language selector
lang = st.radio("🌐 Language / Bahasa", ["English", "Bahasa Indonesia"])

# Dictionaries for labels
LABELS = {
    "title": {
        "English": "HUG – Holding Us Great",
        "Bahasa Indonesia": "HUG – Merangkul Kita Hebat"
    },
    "subtitle": {
        "English": "🔁 Personalized Mood Trajectory Simulator",
        "Bahasa Indonesia": "🔁 Simulasi Trajektori Mood Pribadi"
    },
    "sliders": {
        "recover": {
            "English": "How fast do you recover after emotional setbacks?",
            "Bahasa Indonesia": "Seberapa cepat kamu pulih setelah tekanan emosional?"
        },
        "recover_help": {
            "English": "0 = I stay upset for a long time, 10 = I bounce back quickly",
            "Bahasa Indonesia": "0 = Sangat sulit bangkit, 10 = Pulih sangat cepat"
        },
        "instability": {
            "English": "How often does your mood fluctuate unexpectedly?",
            "Bahasa Indonesia": "Seberapa sering mood kamu berubah tiba-tiba?"
        },
        "impact": {
            "English": "How strongly do negative events affect you?",
            "Bahasa Indonesia": "Seberapa besar dampak peristiwa negatif terhadapmu?"
        },
        "jumpiness": {
            "English": "How often do unexpected emotional events happen in your life?",
            "Bahasa Indonesia": "Seberapa sering kamu mengalami kejutan emosional?"
        },
        "mood_now": {
            "English": "Your mood right now:",
            "Bahasa Indonesia": "Mood kamu saat ini:"
        },
        "bullying": {
            "English": "Have you experienced bullying or social stress recently?",
            "Bahasa Indonesia": "Apakah kamu mengalami bullying atau tekanan sosial?"
        },
        "bullying_choices": ["No", "Maybe", "Yes"],
        "simulate_btn": {
            "English": "Run My Personalized Simulation",
            "Bahasa Indonesia": "Jalankan Simulasi Mood Saya"
        }
    },
    "feedback": {
        "ok": {
            "English": "✅ Your mood trajectory looks stable and adaptive.",
            "Bahasa Indonesia": "✅ Mood kamu terlihat stabil dan adaptif."
        },
        "risk": {
            "English": "⚠️ Mood simulation suggests emotional collapse risk. Consider reaching out.",
            "Bahasa Indonesia": "⚠️ Simulasi menunjukkan risiko kejatuhan emosi. Pertimbangkan mencari bantuan."
        }
    },
    "math_section": {
        "title": {
            "English": "📐 Model Explanation (Jump-Diffusion)",
            "Bahasa Indonesia": "📐 Penjelasan Model Emosional (Jump-Diffusion)"
        },
        "desc": {
            "English": """This model assumes your mood evolves over time with:
- **μ**: tendency to recover (drift)
- **σ**: natural instability (volatility)
- **J**: emotional shock (random jump)
- **dN**: Poisson trigger for surprise events

If mood drops below a threshold (e.g. 30), we flag emotional collapse risk.""",
            "Bahasa Indonesia": """Model ini mengasumsikan bahwa mood kamu berubah seiring waktu:
- **μ**: kecenderungan untuk pulih (drift)
- **σ**: ketidakstabilan alami (volatilitas)
- **J**: lonjakan emosional (shock acak)
- **dN**: proses kejadian acak (trauma/intervensi)

Jika mood turun di bawah ambang (misalnya 30), dianggap berisiko jatuh emosi."""
        }
    }
}

# Interface
st.title(LABELS["title"][lang])
st.subheader(LABELS["subtitle"][lang])

# Inputs
recovery_input = st.slider(
    LABELS["sliders"]["recover"][lang], 0, 10, 5,
    help=LABELS["sliders"]["recover_help"][lang]
)

instability_input = st.slider(LABELS["sliders"]["instability"][lang], 0, 10, 5)
impact_input = st.slider(LABELS["sliders"]["impact"][lang], 0, 10, 5)
jumpiness_input = st.slider(LABELS["sliders"]["jumpiness"][lang], 0, 10, 3)
mood0 = st.slider(LABELS["sliders"]["mood_now"][lang], 0, 100, 50)

bullying_input = st.selectbox(LABELS["sliders"]["bullying"][lang], LABELS["sliders"]["bullying_choices"])
stress_modifier = {"No": 0.0, "Maybe": 0.05, "Yes": 0.1}[bullying_input]

# Map inputs
mu = recovery_input / 10
sigma = 1 + (instability_input * 0.9)
mu_J = -3 * impact_input
sigma_J = 5
p_jump = 0.01 + (jumpiness_input / 100) + stress_modifier

# Simulate
T = 50
dt = 1
collapse_threshold = 30

if st.button(LABELS["sliders"]["simulate_btn"][lang]):
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
    ax.set_title("Mood Trajectory")
    ax.legend()
    st.pyplot(fig)

    # Output
    if any([m < collapse_threshold for m in mood]):
        st.error(LABELS["feedback"]["risk"][lang])
    else:
        st.success(LABELS["feedback"]["ok"][lang])

    st.markdown("---")
    st.markdown(LABELS["math_section"]["title"][lang])
    st.latex(r'dM_t = \mu\,dt + \sigma\,dW_t + J_t\,dN_t')
    st.markdown(LABELS["math_section"]["desc"][lang])

    st.caption("This is not a diagnostic tool / Ini bukan alat diagnosis medis.")
