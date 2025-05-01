import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="Moodrift", layout="wide")

# Initialize session state
if "log" not in st.session_state:
    st.session_state.log = []

if "letters" not in st.session_state:
    st.session_state.letters = []

if "anchors" not in st.session_state:
    st.session_state.anchors = []

# Sidebar navigation
page = st.sidebar.radio("Moodrift Navigation", ["Log Mood", "Mood Report", "Letter to Self", "Reality Anchors", "Mood Simulation"])

# ---------- 1. LOG MOOD ----------
if page == "Log Mood":
    st.title("1. Log Mood")
    with st.form("log_form"):
        time_of_day = st.selectbox("Time of Day", ["Morning", "Afternoon", "Night"])
        mood = st.slider("Mood", -5, 5, 0)
        energy = st.slider("Energy", -5, 5, 0)
        sleep = st.slider("Sleep Quality", -5, 5, 0)
        irritability = st.slider("Irritability", -5, 5, 0)
        confidence = st.slider("Confidence", -5, 5, 0)
        impulsivity = st.slider("Impulsivity", -5, 5, 0)
        notes = st.text_area("What happened today? / How did it feel?")
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
        st.success("Mood logged successfully.")

# ---------- 2. MOOD REPORT ----------
elif page == "Mood Report":
    st.title("2. Mood Report")

    if not st.session_state.log:
        st.info("No data logged yet.")
    else:
        df = pd.DataFrame(st.session_state.log)
        st.dataframe(df)

        mood_range = df["Mood"].max() - df["Mood"].min()
        if mood_range >= 6:
            st.error("⚠️ Mood volatility detected today.")

        st.markdown("#### Mood Over Time")
        mood_series = df.groupby("Time")["Mood"].mean()
        st.line_chart(mood_series)

        st.markdown("#### Confidence / Impulsivity / Irritability")
        fig, ax = plt.subplots()
        df_plot = df[["Confidence", "Impulsivity", "Irritability"]].tail(7)
        df_plot.plot(kind="bar", ax=ax)
        st.pyplot(fig)

        # Flag high-risk mood patterns
        if df.tail(3)[["Confidence", "Impulsivity"]].mean().sum() > 6:
            st.warning("⚠️ Elevated confidence + impulsivity. Consider reviewing your Reality Anchors.")

# ---------- 3. LETTER TO SELF ----------
elif page == "Letter to Self":
    st.title("3. Letter to Self")
    with st.form("letter_form"):
        letter = st.text_area("Write a message to your future self:")
        send_it = st.form_submit_button("Save Letter")
    if send_it:
        st.session_state.letters.append((datetime.datetime.now(), letter))
        st.success("Letter saved.")

    st.markdown("#### Previously Saved Letters")
    for i, (t, txt) in enumerate(st.session_state.letters[::-1]):
        with st.expander(f"Letter from {t.strftime('%Y-%m-%d %H:%M:%S')}"):
            st.write(txt)

# ---------- 4. REALITY ANCHORS ----------
elif page == "Reality Anchors":
    st.title("4. Reality Anchors")
    with st.form("anchor_form"):
        anchors = st.text_area("Write 2–3 reality check truths (e.g., 'I usually sleep 7 hours').")
        anchor_submit = st.form_submit_button("Save Anchors")
    if anchor_submit:
        st.session_state.anchors.append((datetime.datetime.now(), anchors))
        st.success("Anchor saved.")

    if st.session_state.anchors:
        st.markdown("#### Your Anchors")
        for t, a in st.session_state.anchors[::-1]:
            st.markdown(f"**{t.date()}**: {a}")

# ---------- 5. MOOD SIMULATION (JUMP DIFFUSION) ----------
elif page == "Mood Simulation":
    st.title("5. Mood Simulation – Jump Diffusion Model")

    st.markdown("Uses your last mood state to simulate emotional trajectory.")

    if not st.session_state.log:
        st.info("No data available. Log mood first.")
    else:
        last_entry = st.session_state.log[-1]
        mu = last_entry["Mood"] * 0.02
        sigma = max(0.1, abs(last_entry["Irritability"] + last_entry["Impulsivity"]) * 0.05)
        lambda_jump = 0.3
        jump_mean = 0.8 * np.sign(last_entry["Mood"])
        jump_std = 0.4

        # Simulate
        T = 10
        dt = 0.01
        N = int(T / dt)
        time = np.linspace(0, T, N)
        mood_path = np.zeros(N)

        for t in range(1, N):
            dW = np.random.normal(0, np.sqrt(dt))
            dN = np.random.poisson(lambda_jump * dt)
            J = np.random.normal(jump_mean, jump_std) if dN > 0 else 0
            mood_path[t] = mood_path[t - 1] + mu * dt + sigma * dW + J

        st.markdown("#### Simulated Mood Trajectory (Next 10 Units of Time)")
        fig, ax = plt.subplots()
        ax.plot(time, mood_path, color='purple')
        ax.set_title("Jump Diffusion Mood Simulation")
        ax.set_xlabel("Time")
        ax.set_ylabel("Mood Level")
        st.pyplot(fig)
