import streamlit as st
import numpy as np
import pandas as pd
import joblib
import random
import time
from datetime import datetime
import plotly.graph_objects as go
from google import genai

# =========================================================
# PAGE CONFIG
# =========================================================
st.set_page_config(
    page_title="HeartAI | Cardiac Risk Assistant",
    page_icon="🫀",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================
# PROFESSIONAL UI — REDESIGNED COLOR SYSTEM
# =========================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&family=Manrope:wght@700;800&display=swap');

:root{
    /* Core neutrals */
    --navy:#070C16;
    --navy2:#0E1B2E;
    --navy3:#142842;
    --card:#FFFFFF;
    --soft:#F3F7FC;
    --line:#E2E9F2;
    --text:#101827;
    --muted:#64748B;

    /* Brand gradient palette */
    --teal:#0EA893;
    --teal-dark:#087F73;
    --teal-soft:#E4F9F5;
    --violet:#7C5CFC;
    --violet-soft:#F1EDFF;
    --coral:#FF6B6B;
    --coral-soft:#FFEDED;
    --blue:#3B82F6;
    --blue-soft:#EAF2FF;
    --gold:#F0B429;
    --gold-soft:#FFF6DF;

    /* Status colors */
    --green:#0F9D58;
    --green-soft:#E7FBF0;
    --amber:#D97706;
    --amber-soft:#FFF4E0;
    --red:#E53E3E;
    --red-soft:#FFECEC;
}

html, body, [class*="css"]{
    font-family: 'Inter', Arial, sans-serif;
}
.stApp{
    background:
        radial-gradient(circle at 10% 0%, rgba(124,92,252,.05), transparent 40%),
        radial-gradient(circle at 90% 10%, rgba(14,168,147,.06), transparent 45%),
        #F3F7FC;
    color:var(--text);
}
.block-container{
    max-width:1500px;
    padding:1.4rem 2.2rem 3rem;
}

/* ---------------- Sidebar ---------------- */
[data-testid="stSidebar"]{
    background:linear-gradient(180deg,#070C16 0%, #0E1B2E 55%, #0B1830 100%) !important;
    border-right:1px solid #1D2A40;
}
[data-testid="stSidebar"] *{
    color:#E7EEF8;
}
[data-testid="stSidebar"] .stRadio label{
    border-radius:10px;
    padding:8px 10px;
    transition:background .15s ease;
}
[data-testid="stSidebar"] .stRadio label:hover{
    background:linear-gradient(90deg, rgba(14,168,147,.18), rgba(124,92,252,.10));
}
.sidebar-brand{
    text-align:center;
    padding:16px 4px 20px;
    border-bottom:1px solid #24324A;
    margin-bottom:22px;
}
.brand-heart{
    font-size:44px;
    line-height:1;
    filter:drop-shadow(0 0 14px rgba(14,168,147,.55));
}
.brand-name{
    background:linear-gradient(90deg,#5CE6D0,#9C8CFF);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
    font-size:23px;
    font-weight:900;
    margin-top:9px;
    letter-spacing:.3px;
}
.brand-sub{
    color:#8CA0BC;
    font-size:11px;
    letter-spacing:1.6px;
    margin-top:4px;
    text-transform:uppercase;
}
.side-title{
    color:#7F93AE;
    font-size:10px;
    font-weight:800;
    letter-spacing:1.4px;
    text-transform:uppercase;
    margin:12px 0 8px;
}
.status-box{
    background:linear-gradient(160deg,#111C2F, #0D1729);
    border:1px solid #24324A;
    border-radius:14px;
    padding:13px 14px;
    margin-top:10px;
}
.status-row{
    display:flex;
    justify-content:space-between;
    align-items:center;
    padding:7px 0;
    font-size:12px;
}
.dot{
    width:8px;
    height:8px;
    display:inline-block;
    border-radius:50%;
    margin-right:6px;
    box-shadow:0 0 8px currentColor;
}
.side-footer{
    color:#7F93AE;
    text-align:center;
    font-size:11px;
    line-height:1.6;
    margin-top:30px;
}

/* ---------------- General controls ---------------- */
.stButton > button{
    background:linear-gradient(135deg, var(--teal) 0%, var(--teal-dark) 100%) !important;
    color:white !important;
    border:0 !important;
    border-radius:12px !important;
    font-weight:700 !important;
    min-height:46px;
    box-shadow:0 8px 20px rgba(8,127,115,.28);
    transition:transform .15s ease, box-shadow .15s ease;
}
.stButton > button:hover{
    transform:translateY(-2px);
    box-shadow:0 12px 26px rgba(8,127,115,.36);
}
.stTextInput input,
.stTextArea textarea{
    background:#FFFFFF !important;
    color:var(--text) !important;
    border:1px solid var(--line) !important;
    border-radius:10px !important;
}
.stSelectbox [data-baseweb="select"] > div{
    background:#FFFFFF !important;
    color:var(--text) !important;
    border-color:var(--line) !important;
    border-radius:10px !important;
}
.stSlider [data-baseweb="slider"]{
    padding-top:5px;
}
.stSlider [data-testid="stThumbValue"]{
    color:var(--teal-dark) !important;
    font-weight:700 !important;
}
div[data-baseweb="slider"] > div > div > div{
    background:linear-gradient(90deg, var(--teal), var(--violet)) !important;
}
h1,h2,h3,h4{
    color:var(--text) !important;
}
.stCaption, small{
    color:var(--muted) !important;
}
hr{
    border-color:var(--line) !important;
}
[data-testid="stProgress"] > div > div{
    background:linear-gradient(90deg, var(--teal), var(--violet)) !important;
}

/* ---------------- Hero ---------------- */
.hero{
    background:linear-gradient(120deg,#070C16 0%, #0E2038 45%, #0A3D38 100%);
    border-radius:24px;
    padding:38px 40px;
    color:white;
    box-shadow:0 18px 45px rgba(7,12,22,.22);
    margin-bottom:24px;
    position:relative;
    overflow:hidden;
}
.hero:after{
    content:"";
    position:absolute;
    width:360px;
    height:360px;
    right:-120px;
    top:-160px;
    border-radius:50%;
    background:radial-gradient(circle, rgba(124,92,252,.28), transparent 70%);
}
.hero:before{
    content:"";
    position:absolute;
    width:260px;
    height:260px;
    left:-90px;
    bottom:-140px;
    border-radius:50%;
    background:radial-gradient(circle, rgba(14,168,147,.30), transparent 70%);
}
.hero-badge{
    display:inline-block;
    background:rgba(255,255,255,.10);
    border:1px solid rgba(255,255,255,.18);
    color:#B9F2E8;
    border-radius:999px;
    padding:8px 14px;
    font-size:11px;
    font-weight:800;
    letter-spacing:1.2px;
    text-transform:uppercase;
    position:relative;
}
.hero h1{
    color:white !important;
    font-family:'Manrope', 'Inter', sans-serif;
    font-size:clamp(30px,4vw,50px);
    line-height:1.08;
    margin:18px 0 10px;
    font-weight:800;
    position:relative;
}
.hero h1 span{
    background:linear-gradient(90deg,#5CE6D0,#9C8CFF 70%);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
}
.hero p{
    color:#CBD9EA;
    max-width:760px;
    font-size:15.5px;
    line-height:1.7;
    margin:0;
    position:relative;
}
.hero-pills{
    margin-top:24px;
    display:flex;
    flex-wrap:wrap;
    gap:9px;
    position:relative;
}
.pill{
    padding:8px 13px;
    border-radius:999px;
    background:rgba(255,255,255,.08);
    border:1px solid rgba(255,255,255,.16);
    color:#EAF4FF;
    font-size:11.5px;
    font-weight:700;
    backdrop-filter:blur(6px);
}

/* ---------------- Cards ---------------- */
.card{
    background:var(--card);
    border:1px solid var(--line);
    border-radius:18px;
    padding:24px;
    box-shadow:0 6px 20px rgba(15,23,42,.05);
    margin-bottom:18px;
    border-top:3px solid transparent;
    background-image:linear-gradient(#FFFFFF,#FFFFFF), linear-gradient(90deg, var(--teal), var(--violet));
    background-origin:border-box;
    background-clip:padding-box, border-box;
}
.card-title{
    color:var(--text);
    font-size:17.5px;
    font-weight:800;
    margin-bottom:4px;
}
.card-sub{
    color:var(--muted);
    font-size:13px;
    line-height:1.6;
}

.metric-card{
    background:linear-gradient(160deg,#FFFFFF, #F8FBFF);
    border:1px solid var(--line);
    border-radius:16px;
    padding:18px;
    min-height:106px;
    box-shadow:0 4px 16px rgba(15,23,42,.04);
    transition:transform .15s ease, box-shadow .15s ease;
}
.metric-card:hover{
    transform:translateY(-3px);
    box-shadow:0 10px 24px rgba(15,23,42,.09);
}
.metric-label{
    color:var(--muted);
    font-size:11px;
    font-weight:800;
    letter-spacing:.7px;
    text-transform:uppercase;
}
.metric-value{
    font-size:25px;
    font-weight:800;
    margin-top:8px;
    background:linear-gradient(90deg, var(--navy), var(--teal-dark));
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
}
.metric-note{
    color:var(--muted);
    font-size:11px;
    margin-top:4px;
}
.tag{
    display:inline-block;
    border-radius:8px;
    padding:5px 10px;
    font-size:10px;
    font-weight:800;
    text-transform:uppercase;
    letter-spacing:.5px;
}
.normal{background:var(--green-soft);color:var(--green);}
.warn{background:var(--amber-soft);color:var(--amber);}
.danger{background:var(--red-soft);color:var(--red);}

/* ---------------- Chat ---------------- */
.chat-header{
    background:linear-gradient(120deg,#070C16, #142842 60%, #0A3D38);
    border-radius:18px 18px 0 0;
    padding:22px 24px;
    color:white;
    border:1px solid #1F3048;
    position:relative;
    overflow:hidden;
}
.chat-header:after{
    content:"";
    position:absolute;
    width:220px;height:220px;
    right:-80px;top:-100px;
    border-radius:50%;
    background:radial-gradient(circle, rgba(124,92,252,.25), transparent 70%);
}
.chat-header-title{
    font-size:20px;
    font-weight:800;
    position:relative;
}
.chat-header-sub{
    color:#B7C6DA;
    font-size:12.5px;
    margin-top:5px;
    position:relative;
}
[data-testid="stChatMessage"]{
    border-radius:16px !important;
    border:1px solid var(--line) !important;
    background:#FFFFFF !important;
    color:var(--text) !important;
    box-shadow:0 3px 12px rgba(15,23,42,.035);
}
[data-testid="stChatMessage"] p{
    color:var(--text) !important;
    line-height:1.65;
}
[data-testid="stChatInput"]{
    border-color:var(--line) !important;
    border-radius:0 0 18px 18px !important;
}

/* ---------------- Footer ---------------- */
.footer{
    background:linear-gradient(120deg,#070C16, #0E1B2E 60%, #0A3D38);
    color:#AFC0D4;
    border-radius:18px;
    padding:26px;
    text-align:center;
    margin-top:32px;
}
.footer strong{
    background:linear-gradient(90deg,#5CE6D0,#9C8CFF);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;
    background-clip:text;
}
.disclaimer{
    background:linear-gradient(160deg,#F8FAFC,#F1F6FC);
    border:1px solid var(--line);
    border-left:4px solid var(--gold);
    border-radius:12px;
    padding:13px 15px;
    color:#5B6B80;
    font-size:11.5px;
    line-height:1.6;
}

/* ---------------- Project Team ---------------- */
.team-hero{
    background:linear-gradient(120deg,#070C16 0%, #142842 55%, #0A3D38 100%);
    border-radius:22px;
    padding:30px 34px;
    color:white;
    box-shadow:0 14px 34px rgba(7,12,22,.18);
    margin-bottom:22px;
    position:relative;
    overflow:hidden;
}
.team-hero:after{
    content:"";
    position:absolute;
    width:260px;height:260px;
    right:-90px;top:-120px;
    border-radius:50%;
    background:radial-gradient(circle, rgba(124,92,252,.25), transparent 70%);
}
.team-hero-title{
    font-family:'Manrope','Inter',sans-serif;
    font-size:26px;
    font-weight:800;
    position:relative;
}
.team-hero-sub{
    color:#CBD9EA;
    font-size:13.5px;
    margin-top:6px;
    max-width:640px;
    line-height:1.6;
    position:relative;
}
.univ-badge{
    display:inline-flex;
    align-items:center;
    gap:8px;
    background:rgba(255,255,255,.09);
    border:1px solid rgba(255,255,255,.16);
    color:#EAF4FF;
    border-radius:999px;
    padding:8px 14px;
    font-size:12px;
    font-weight:700;
    margin-top:16px;
    position:relative;
}
.team-card{
    background:linear-gradient(160deg,#FFFFFF,#F8FBFF);
    border:1px solid var(--line);
    border-radius:18px;
    padding:26px 22px;
    text-align:center;
    box-shadow:0 6px 20px rgba(15,23,42,.05);
    transition:transform .15s ease, box-shadow .15s ease;
    height:100%;
}
.team-card:hover{
    transform:translateY(-4px);
    box-shadow:0 14px 30px rgba(15,23,42,.10);
}
.team-avatar{
    width:74px;
    height:74px;
    margin:0 auto 14px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:26px;
    font-weight:800;
    color:white;
    background:linear-gradient(135deg, var(--teal), var(--violet));
    box-shadow:0 8px 18px rgba(124,92,252,.25);
}
.team-name{
    font-size:17px;
    font-weight:800;
    color:var(--text);
}
.team-roll{
    display:inline-block;
    margin-top:6px;
    background:var(--teal-soft);
    color:var(--teal-dark);
    border-radius:999px;
    padding:4px 12px;
    font-size:11.5px;
    font-weight:700;
    letter-spacing:.3px;
}
.team-role{
    color:var(--muted);
    font-size:12px;
    margin-top:10px;
}
.guide-card{
    background:linear-gradient(120deg,#0E1B2E,#142842 60%,#0A3D38);
    border-radius:18px;
    padding:26px 24px;
    color:white;
    display:flex;
    align-items:center;
    gap:18px;
    box-shadow:0 10px 26px rgba(7,12,22,.18);
    margin-top:6px;
}
.guide-avatar{
    width:64px;
    height:64px;
    min-width:64px;
    border-radius:50%;
    display:flex;
    align-items:center;
    justify-content:center;
    font-size:24px;
    font-weight:800;
    background:linear-gradient(135deg,#5CE6D0,#9C8CFF);
    color:#0B1220;
}
.guide-label{
    color:#9FB0C7;
    font-size:11px;
    letter-spacing:1.2px;
    text-transform:uppercase;
    font-weight:800;
}
.guide-name{
    font-size:19px;
    font-weight:800;
    margin-top:4px;
}
.guide-role{
    color:#CBD9EA;
    font-size:12.5px;
    margin-top:3px;
}

/* ---------------- Responsive ---------------- */
@media(max-width:900px){
    .block-container{padding:1rem 1rem 2rem;}
    .hero{padding:28px 22px;}
}
</style>
""", unsafe_allow_html=True)

# =========================================================
# API / MODEL HELPERS
# =========================================================
if "GEMINI_API_KEY" not in st.secrets:
    st.error("Gemini API key is not configured.")
    st.info("Add GEMINI_API_KEY to .streamlit/secrets.toml and restart Streamlit.")
    st.stop()

@st.cache_resource
def load_models():
    try:
        model = joblib.load("models/best_model.pkl")
        scaler = joblib.load("models/scaler.pkl")
        return model, scaler, None
    except Exception as exc:
        return None, None, str(exc)

model, scaler, model_error = load_models()

@st.cache_resource
def get_gemini_client():
    return genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

# =========================================================
# SIDEBAR
# =========================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-brand">
        <div class="brand-heart">🫀</div>
        <div class="brand-name">HeartAI</div>
        <div class="brand-sub">Cardiac Intelligence</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="side-title">Workspace</div>', unsafe_allow_html=True)
    page = st.radio(
        "Navigation",
        ["🏠 Dashboard", "🔍 Prediction", "📊 Analytics", "💬 AI Assistant", "👥 Project Team"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="side-title">System status</div>', unsafe_allow_html=True)
    model_status = "Online" if model is not None else "Demo mode"
    model_color = "#35D399" if model is not None else "#F0B429"

    st.markdown(f"""
    <div class="status-box">
        <div class="status-row">
            <span>🤖 ML Model</span>
            <span><i class="dot" style="background:{model_color};color:{model_color}"></i>{model_status}</span>
        </div>
        <div class="status-row">
            <span>☁️ Gemini</span>
            <span><i class="dot" style="background:#35D399;color:#35D399"></i>Ready</span>
        </div>
        <div class="status-row">
            <span>📊 Analytics</span>
            <span><i class="dot" style="background:#7C5CFC;color:#7C5CFC"></i>Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="side-footer">
        HeartAI is an academic project.<br>
        AI output is informational, not a diagnosis.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# HERO
# =========================================================
st.markdown("""
<div class="hero">
    <div class="hero-badge">AI-Assisted Cardiac Risk Screening</div>
    <h1>Understand your heart health<br><span>with clarity.</span></h1>
    <p>
        HeartAI combines a machine-learning prediction model, visual analytics,
        and a Gemini-powered health assistant in one clean dashboard.
    </p>
    <div class="hero-pills">
        <span class="pill">⚡ Fast analysis</span>
        <span class="pill">🧠 Machine learning</span>
        <span class="pill">📈 Visual analytics</span>
        <span class="pill">💬 AI assistant</span>
        <span class="pill">🔒 API key protected</span>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# DASHBOARD METRICS
# =========================================================
m1, m2, m3, m4 = st.columns(4)
dashboard_metrics = [
    ("🫀 Heart rate", f"{random.randint(68, 88)} BPM", "Sample dashboard value"),
    ("🩸 SpO₂", f"{random.randint(96, 99)}%", "Sample dashboard value"),
    ("🚶 Activity", f"{random.randint(4, 10)}k", "Steps • sample value"),
    ("😴 Sleep", f"{random.uniform(6.5, 8.5):.1f} h", "Sample dashboard value"),
]
for col, (label, value, note) in zip((m1, m2, m3, m4), dashboard_metrics):
    with col:
        st.markdown(
            f'<div class="metric-card"><div class="metric-label">{label}</div>'
            f'<div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>',
            unsafe_allow_html=True,
        )

st.write("")

# =========================================================
# PREDICTION
# =========================================================
if page in ["🏠 Dashboard", "🔍 Prediction"]:
    st.markdown("""
    <div class="card">
        <div class="card-title">🔍 Cardiac Risk Prediction</div>
        <div class="card-sub">
            Enter the five parameters used by the current project model.
            The result is a screening output and should not be treated as a medical diagnosis.
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)

    with c1:
        age = st.slider("Age (years)", 1, 120, 45)
        blood_pre = st.slider("Blood pressure (mmHg)", 50, 250, 120)

        bp_label = "Normal" if blood_pre < 120 else "Elevated" if blood_pre < 130 else "High"
        bp_class = "normal" if blood_pre < 120 else "warn" if blood_pre < 130 else "danger"
        st.markdown(f'<span class="tag {bp_class}">{bp_label}</span>', unsafe_allow_html=True)

    with c2:
        cholesterol = st.slider("Cholesterol (mg/dL)", 50, 500, 200)
        bmi = st.slider("BMI (kg/m²)", 10, 60, 25)

        chol_class = "normal" if cholesterol < 200 else "warn" if cholesterol < 240 else "danger"
        chol_label = "Desirable" if cholesterol < 200 else "Borderline" if cholesterol < 240 else "High"
        st.markdown(f'<span class="tag {chol_class}">{chol_label}</span>', unsafe_allow_html=True)

    with c3:
        glucose_level = st.slider("Fasting glucose (mg/dL)", 20, 400, 100)
        sex = st.selectbox("Sex", ["Male", "Female"])
        smoker = st.selectbox("Smoking status", ["No", "Yes", "Former"])

        gluc_class = "normal" if glucose_level < 100 else "warn" if glucose_level < 126 else "danger"
        gluc_label = "Normal" if glucose_level < 100 else "Elevated" if glucose_level < 126 else "High"
        st.markdown(f'<span class="tag {gluc_class}">{gluc_label}</span>', unsafe_allow_html=True)

    # Keep the same five model inputs used by the uploaded project.
    input_data = np.array([[age, blood_pre, cholesterol, bmi, glucose_level]], dtype=float)

    risk_factors = 0
    if blood_pre >= 130:
        risk_factors += 1
    if cholesterol >= 200:
        risk_factors += 1
    if bmi >= 25:
        risk_factors += 1
    if glucose_level >= 100:
        risk_factors += 1
    if smoker == "Yes":
        risk_factors += 2
    if age > 60:
        risk_factors += 1

    preliminary_score = max(30, min(100, 100 - risk_factors * 10))

    st.markdown(f"""
    <div class="card">
        <div class="card-title">🧠 Preliminary Health Score</div>
        <div class="card-sub">A simple visual indicator based on the entered values. It is separate from the ML model probability.</div>
    </div>
    """, unsafe_allow_html=True)

    pc1, pc2 = st.columns([5, 1])
    with pc1:
        st.progress(preliminary_score / 100)
    with pc2:
        score_class = "normal" if preliminary_score >= 70 else "warn" if preliminary_score >= 50 else "danger"
        st.markdown(
            f'<div style="text-align:right;font-size:24px;font-weight:800;color:'
            f'{"#0F9D58" if score_class=="normal" else "#D97706" if score_class=="warn" else "#E53E3E"}">'
            f'{preliminary_score}%</div>',
            unsafe_allow_html=True,
        )

    if st.button("🔍 Run Cardiac Risk Analysis", type="primary", use_container_width=True):
        with st.spinner("Analyzing the entered parameters..."):
            time.sleep(0.6)

            if model is not None and scaler is not None:
                try:
                    input_scaled = scaler.transform(input_data)
                    prediction = int(model.predict(input_scaled)[0])

                    if hasattr(model, "predict_proba"):
                        probability = model.predict_proba(input_scaled)
                        risk_score = float(probability[0][1])
                    else:
                        risk_score = float(prediction)
                except Exception as exc:
                    st.error(f"Model prediction failed: {exc}")
                    st.stop()
            else:
                risk_score = min(0.95, max(0.05, (risk_factors / 7)))
                prediction = int(risk_score >= 0.5)

        result_high = prediction == 1
        result_color = "#E53E3E" if result_high else "#0F9D58"
        result_bg = "linear-gradient(135deg,#FFECEC,#FFF5F5)" if result_high else "linear-gradient(135deg,#E7FBF0,#F3FFF8)"
        result_icon = "⚠️" if result_high else "✅"
        result_title = "Higher predicted cardiac risk" if result_high else "Lower predicted cardiac risk"

        st.markdown(f"""
        <div style="background:{result_bg};border:1px solid {result_color}33;border-radius:18px;padding:24px;margin-top:18px;box-shadow:0 8px 24px rgba(15,23,42,.06);">
            <div style="font-size:12px;font-weight:800;letter-spacing:.8px;color:{result_color};text-transform:uppercase;">Screening result</div>
            <div style="font-size:28px;font-weight:800;color:{result_color};margin-top:7px;">{result_icon} {result_title}</div>
            <div style="color:#64748B;font-size:13px;margin-top:6px;">
                Model output probability: <strong>{risk_score*100:.1f}%</strong>
                {" • Demo fallback is active" if model is None else ""}
            </div>
        </div>
        """, unsafe_allow_html=True)

        g1, g2 = st.columns(2)

        with g1:
            gauge = go.Figure(go.Indicator(
                mode="gauge+number",
                value=risk_score * 100,
                title={"text": "Model risk probability", "font": {"size": 15, "color": "#475569"}},
                number={"suffix": "%", "font": {"size": 34, "color": "#101827"}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#94A3B8"},
                    "bar": {"color": result_color, "thickness": 0.28},
                    "bgcolor": "#FFFFFF",
                    "borderwidth": 1,
                    "bordercolor": "#E2E9F2",
                    "steps": [
                        {"range": [0, 33], "color": "#E7FBF0"},
                        {"range": [33, 66], "color": "#FFF4E0"},
                        {"range": [66, 100], "color": "#FFECEC"},
                    ],
                },
            ))
            gauge.update_layout(
                paper_bgcolor="#FFFFFF",
                plot_bgcolor="#FFFFFF",
                height=300,
                margin=dict(l=20, r=20, t=55, b=10),
            )
            st.plotly_chart(gauge, width="stretch", config={"displayModeBar": False})

        with g2:
            factors = ["Blood pressure", "Cholesterol", "BMI", "Glucose", "Age"]
            values = [
                min(100, blood_pre / 180 * 100),
                min(100, cholesterol / 300 * 100),
                min(100, bmi / 40 * 100),
                min(100, glucose_level / 200 * 100),
                min(100, age / 80 * 100),
            ]
            radar = go.Figure()
            radar.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=factors + [factors[0]],
                fill="toself",
                fillcolor="rgba(124,92,252,.16)",
                line=dict(color="#7C5CFC", width=2),
                marker=dict(size=6, color="#0EA893"),
                name="Entered values",
            ))
            radar.update_layout(
                polar=dict(
                    bgcolor="#FFFFFF",
                    radialaxis=dict(range=[0, 100], gridcolor="#E2E8F0", color="#64748B"),
                    angularaxis=dict(gridcolor="#E2E8F0", color="#475569"),
                ),
                paper_bgcolor="#FFFFFF",
                font=dict(color="#475569"),
                height=300,
                margin=dict(l=40, r=40, t=35, b=10),
                showlegend=False,
            )
            st.plotly_chart(radar, width="stretch", config={"displayModeBar": False})

        st.markdown("""
        <div class="disclaimer">
            <strong>Important:</strong> This prediction is an academic ML screening output.
            It does not diagnose heart disease and should not be used to start, stop, or change medication.
            If you have concerning symptoms, seek appropriate medical care.
        </div>
        """, unsafe_allow_html=True)

# =========================================================
# ANALYTICS
# =========================================================
if page in ["🏠 Dashboard", "📊 Analytics"]:
    st.write("")
    st.markdown("""
    <div class="card">
        <div class="card-title">📊 Health Analytics</div>
        <div class="card-sub">Interactive sample trends for demonstrating the dashboard interface.</div>
    </div>
    """, unsafe_allow_html=True)

    days = pd.date_range(end=datetime.now(), periods=30)
    rng = np.random.default_rng(42)
    trend = pd.DataFrame({
        "Date": days,
        "Heart Rate": rng.integers(68, 92, 30),
        "Systolic BP": rng.integers(112, 142, 30),
        "Glucose": rng.integers(85, 128, 30),
    })

    fig = go.Figure()
    for name, color in [
        ("Heart Rate", "#E53E3E"),
        ("Systolic BP", "#3B82F6"),
        ("Glucose", "#F0B429"),
    ]:
        fig.add_trace(go.Scatter(
            x=trend["Date"],
            y=trend[name],
            name=name,
            mode="lines+markers",
            line=dict(color=color, width=2.5, shape="spline"),
            marker=dict(size=5),
        ))
    fig.update_layout(
        title="30-Day Sample Health Trends",
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#475569"),
        height=360,
        hovermode="x unified",
        legend=dict(orientation="h", y=1.12),
        xaxis=dict(gridcolor="#E2E8F0"),
        yaxis=dict(gridcolor="#E2E8F0"),
        margin=dict(l=20, r=20, t=65, b=20),
    )
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})

    a1, a2 = st.columns(2)
    with a1:
        water = st.slider("💧 Water intake (glasses)", 0, 16, 8)
        st.progress(min(water / 12, 1.0))
        st.caption(f"{water} glasses logged today")

    with a2:
        duration = st.slider("🏃 Exercise duration (minutes)", 0, 120, 30)
        st.progress(min(duration / 60, 1.0))
        st.caption(f"{duration} minutes logged today")

# =========================================================
# AI ASSISTANT
# =========================================================
if page in ["🏠 Dashboard", "💬 AI Assistant"]:
    st.write("")
    st.markdown("""
    <div class="chat-header">
        <div class="chat-header-title">💬 HeartAI Health Assistant</div>
        <div class="chat-header-sub">Ask about heart health, nutrition, exercise, symptoms, or your prediction result.</div>
    </div>
    """, unsafe_allow_html=True)

    emergency_keywords = [
        "heart attack", "cardiac arrest", "severe chest pain",
        "chest pain right now", "chest pain now", "can't breathe",
        "cannot breathe", "difficulty breathing", "severe shortness of breath",
        "fainting and chest pain",
    ]

    def get_gemini_response(question):
        q = question.lower().strip()

        if not q:
            return "Please type a question about heart health or related topics."

        if any(k in q for k in emergency_keywords):
            return (
                "⚠️ **This may be a medical emergency.** If you are currently "
                "experiencing severe or new chest pain, severe breathing difficulty, "
                "fainting, or symptoms that could indicate a heart attack or cardiac "
                "emergency, seek emergency medical care immediately. HeartAI cannot "
                "diagnose or treat emergencies."
            )

        prompt = f"""
You are HeartAI, a helpful AI health assistant inside a student heart-disease
prediction project.

Answer clearly and naturally. Focus on heart/cardiovascular health, nutrition,
exercise, lifestyle, risk factors, symptoms, and interpretation of this project's
screening output.

Safety rules:
- Do not diagnose diseases.
- Do not replace a doctor.
- Do not prescribe or change medication doses.
- For potentially serious symptoms, recommend professional medical evaluation.
- For emergency symptoms, advise immediate emergency medical care.
- Use simple language and answer the question directly first.
- If unrelated to health, politely explain that HeartAI focuses on heart and health topics.

User question:
{question}
"""

        try:
            client = get_gemini_client()
            response = client.models.generate_content(
                model="gemini-3.5-flash-lite",
                contents=prompt,
            )
            text = getattr(response, "text", None)
            if text:
                return text.strip()
            return "I couldn't generate a response. Please try again."
        except Exception:
            return (
                "⚠️ Gemini is temporarily unavailable. "
                "Please verify your API key, internet connection, and selected Gemini model."
            )

    if "heartai_chat_history" not in st.session_state:
        st.session_state.heartai_chat_history = []

    for message in st.session_state.heartai_chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask HeartAI anything about heart health...")

    if question:
        st.session_state.heartai_chat_history.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("HeartAI is thinking..."):
                answer = get_gemini_response(question)
            st.markdown(answer)

        st.session_state.heartai_chat_history.append({"role": "assistant", "content": answer})

# =========================================================
# PROJECT TEAM
# =========================================================
if page == "👥 Project Team":
    st.write("")
    st.markdown("""
    <div class="team-hero">
        <div class="team-hero-title">👥 Project Team &amp; Acknowledgement</div>
        <div class="team-hero-sub">
            HeartAI — Cardiac Intelligence Platform is developed as an academic project,
            combining machine learning, data visualization, and generative AI to support
            cardiac risk screening and health awareness.
        </div>
        <div class="univ-badge">🎓 CSJM University, Kanpur</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="card">
        <div class="card-title">🛠️ Developed By</div>
        <div class="card-sub">Team members who designed, built, and tested the HeartAI platform.</div>
    </div>
    """, unsafe_allow_html=True)

    t1, t2 = st.columns(2)
    team_members = [
        ("Prem Sharma", "320", "Development &amp; Design"),
        ("Krishna Kumar Verma", "290", "Development &amp; Testing"),
    ]
    for col, (name, roll, role) in zip((t1, t2), team_members):
        initials = "".join([w[0] for w in name.split()[:2]]).upper()
        with col:
            st.markdown(f"""
            <div class="team-card">
                <div class="team-avatar">{initials}</div>
                <div class="team-name">{name}</div>
                <div class="team-roll">Roll No. {roll}</div>
                <div class="team-role">{role}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    st.markdown("""
    <div class="card">
        <div class="card-title">🧭 Under the Guidance Of</div>
        <div class="card-sub">This project was completed under academic mentorship and supervision.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="guide-card">
        <div class="guide-avatar">PT</div>
        <div>
            <div class="guide-label">Project Guide</div>
            <div class="guide-name">Pragya Tripathi Ma'am</div>
            <div class="guide-role">Faculty Guide, CSJM University, Kanpur</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.write("")
    st.markdown("""
    <div class="disclaimer">
        <strong>Note:</strong> HeartAI is an academic project built for learning purposes.
        It is not a certified medical device, and its predictions should not be used
        as a substitute for professional medical advice.
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================
st.markdown("""
<div class="footer">
    <div style="font-size:11px;letter-spacing:1.2px;text-transform:uppercase;margin-bottom:10px;">
        HEARTAI • CARDIAC INTELLIGENCE PLATFORM
    </div>
    <strong>Python</strong> · Streamlit · Scikit-learn · Plotly · Gemini
    <div style="margin-top:12px;font-size:11px;">
        Academic project • AI output is informational and not a medical diagnosis.
    </div>
</div>
""", unsafe_allow_html=True)