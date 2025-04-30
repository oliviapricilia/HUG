import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="HUG – Personalized Mood Simulator", layout="centered")

# --- Language toggle ---
lang = st.radio("\U0001F310 Language / Bahasa", ["English", "Bahasa Indonesia"])

# --- Crisis Mode & Bullying SOS ---
if st.button("🆘 I'm not feeling okay (Activate Crisis Mode)"):
    st.markdown("## 🆘 Crisis Mode Activated")
    st.markdown("You're not alone. Let's take this one small step at a time.")

    with st.expander("📦 Emergency Grounding Toolkit"):
        st.markdown("""
- Take a breath: Inhale for 4 seconds, hold for 4, exhale for 6.  
- Name 3 things you see, 2 you hear, 1 you feel.  
- Grab a glass of water or walk to a window.
        """)

    with st.expander("💬 Try typing out what you're feeling"):
        user_input = st.text_area("What’s happening for you right now?")
        if user_input:
            st.markdown("✅ Thank you for sharing. Just typing it out can help shift the weight a little.")

    with st.expander("📞 Helpful Resources"):
        st.markdown("""
- **Befrienders Worldwide**: [https://www.befrienders.org](https://www.befrienders.org)  
- **Indonesia (Samaritans)**: Call 021-500-454  
- **UK (Samaritans)**: Call 116 123  
- **Text a friend** you trust and just say: "Hey, can we talk?"
        """)

    st.stop()

if st.button("🚩 Help, I’m getting bullied"):
    st.markdown("## 💬 Bullying Support Bot")
    st.markdown("That’s hard. Let’s talk it through – anonymously and safely.")

    bullying_input = st.text_area("What’s been going on?")
    if bullying_input:
        st.markdown("🫂 Thank you for sharing. No one deserves that. You're not overreacting.")
        st.markdown("You might try keeping a small log of what happens and when, and talk to someone you trust. I'm here for more support anytime.")

    st.stop()

# --- Input Labels Dictionary (English only for now) ---
LABELS = {
    "title": "HUG – Holding Us Great",
    "subtitle": "\U0001F504 Personalized Mood Trajectory Simulator",
    "simulate_btn": "Run My Personalized Simulation",
    "feedback_ok": "✅ Your mood trajectory looks stable and adaptive.",
    "feedback_risk": "⚠️ Your simulation shows risk of approaching an emotional tipping point. This may be a good moment to reach out or slow down."
}

st.title(LABELS["title"])
st.subheader(LABELS["subtitle"])

# --- User Sliders ---
recovery_input = st.slider("How fast do you recover after emotional setbacks?", 0, 10, 5)
instability_input = st.slider("How often does your mood fluctuate unexpectedly?", 0, 10, 5)
impact_input = st.slider("How strongly do negative events affect you?", 0, 10, 5)
jumpiness_input = st.slider("How often do unexpected emotional events happen?", 0, 10, 3)
mood0 = st.slider("Your mood right now:", 0, 100, 50)

bullying_status = st.selectbox("Have you experienced bullying or social stress recently?", ["No", "Maybe", "Yes"])
stress_modifier = {"No": 0.0, "Maybe": 0.05, "Yes": 0.1}[bullying_status]

# --- Parameter Mapping ---
mu = recovery_input / 10
sigma = 1 + (instability_input * 0.9)
mu_J = -3 * impact_input
sigma_J = 5
p_jump = 0.01 + (jumpiness_input / 100) + stress_modifier

# --- Simulation ---
T = 50
collapse_threshold = 30

if st.button(LABELS["simulate_btn"]):
    mood = [mood0]
    np.random.seed(42)

    for t in range(T):
        dW = np.random.normal()
        jump = np.random.normal(mu_J, sigma_J) if np.random.rand() < p_jump else 0
        dM = mu + sigma * dW + jump
        M_t = max(0, min(100, mood[-1] + dM))
        mood.append(M_t)

    # Plot
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(mood, label="Mood", color="blue")
    ax.axhline(collapse_threshold, color='red', linestyle='--', label="Tipping Point")
    ax.set_xlabel("Time")
    ax.set_ylabel("Mood Level")
    ax.legend()
    st.pyplot(fig)

    # Outcome
    if any(m < collapse_threshold for m in mood):
        st.error(LABELS["feedback_risk"])
    else:
        st.success(LABELS["feedback_ok"])

    st.markdown("---")
    st.markdown("### 📐 Model Explanation")
    st.latex(r'dM_t = \mu\,dt + \sigma\,dW_t + J_t\,dN_t')
    st.markdown("""
This model assumes mood changes with:
- \( \mu \): recovery tendency
- \( \sigma \): natural emotional volatility
- \( J_t \): emotional shock size
- \( dN_t \): random occurrence of shocks (e.g. social conflict, trauma)
    """)

# --- HUG Info Section ---
st.markdown("## 💬 About HUG")
with st.expander("🌍 What HUG Aims to Solve"):
    st.markdown("""
1. **Access** – Therapy is expensive, rare, or taboo.
2. **Stigma** – People fear speaking up until it’s too late.
3. **Delay** – Lack of early support leads to help only at crisis points.
4. **Overload** – Young professionals and students are silently burning out.
5. **Cultural Mismatch** – Mental health tools often miss local realities.
    """)

with st.expander("👥 Who HUG Is For"):
    st.markdown("""
- **Teenagers/Students** – Facing bullying, anxiety, or academic pressure.
- **Young Professionals** – Experiencing quiet burnout, low support.
- **Suicide-vulnerable groups** – Especially in academia.
- **Supporters** – Parents, teachers, and managers who want to help.
    """)

with st.expander("🛠 Features (Early Version)"):
    st.markdown("""
- **Emotional Check-in Bot** – Mood check & daily prompts.
- **Guided Journaling** – Adaptive mood pattern tracking.
- **Mood Volatility Analysis** – Quant-style emotional risk modeling.
- **Localized Psychoeducation** – Mental health insights in context.
- **Burnout Dashboard** – Visual overview of mood/stress levels.
- **Escalation Paths** – Help, therapist chat, or peer community.
- **Crisis Mode** – A supportive chatbot and immediate resources.
    """)
