import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import os

st.set_page_config(page_title="Moodrift + HUG", layout="wide")

# File persistence
DATA_FILE = "mood_log.csv"

# Load existing data
if os.path.exists(DATA_FILE):
    df_log = pd.read_csv(DATA_FILE)
    df_log["Date"] = pd.to_datetime(df_log["Date"]).dt.date
    st.session_state.log = df_log.to_dict("records")
else:
    st.session_state.log = []

if "letters" not in st.session_state:
    st.session_state.letters = []
if "anchors" not in st.session_state:
    st.session_state.anchors = []
if "crisis_mode" not in st.session_state:
    st.session_state.crisis_mode = False
if "bully_mode" not in st.session_state:
    st.session_state.bully_mode = False

# Language toggle
lang = st.sidebar.radio("🌐 Language / Bahasa", ["English", "Bahasa Indonesia"])

# Crisis buttons
st.sidebar.markdown("## 🆘 Support")
if st.sidebar.button("🆘 Crisis Mode"):
    st.session_state.crisis_mode = True
    st.session_state.bully_mode = False
if st.sidebar.button("🚩 I'm being bullied"):
    st.session_state.bully_mode = True
    st.session_state.crisis_mode = False
if st.sidebar.button("↩️ Exit Support"):
    st.session_state.crisis_mode = False
    st.session_state.bully_mode = False

# Crisis mode
if st.session_state.crisis_mode:
    st.title("🆘 Crisis Mode Activated")
    st.markdown("You're not alone. Let’s take this one small step at a time.")

    with st.expander("📦 Grounding Toolkit"):
        st.markdown("""
- Inhale 4s, hold 4s, exhale 6s.
- Name 3 things you see, 2 you hear, 1 you feel.
- Drink water. Look outside.
        """)

    with st.expander("💬 Talk to HUG"):
        with st.form("crisis_chat"):
            user_input = st.text_area("What’s happening?")
            if st.form_submit_button("Send") and user_input:
                st.markdown(f"🫂 You said: *{user_input}*")
                if any(x in user_input.lower() for x in ["suicide", "hopeless", "end it"]):
                    st.warning("💔 Please contact a crisis line or trusted person.")

    with st.expander("📞 Resources"):
        st.markdown("""
- **Befrienders Worldwide**: [https://www.befrienders.org](https://www.befrienders.org)  
- **Indonesia**: 021-500-454  
- **UK**: 116 123
        """)
    st.stop()

# Bullying mode
if st.session_state.bully_mode:
    st.title("💬 Bullying Support")
    with st.form("bully_chat"):
        msg = st.text_area("What happened?")
        if st.form_submit_button("Send") and msg:
            st.success("🫂 Thanks for sharing. That matters.")
    st.stop()

# Main navigation
page = st.sidebar.radio("Navigate", ["Log Mood", "Mood Report", "Letter to Self", "Reality Anchors", "Mood Simulation"])

# ---------- 1. LOG MOOD ----------
if page == "Log Mood":
    st.title("1. Log Mood")
    with st.form("log_form"):
        time_of_day = st.selectbox("Time", ["Morning", "Afternoon", "Night"])
        mood = st.slider("Mood (0=very low, 10=very high)", 0, 10, 5)
        energy = st.slider("Energy (0=exhausted, 10=energized)", 0, 10, 5)
        sleep = st.slider("Sleep Quality (0=terrible, 10=great)", 0, 10, 5)
        irritability = st.slider("Irritability (0=calm, 10=very irritable)", 0, 10, 0)
        confidence = st.slider("Confidence (0=none, 10=super high)", 0, 10, 5)
        impulsivity = st.slider("Impulsivity (0=very cautious, 10=very impulsive)", 0, 10, 5)
        notes = st.text_area("What happened today? How did it feel?")
        submit = st.form_submit_button("Submit")

    if submit:
        entry = {
            "Date": datetime.date.today(),
            "Time": time_of_day,
            "Mood": mood,
            "Energy": energy,
            "Sleep": sleep,
            "Irritability": irritability,
            "Confidence": confidence,
            "Impulsivity": impulsivity,
            "Notes": notes
        }
        st.session_state.log.append(entry)
        pd.DataFrame(st.session_state.log).to_csv(DATA_FILE, index=False)
        st.success("Mood logged.")

# ---------- 2. MOOD REPORT ----------
elif page == "Mood Report":
    st.title("2. Mood Report")
    if not st.session_state.log:
        st.info("No mood data yet.")
    else:
        df = pd.DataFrame(st.session_state.log)
        st.dataframe(df.tail(10))

        if st.button("Delete Last Entry"):
            st.session_state.log.pop()
            pd.DataFrame(st.session_state.log).to_csv(DATA_FILE, index=False)
            st.success("Last entry deleted.")

        st.line_chart(df.set_index("Date")[["Mood", "Energy", "Sleep"]].rolling(3).mean())

        fig, ax = plt.subplots()
        df[["Confidence", "Impulsivity", "Irritability"]].tail(7).plot(kind="bar", ax=ax)
        st.pyplot(fig)

# ---------- 3. LETTER TO SELF ----------
elif page == "Letter to Self":
    st.title("3. Letter to Self")
    with st.form("letter_form"):
        letter = st.text_area("Write a message to your future self.")
        if st.form_submit_button("Save Letter"):
            st.session_state.letters.append((datetime.datetime.now(), letter))
            st.success("Letter saved.")
    for t, txt in st.session_state.letters[::-1]:
        with st.expander(f"Letter from {t.strftime('%Y-%m-%d %H:%M')}"):
            st.write(txt)

# ---------- 4. REALITY ANCHORS ----------
elif page == "Reality Anchors":
    st.title("4. Reality Anchors")
    with st.form("anchor_form"):
        anchor = st.text_area("Write 2–3 self-check truths.")
        if st.form_submit_button("Save Anchors"):
            st.session_state.anchors.append((datetime.datetime.now(), anchor))
            st.success("Anchor saved.")
    for t, a in st.session_state.anchors[::-1]:
        st.markdown(f"**{t.date()}** – {a}")

# ---------- 5. MOOD SIMULATION ----------
elif page == "Mood Simulation":
    st.title("5. Mood Simulation – Jump Diffusion Model")
    if not st.session_state.log:
        st.warning("Log at least one mood entry.")
    else:
        last = st.session_state.log[-1]
        use_stoch_vol = st.checkbox("Enable Stochastic Volatility", value=True)

        # Parameters
        mu = 0.1
        sigma_base = 1 + (last["Impulsivity"] + last["Irritability"]) / 10
        lambda_jump = 0.1
        jump_mean = -5 if last["Mood"] < 4 else 3
        jump_std = 2
        T = 50
        M = last["Mood"] * 10
        vol = sigma_base
        mood_path = []
        vol_path = []

        for _ in range(T):
            mean_revert = mu * (60 - M)
            dW = np.random.normal()
            jumps = np.sum(np.random.normal(jump_mean, jump_std, np.random.poisson(lambda_jump)))
            if use_stoch_vol:
                vol = max(vol + 0.3 * (sigma_base - vol) + 0.2 * np.random.normal(), 0.1)
            M = np.clip(M + mean_revert + vol * dW + jumps, 0, 100)
            mood_path.append(M)
            vol_path.append(vol)

        st.line_chart(mood_path)
        if use_stoch_vol:
            st.line_chart(vol_path)

        st.latex(r'dM_t = \mu(M^* - M_t)dt + \sigma_t dW_t + J_t dN_t')
        if use_stoch_vol:
            st.latex(r'd\sigma_t = \kappa(\theta - \sigma_t)dt + \eta dZ_t')
