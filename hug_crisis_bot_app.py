import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="HUG – Personalized Mood Simulator", layout="centered")

# --- Session state to persist crisis/bullying view ---
if "crisis_mode" not in st.session_state:
    st.session_state.crisis_mode = False
if "bully_mode" not in st.session_state:
    st.session_state.bully_mode = False

# --- Language toggle ---
lang = st.radio("\U0001F310 Language / Bahasa", ["English", "Bahasa Indonesia"])

# --- Crisis Mode & Bullying SOS ---
col1, col2, col3 = st.columns([1, 1, 2])
with col1:
    if st.button("🆘 Crisis Mode" if lang == "English" else "🆘 Mode Krisis"):
        st.session_state.crisis_mode = True
        st.session_state.bully_mode = False
with col2:
    if st.button("🚩 I'm being bullied" if lang == "English" else "🚩 Saya sedang dibully"):
        st.session_state.crisis_mode = False
        st.session_state.bully_mode = True
with col3:
    if st.button("↩️ Exit Support Mode" if lang == "English" else "↩️ Keluar dari Mode Dukungan"):
        st.session_state.crisis_mode = False
        st.session_state.bully_mode = False

if st.session_state.crisis_mode:
    st.markdown("## 🆘 Crisis Mode Activated" if lang == "English" else "## 🆘 Mode Krisis Aktif")
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

if st.session_state.bully_mode:
    st.markdown("## 💬 Bullying Support Bot" if lang == "English" else "## 💬 Bot Dukungan untuk Perundungan")
    st.markdown("That’s hard. Let’s talk it through – anonymously and safely." if lang == "English" else "Itu berat. Mari kita bicarakan secara anonim dan aman.")

    with st.form(key="bully_chat"):
        bullying_input = st.text_area("What’s been going on?" if lang == "English" else "Apa yang sedang terjadi padamu?")
        bully_submit = st.form_submit_button("Send" if lang == "English" else "Kirim")

    if bully_submit and bullying_input:
        st.markdown(f"🫂 You said: *{bullying_input}*" if lang == "English" else f"🫂 Kamu bilang: *{bullying_input}*")
        st.markdown("🫂 Thank you for sharing. No one deserves that. You're not overreacting." if lang == "English" else "🫂 Terima kasih sudah berbagi. Tidak ada yang pantas diperlakukan seperti itu. Kamu tidak berlebihan.")
        st.markdown("You might try keeping a small log of what happens and when, and talk to someone you trust. I'm here for more support anytime." if lang == "English" else "Kamu bisa mencoba mencatat kejadian dan waktunya, lalu bicara dengan orang yang kamu percaya. Aku di sini kalau kamu butuh dukungan.")

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

# --- Mood Simulator Section ---
use_stoch_vol = st.checkbox("Use stochastic volatility?" if lang == "English" else "Gunakan volatilitas stokastik?", value=False)

# Parameters
mu = recovery_input / 10
sigma_base = 1 + (instability_input * 0.9)
mu_J = -3 * impact_input
sigma_J = 5
stress_modifier = {"No": 0.0, "Maybe": 0.05, "Yes": 0.1}[bullying_status]
lambda_jump = 0.01 + (jumpiness_input / 100) + stress_modifier

T = 50
collapse_threshold = 30
baseline = 60

if st.button(LABELS["simulate_btn"]):
    mood = [mood0]
    vol = sigma_base
    sigma_path = [vol]
    np.random.seed(42)

    for _ in range(T):
        current_mood = mood[-1]
        mean_reversion = mu * (baseline - current_mood)

        if use_stoch_vol:
            # Heston-like volatility update
            kappa = 1.5
            theta = sigma_base
            eta = 0.3
            dZ = np.random.normal()
            vol = max(vol + kappa * (theta - vol) + eta * dZ, 0.1)
            sigma_t = vol
            sigma_path.append(vol)
        else:
            sigma_t = sigma_base * (1 + (1 - current_mood / 100))

        dW = np.random.normal()
        num_jumps = np.random.poisson(lambda_jump)
        jumps = np.random.normal(loc=mu_J, scale=sigma_J, size=num_jumps).sum() if num_jumps > 0 else 0

        dM = mean_reversion + sigma_t * dW + jumps
        next_mood = np.clip(current_mood + dM, 0, 100)
        mood.append(next_mood)

    # Plotting
    fig, ax = plt.subplots(figsize=(10, 4))
    ax.plot(mood, label="Mood", color="blue")
    ax.axhline(collapse_threshold, color='red', linestyle='--', label="Tipping Point")
    ax.set_xlabel("Time")
    ax.set_ylabel("Mood Level")
    ax.legend()
    st.pyplot(fig)

    # Feedback
    if any(m < collapse_threshold for m in mood):
        st.error(LABELS["feedback_risk"])
    else:
        st.success(LABELS["feedback_ok"])

    # LaTeX model
    st.markdown("### 📐 Model Explanation" if lang == "English" else "### 📐 Penjelasan Model")
    st.latex(r'dM_t = \mu (M^* - M_t)\,dt + \sigma_t\,dW_t + J_t\,dN_t')

    with st.expander("📊 Parameter Descriptions" if lang == "English" else "📊 Deskripsi Parameter"):
        st.markdown(r"""
- \( M_t \): Current mood
- \( M^* \): Baseline mood (e.g. 60)
- \( \mu \): Recovery speed
- \( \sigma_t \): Emotional volatility, either adaptive or stochastic
- \( dW_t \): Random mood shifts (Brownian motion)
- \( J_t \): Mood shocks (trauma, conflict)
- \( dN_t \): Random occurrence of shocks (Poisson process)
        """ if lang == "English" else r"""
- \( M_t \): Mood saat ini
- \( M^* \): Mood ideal (misal: 60)
- \( \mu \): Kecepatan pemulihan
- \( \sigma_t \): Volatilitas emosi, adaptif atau stokastik
- \( dW_t \): Perubahan mood acak (proses Brown)
- \( J_t \): Guncangan emosi (trauma, konflik)
- \( dN_t \): Kejadian acak dari guncangan (proses Poisson)
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

