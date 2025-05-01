# app.py

import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt

# Set page configuration
st.set_page_config(page_title="Moodrift-HUG", layout="wide")

# Initialize session state
if "log" not in st.session_state:
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

# Crisis Mode & Bullying SOS
st.sidebar.markdown("## 🆘 Support Modes")
if st.sidebar.button("🆘 Crisis Mode" if lang == "English" else "🆘 Mode Krisis"):
    st.session_state.crisis_mode = True
    st.session_state.bully_mode = False
if st.sidebar.button("🚩 I'm being bullied" if lang == "English" else "🚩 Saya sedang dibully"):
    st.session_state.crisis_mode = False
    st.session_state.bully_mode = True
if st.sidebar.button("↩️ Exit Support Mode" if lang == "English" else "↩️ Keluar dari Mode Dukungan"):
    st.session_state.crisis_mode = False
    st.session_state.bully_mode = False

# Crisis Mode
if st.session_state.crisis_mode:
    st.title("🆘 Crisis Mode Activated" if lang == "English" else "🆘 Mode Krisis Aktif")
    st.markdown("You're not alone. Let's take this one small step at a time." if lang == "English" else "Kamu tidak sendiri. Mari kita ambil langkah kecil bersama-sama.")

    with st.expander("📦 Emergency Grounding Toolkit" if lang == "English" else "📦 Alat Darurat untuk Menenangkan Diri"):
        st.markdown("""
- Take a breath: Inhale for 4 seconds, hold for 4, exhale for 6.
- Name 3 things you see, 2 you hear, 1 you feel.
- Grab a glass of water or walk to a window.
        """ if lang == "English" else """
- Tarik napas: Tarik napas 4 detik, tahan 4 detik, hembuskan 6 detik.
- Sebutkan 3 hal yang kamu lihat, 2 yang kamu dengar, 1 yang kamu rasakan.
- Minum air putih atau lihat keluar jendela.
        """)

    with st.expander("💬 Talk to HUG" if lang == "English" else "💬 Bicara dengan HUG"):
        with st.form(key="crisis_chat"):
            user_input = st.text_area("What’s happening for you right now?" if lang == "English" else "Apa yang sedang kamu rasakan saat ini?")
            submitted = st.form_submit_button("Send" if lang == "English" else "Kirim")

        if submitted and user_input:
            st.markdown(f"🫂 You said: *{user_input}*" if lang == "English" else f"🫂 Kamu bilang: *{user_input}*")

            if any(word in user_input.lower() for word in ["hopeless", "give up", "suicidal", "kill", "end it"]):
                st.warning("💔 That sounds really heavy. Please consider calling a crisis line or reaching out to someone you trust. You don’t have to go through this alone." if lang == "English" else "💔 Itu terdengar sangat berat. Pertimbangkan untuk menghubungi layanan krisis atau seseorang yang kamu percaya. Kamu tidak harus menghadapinya sendiri.")
            elif any(word in user_input.lower() for word in ["anxious", "nervous", "panic"]):
                st.info("🫁 Try a grounding technique: 5 deep breaths, or list 3 things you can see, hear, and touch." if lang == "English" else "🫁 Coba teknik menenangkan: 5 kali napas dalam, atau sebutkan 3 hal yang kamu lihat, dengar, dan rasakan.")
            elif any(word in user_input.lower() for word in ["sad", "cry", "alone", "hurt"]):
                st.info("💙 It’s okay to feel what you’re feeling. You’re not alone, and this feeling won’t last forever." if lang == "English" else "💙 Tidak apa-apa merasakan apa yang kamu rasakan. Kamu tidak sendiri, dan perasaan ini tidak akan berlangsung selamanya.")
            else:
                st.success("✅ Thank you for sharing. Sometimes just expressing it helps a little." if lang == "English" else "✅ Terima kasih sudah berbagi. Terkadang hanya mengungkapkan saja sudah cukup membantu.")

    with st.expander("📞 Helpful Resources" if lang == "English" else "📞 Sumber Bantuan"):
        st.markdown("""
- **Befrienders Worldwide**: [https://www.befrienders.org](https://www.befrienders.org)  
- **Indonesia (Samaritans)**: Call 021-500-454  
- **UK (Samaritans)**: Call 116 123  
- **Text a friend** you trust and just say: "Hey, can we talk?"
        """ if lang == "English" else """
- **Befrienders Indonesia**: [https://www.befrienders.or.id](https://www.befrienders.or.id)  
- **Indonesia (Samaritans)**: Hubungi 021-500-454  
- **UK (Samaritans)**: Hubungi 116 123  
- **Kirim pesan ke teman** yang kamu percaya dan katakan: "Hai, boleh kita ngobrol?"
        """)

    st.stop()

