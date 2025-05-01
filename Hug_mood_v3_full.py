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