# Bullying Support Mode
if st.session_state.bully_mode:
    st.title("💬 Bullying Support Bot" if lang == "English" else "💬 Bot Dukungan untuk Perundungan")
    st.markdown("That’s hard. Let’s talk it through – anonymously and safely." if lang == "English" else "Itu berat. Mari kita bicarakan secara anonim dan aman.")

    with st.form(key="bully_chat"):
        bullying_input = st.text_area("What’s been going on?" if lang == "English" else "Apa yang sedang terjadi padamu?")
        bully_submit = st.form_submit_button("Send" if lang == "English" else "Kirim")

    if bully_submit and bullying_input:
        st.markdown(f"🫂 You said: *{bullying_input}*" if lang == "English" else f"🫂 Kamu bilang: *{bullying_input}*")
        st.markdown("🫂 Thank you for sharing. No one deserves that. You're not overreacting." if lang == "English" else "🫂 Terima kasih sudah berbagi. Tidak ada yang pantas diperlakukan seperti itu. Kamu tidak berlebihan.")
        st.markdown("You might try keeping a small log of what happens and when, and talk to someone you trust. I'm here for more support anytime." if lang == "English" else "Kamu bisa mencoba mencatat kejadian dan waktunya, lalu bicara dengan orang yang kamu percaya. Aku di sini kalau kamu butuh dukungan.")

    st.stop()

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
        mu = 0.05 * (60 - (last_entry["Mood"] * 10)) / 100
        sigma_base = 1 + abs(last_entry["Irritability"] + last_entry["Impulsivity"]) * 0.5
        lambda_jump = 0.05
        jump_mean = -5 if last_entry["Mood"] < 0 else 2
        jump_std = 3
        use_stoch_vol = st.checkbox("Enable Stochastic Volatility", value=True)

        # Simulate jump diffusion
        T = 50
        dt = 1
        mood_path = []
        vol_path = []

        M = 60
        vol = sigma_base
        np.random.seed(42)

        for t in range(T):
            mean_rev = mu * (60 - M)
            dW = np.random.normal(0, 1)
            dN = np.random.poisson(lambda_jump)
            J = np.random.normal(jump_mean, jump_std) if dN > 0 else 0

            if use_stoch_vol:
                kappa = 1.0
                theta = sigma_base
                eta = 0.3
                dZ = np.random.normal()
                vol = max(vol + kappa * (theta - vol) + eta * dZ, 0.1)

            sigma_t = vol
            dM = mean_rev + sigma_t * dW + J
            M = np.clip(M + dM, 0, 100)

            mood_path.append(M)
            vol_path.append(sigma_t)

        st.markdown("#### Simulated Mood Trajectory")
        fig, ax = plt.subplots()
        ax.plot(range(T), mood_path, label="Mood", color='purple')
        ax.axhline(30, color='red', linestyle='--', label="Crisis Threshold")
        ax.set_xlabel("Time")
        ax.set_ylabel("Mood")
        ax.legend()
        st.pyplot(fig)

        if use_stoch_vol:
            st.markdown("#### Volatility Over Time")
            fig2, ax2 = plt.subplots()
            ax2.plot(range(T), vol_path, color="orange")
            ax2.set_xlabel("Time")
            ax2.set_ylabel("Volatility")
            st.pyplot(fig2)

        st.markdown("### Model Equations")
        st.latex(r'dM_t = \mu(M^* - M_t)dt + \sigma_t dW_t + J_t dN_t')
        if use_stoch_vol:
            st.latex(r'd\sigma_t = \kappa(\theta - \sigma_t)dt + \eta dZ_t')
          
