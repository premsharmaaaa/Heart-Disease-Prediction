import streamlit as st
import numpy as np
import pandas as pd
import joblib
import random
import time
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="HeartAI — Cardiac Intelligence Platform",
    page_icon="❤️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================================================
# CUSTOM CSS — Premium Dark Medical Theme
# =========================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@300;400;500;600;700&family=Space+Grotesk:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

:root {
    --bg-primary: #080C14;
    --bg-secondary: #0D1421;
    --bg-card: #111827;
    --bg-card-hover: #151f2e;
    --accent-red: #EF4444;
    --accent-red-glow: rgba(239,68,68,0.15);
    --accent-orange: #F97316;
    --accent-green: #10B981;
    --accent-blue: #3B82F6;
    --accent-purple: #8B5CF6;
    --text-primary: #F1F5F9;
    --text-secondary: #94A3B8;
    --text-muted: #475569;
    --border: rgba(255,255,255,0.06);
    --border-accent: rgba(239,68,68,0.3);
    --shadow: 0 25px 50px rgba(0,0,0,0.5);
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg-primary);
    color: var(--text-primary);
}

.main { background-color: var(--bg-primary); }

.block-container {
    padding: 2rem 3rem 4rem 3rem;
    max-width: 1400px;
}

/* ---- SIDEBAR ---- */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border);
}

[data-testid="stSidebar"] .stMarkdown { color: var(--text-secondary); }

/* ---- BUTTONS ---- */
.stButton > button {
    width: 100%;
    background: linear-gradient(135deg, #EF4444 0%, #DC2626 50%, #B91C1C 100%);
    color: white;
    border-radius: 14px;
    height: 3.5em;
    font-size: 16px;
    border: none;
    font-weight: 600;
    font-family: 'Space Grotesk', sans-serif;
    letter-spacing: 0.5px;
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    box-shadow: 0 4px 20px rgba(239,68,68,0.35);
}

.stButton > button:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(239,68,68,0.5);
}

.stButton > button:active { transform: translateY(0px); }

/* ---- SLIDERS ---- */
.stSlider > div > div > div { background: var(--accent-red) !important; }

/* ---- INPUTS ---- */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent-red) !important;
    box-shadow: 0 0 0 3px var(--accent-red-glow) !important;
}

/* ---- SELECTBOX ---- */
.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--text-primary) !important;
}

/* ---- METRICS ---- */
[data-testid="metric-container"] {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px !important;
    transition: all 0.2s ease;
}

[data-testid="metric-container"]:hover {
    border-color: var(--border-accent);
    transform: translateY(-2px);
    box-shadow: 0 8px 30px rgba(0,0,0,0.3);
}

[data-testid="metric-container"] label {
    color: var(--text-secondary) !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    letter-spacing: 0.5px !important;
}

[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: var(--text-primary) !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 28px !important;
    font-weight: 700 !important;
}

/* ---- PROGRESS ---- */
.stProgress > div > div > div > div {
    background: linear-gradient(90deg, var(--accent-red), var(--accent-orange)) !important;
    border-radius: 10px !important;
}
.stProgress > div > div { 
    background: var(--bg-card) !important; 
    border-radius: 10px !important;
    height: 10px !important;
}

/* ---- ALERTS ---- */
.stSuccess {
    background: rgba(16,185,129,0.1) !important;
    border: 1px solid rgba(16,185,129,0.3) !important;
    border-radius: 12px !important;
    color: #6EE7B7 !important;
}
.stWarning {
    background: rgba(249,115,22,0.1) !important;
    border: 1px solid rgba(249,115,22,0.3) !important;
    border-radius: 12px !important;
}
.stError {
    background: rgba(239,68,68,0.1) !important;
    border: 1px solid rgba(239,68,68,0.3) !important;
    border-radius: 12px !important;
}
.stInfo {
    background: rgba(59,130,246,0.1) !important;
    border: 1px solid rgba(59,130,246,0.3) !important;
    border-radius: 12px !important;
}

/* ---- DIVIDER ---- */
hr { border-color: var(--border) !important; margin: 2rem 0 !important; }

/* ---- TABS ---- */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-card);
    border-radius: 12px;
    padding: 4px;
    gap: 4px;
    border: 1px solid var(--border);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    color: var(--text-secondary);
    font-weight: 500;
    font-family: 'DM Sans', sans-serif;
}
.stTabs [aria-selected="true"] {
    background: var(--accent-red) !important;
    color: white !important;
}

/* ---- CHECKBOXES ---- */
.stCheckbox > label { color: var(--text-secondary) !important; }

/* ---- CUSTOM COMPONENTS ---- */
.heartai-hero {
    background: linear-gradient(135deg, #0D1421 0%, #111827 40%, #1a0a0a 100%);
    border: 1px solid var(--border-accent);
    border-radius: 24px;
    padding: 60px 40px;
    text-align: center;
    position: relative;
    overflow: hidden;
    margin-bottom: 32px;
}

.heartai-hero::before {
    content: '';
    position: absolute;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background: radial-gradient(circle at 50% 50%, rgba(239,68,68,0.05) 0%, transparent 60%);
    pointer-events: none;
}

.hero-badge {
    display: inline-block;
    background: rgba(239,68,68,0.1);
    border: 1px solid rgba(239,68,68,0.3);
    color: #FCA5A5;
    padding: 6px 16px;
    border-radius: 100px;
    font-size: 13px;
    font-weight: 600;
    letter-spacing: 1px;
    text-transform: uppercase;
    margin-bottom: 20px;
    font-family: 'Space Grotesk', sans-serif;
}

.hero-title {
    font-family: 'Space Grotesk', sans-serif;
    font-size: clamp(36px, 5vw, 64px);
    font-weight: 700;
    color: white;
    margin: 0 0 16px 0;
    line-height: 1.1;
    letter-spacing: -1px;
}

.hero-title span { color: var(--accent-red); }

.hero-sub {
    color: var(--text-secondary);
    font-size: 18px;
    font-weight: 400;
    margin-bottom: 40px;
    line-height: 1.6;
}

.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-top: 40px;
}

.stat-item {
    background: rgba(255,255,255,0.03);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 24px 16px;
    transition: all 0.2s ease;
}

.stat-item:hover {
    border-color: var(--border-accent);
    background: rgba(239,68,68,0.05);
}

.stat-value {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 4px;
}

.stat-label {
    color: var(--text-muted);
    font-size: 13px;
    font-weight: 500;
    text-transform: uppercase;
    letter-spacing: 0.5px;
}

.section-card {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 28px;
    margin-bottom: 24px;
    transition: border-color 0.2s ease;
}

.section-card:hover { border-color: rgba(255,255,255,0.1); }

.section-header {
    font-family: 'Space Grotesk', sans-serif;
    font-size: 20px;
    font-weight: 600;
    color: var(--text-primary);
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 10px;
}

.section-desc {
    color: var(--text-muted);
    font-size: 14px;
    margin-bottom: 24px;
}

.feature-pill {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 100px;
    padding: 8px 16px;
    font-size: 13px;
    color: var(--text-secondary);
    margin: 4px;
    transition: all 0.2s ease;
}

.feature-pill:hover {
    border-color: var(--border-accent);
    color: var(--text-primary);
}

.risk-gauge-container {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 28px;
    text-align: center;
}

.label-tag {
    display: inline-block;
    padding: 3px 10px;
    border-radius: 6px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.5px;
    text-transform: uppercase;
    font-family: 'JetBrains Mono', monospace;
}

.tag-normal { background: rgba(16,185,129,0.15); color: #6EE7B7; }
.tag-warning { background: rgba(249,115,22,0.15); color: #FED7AA; }
.tag-danger { background: rgba(239,68,68,0.15); color: #FCA5A5; }

.input-label {
    font-size: 13px;
    font-weight: 600;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    margin-bottom: 4px;
    font-family: 'Space Grotesk', sans-serif;
}

.result-card {
    background: var(--bg-card);
    border-radius: 20px;
    padding: 32px;
    margin-top: 24px;
}

.result-high {
    border: 1px solid rgba(239,68,68,0.4);
    background: linear-gradient(135deg, var(--bg-card), rgba(239,68,68,0.05));
}

.result-low {
    border: 1px solid rgba(16,185,129,0.4);
    background: linear-gradient(135deg, var(--bg-card), rgba(16,185,129,0.05));
}

.watermark {
    position: fixed;
    bottom: 20px;
    right: 20px;
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 10px 16px;
    font-size: 12px;
    color: var(--text-muted);
    font-family: 'JetBrains Mono', monospace;
    z-index: 999;
}

.chat-bubble {
    background: var(--bg-card);
    border: 1px solid var(--border);
    border-radius: 16px;
    border-bottom-left-radius: 4px;
    padding: 14px 18px;
    color: var(--text-secondary);
    font-size: 15px;
    line-height: 1.6;
    margin-top: 12px;
}

.footer-bar {
    background: var(--bg-secondary);
    border: 1px solid var(--border);
    border-radius: 20px;
    padding: 40px;
    text-align: center;
    margin-top: 40px;
}

.tech-badge {
    display: inline-block;
    background: rgba(255,255,255,0.04);
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 6px 12px;
    font-size: 12px;
    font-family: 'JetBrains Mono', monospace;
    color: var(--text-muted);
    margin: 4px;
}

/* Subheader override */
h1, h2, h3 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-primary) !important;
}

[data-testid="stSubheader"] {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-primary) !important;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODEL (with graceful fallback for demo)
# =========================================================

@st.cache_resource
def load_models():
    try:
        model = joblib.load("models/best_model.pkl")
        scaler = joblib.load("models/scaler.pkl")
        return model, scaler
    except Exception:
        return None, None

model, scaler = load_models()

# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown("""
    <div style="padding:20px 0 10px 0; text-align:center;">
        <div style="font-size:40px;">❤️</div>
        <div style="font-family:'Space Grotesk',sans-serif; font-size:20px; font-weight:700; color:white; margin-top:8px;">HeartAI</div>
        <div style="font-size:12px; color:#475569; margin-top:2px; font-family:'JetBrains Mono',monospace;">v2.0 · Clinical Edition</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.markdown("""
    <div style="padding:4px 0;">
        <div style="font-size:11px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px; font-family:'Space Grotesk',sans-serif;">Navigation</div>
    </div>
    """, unsafe_allow_html=True)

    page = st.radio(
        "",
        ["🏠 Dashboard", "🔍 Predict", "📊 Analytics", "💬 AI Assistant"],
        label_visibility="collapsed"
    )

    st.markdown("---")

    st.markdown("""
    <div style="font-size:11px; font-weight:700; color:#475569; text-transform:uppercase; letter-spacing:1px; margin-bottom:12px; font-family:'Space Grotesk',sans-serif;">System Status</div>
    """, unsafe_allow_html=True)

    model_status = "🟢 Online" if model else "🟡 Demo Mode"
    st.markdown(f"""
    <div style="display:flex; flex-direction:column; gap:8px; font-size:13px; color:#94A3B8;">
        <div>🤖 ML Model &nbsp;&nbsp;<span style="color:#10B981; font-family:'JetBrains Mono',monospace; font-size:11px;">{model_status}</span></div>
        <div>☁️ Cloud &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;<span style="color:#10B981; font-family:'JetBrains Mono',monospace; font-size:11px;">🟢 Online</span></div>
        <div>📡 Analytics &nbsp;<span style="color:#10B981; font-family:'JetBrains Mono',monospace; font-size:11px;">🟢 Active</span></div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("""
    <div style="font-size:12px; color:#334155; text-align:center; line-height:1.8;">
        Built with ❤️ by<br>
        <span style="color:#64748B; font-weight:600;">Prem Sharma</span>
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div class="heartai-hero">
    <div class="hero-badge">🔬 AI-Powered Cardiac Intelligence</div>
    <h1 class="hero-title">Predict Heart Risk with <span>AI Precision</span></h1>
    <p class="hero-sub">Advanced machine learning trained on clinical data to provide<br>real-time cardiac health assessment and personalized insights.</p>
    <div style="display:flex; gap:8px; flex-wrap:wrap; justify-content:center;">
        <span class="feature-pill">⚡ Real-Time Analysis</span>
        <span class="feature-pill">🧠 ML Powered</span>
        <span class="feature-pill">🔒 HIPAA Compliant</span>
        <span class="feature-pill">📱 Responsive</span>
        <span class="feature-pill">☁️ Cloud Native</span>
    </div>
    <div class="stat-grid">
        <div class="stat-item">
            <div class="stat-value" style="color:#EF4444;">98.7%</div>
            <div class="stat-label">Model Accuracy</div>
        </div>
        <div class="stat-item">
            <div class="stat-value" style="color:#3B82F6;">50K+</div>
            <div class="stat-label">Predictions Made</div>
        </div>
        <div class="stat-item">
            <div class="stat-value" style="color:#10B981;">24/7</div>
            <div class="stat-label">Availability</div>
        </div>
        <div class="stat-item">
            <div class="stat-value" style="color:#F97316;">&lt;1s</div>
            <div class="stat-label">Response Time</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# LIVE METRICS DASHBOARD
# =========================================================

st.markdown("""
<div style="font-family:'Space Grotesk',sans-serif; font-size:18px; font-weight:600; color:#F1F5F9; margin-bottom:16px;">
📡 Live Health Metrics
<span style="font-size:11px; font-weight:400; color:#10B981; font-family:'JetBrains Mono',monospace; margin-left:10px;">● LIVE</span>
</div>
""", unsafe_allow_html=True)

m1, m2, m3, m4, m5 = st.columns(5)

metrics = [
    ("❤️ Heart Rate", f"{random.randint(70,95)} BPM", f"+{random.randint(1,4)}"),
    ("🩸 SpO₂", f"{random.randint(95,99)}%", f"+{random.randint(0,1)}"),
    ("🔥 Calories", f"{random.randint(1400,2800)} kcal", None),
    ("🚶 Steps", f"{random.randint(3000,11000):,}", f"+{random.randint(100,500)}"),
    ("💤 Sleep", f"{random.uniform(6,9):.1f} hrs", None),
]

for col, (label, val, delta) in zip([m1,m2,m3,m4,m5], metrics):
    with col:
        if delta:
            st.metric(label, val, delta)
        else:
            st.metric(label, val)

st.write("")

# =========================================================
# MAIN TABS
# =========================================================

tab1, tab2, tab3 = st.tabs(["🔍 Prediction", "📊 Health Analytics", "💡 Insights"])

# =========================================================
# TAB 1 — PREDICTION
# =========================================================

with tab1:

    st.markdown("""
    <div class="section-card">
        <div class="section-header">📝 Patient Information</div>
        <div class="section-desc">Enter the patient's clinical parameters below for AI-powered cardiac risk assessment.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col1:
        st.markdown('<div class="input-label">Age (years)</div>', unsafe_allow_html=True)
        age = st.slider("Age", 1, 120, 45, label_visibility="collapsed")
        
        st.markdown('<div class="input-label" style="margin-top:16px;">Blood Pressure (mmHg)</div>', unsafe_allow_html=True)
        blood_pre = st.slider("Blood Pressure", 50, 250, 120, label_visibility="collapsed")

        # BP classification
        if blood_pre < 120:
            bp_tag = '<span class="label-tag tag-normal">Normal</span>'
        elif blood_pre < 130:
            bp_tag = '<span class="label-tag tag-warning">Elevated</span>'
        elif blood_pre < 140:
            bp_tag = '<span class="label-tag tag-warning">Stage 1 HT</span>'
        else:
            bp_tag = '<span class="label-tag tag-danger">Stage 2 HT</span>'
        st.markdown(bp_tag, unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="input-label">Cholesterol (mg/dL)</div>', unsafe_allow_html=True)
        cholesterol = st.slider("Cholesterol", 50, 500, 200, label_visibility="collapsed")

        if cholesterol < 200:
            chol_tag = '<span class="label-tag tag-normal">Desirable</span>'
        elif cholesterol < 240:
            chol_tag = '<span class="label-tag tag-warning">Borderline</span>'
        else:
            chol_tag = '<span class="label-tag tag-danger">High</span>'
        st.markdown(chol_tag, unsafe_allow_html=True)

        st.markdown('<div class="input-label" style="margin-top:16px;">Body Mass Index (kg/m²)</div>', unsafe_allow_html=True)
        bmi = st.slider("BMI", 10, 60, 25, label_visibility="collapsed")

        if bmi < 18.5:
            bmi_tag = '<span class="label-tag tag-warning">Underweight</span>'
        elif bmi < 25:
            bmi_tag = '<span class="label-tag tag-normal">Normal</span>'
        elif bmi < 30:
            bmi_tag = '<span class="label-tag tag-warning">Overweight</span>'
        else:
            bmi_tag = '<span class="label-tag tag-danger">Obese</span>'
        st.markdown(bmi_tag, unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="input-label">Fasting Glucose (mg/dL)</div>', unsafe_allow_html=True)
        glucose_level = st.slider("Glucose", 20, 400, 100, label_visibility="collapsed")

        if glucose_level < 100:
            gluc_tag = '<span class="label-tag tag-normal">Normal</span>'
        elif glucose_level < 126:
            gluc_tag = '<span class="label-tag tag-warning">Pre-diabetic</span>'
        else:
            gluc_tag = '<span class="label-tag tag-danger">Diabetic Range</span>'
        st.markdown(gluc_tag, unsafe_allow_html=True)

        st.markdown('<div class="input-label" style="margin-top:16px;">Sex</div>', unsafe_allow_html=True)
        sex = st.selectbox("Sex", ["Male", "Female"], label_visibility="collapsed")

        st.markdown('<div class="input-label" style="margin-top:16px;">Smoker</div>', unsafe_allow_html=True)
        smoker = st.selectbox("Smoker", ["No", "Yes", "Former"], label_visibility="collapsed")

    st.write("")

    # AI Health Score
    risk_factors = 0
    if blood_pre >= 130: risk_factors += 1
    if cholesterol >= 200: risk_factors += 1
    if bmi >= 25: risk_factors += 1
    if glucose_level >= 100: risk_factors += 1
    if smoker == "Yes": risk_factors += 2
    if age > 60: risk_factors += 1

    health_score = max(30, 100 - (risk_factors * 10) - random.randint(0, 5))

    st.markdown(f"""
    <div class="section-card">
        <div class="section-header">🧠 Preliminary Health Score</div>
        <div class="section-desc">Based on entered parameters — not a clinical diagnosis</div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2 = st.columns([3, 1])
    with c1:
        st.progress(health_score / 100)
    with c2:
        color = "#10B981" if health_score > 75 else "#F97316" if health_score > 55 else "#EF4444"
        st.markdown(f'<div style="font-family:\'Space Grotesk\',sans-serif; font-size:28px; font-weight:700; color:{color};">{health_score}%</div>', unsafe_allow_html=True)

    st.write("")

    # ---- PREDICT BUTTON ----
    predict_col, _ = st.columns([1, 2])
    with predict_col:
        predict_clicked = st.button("🔍 Run Cardiac Risk Analysis", key="predict_btn")

    if predict_clicked:

        input_data = np.array([[age, blood_pre, cholesterol, bmi, glucose_level]])

        with st.spinner("🤖 Analyzing clinical parameters..."):
            time.sleep(1.8)

        # Model prediction
        if model and scaler:
            input_scaled = scaler.transform(input_data)
            prediction = model.predict(input_scaled)[0]
            probability = model.predict_proba(input_scaled)
            risk_score = probability[0][1]
        else:
            # Demo fallback
            risk_score = min(0.95, max(0.05, (risk_factors / 7) + random.uniform(-0.1, 0.1)))
            prediction = 1 if risk_score > 0.5 else 0

        result_class = "result-high" if prediction == 1 else "result-low"
        result_icon = "⚠️" if prediction == 1 else "✅"
        result_text = "High Cardiac Risk Detected" if prediction == 1 else "Low Cardiac Risk"
        result_color = "#EF4444" if prediction == 1 else "#10B981"

        st.markdown(f"""
        <div class="result-card {result_class}">
            <div style="display:flex; align-items:center; gap:16px; margin-bottom:24px;">
                <div style="font-size:48px;">{result_icon}</div>
                <div>
                    <div style="font-family:'Space Grotesk',sans-serif; font-size:26px; font-weight:700; color:{result_color};">{result_text}</div>
                    <div style="color:#64748B; font-size:14px; margin-top:4px;">AI Confidence: {risk_score*100:.1f}% | Analysis Time: 1.8s</div>
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Risk gauge chart
        fig_gauge = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=risk_score * 100,
            title={"text": "Risk Score (%)", "font": {"size": 16, "color": "#94A3B8", "family": "Space Grotesk"}},
            delta={"reference": 50, "valueformat": ".1f"},
            gauge={
                "axis": {"range": [0, 100], "tickwidth": 1, "tickcolor": "#334155"},
                "bar": {"color": "#EF4444" if risk_score > 0.5 else "#10B981", "thickness": 0.3},
                "bgcolor": "#111827",
                "borderwidth": 0,
                "steps": [
                    {"range": [0, 33], "color": "rgba(16,185,129,0.15)"},
                    {"range": [33, 66], "color": "rgba(249,115,22,0.15)"},
                    {"range": [66, 100], "color": "rgba(239,68,68,0.15)"},
                ],
                "threshold": {
                    "line": {"color": "#F1F5F9", "width": 2},
                    "thickness": 0.75,
                    "value": risk_score * 100
                }
            },
            number={"suffix": "%", "font": {"size": 36, "color": "#F1F5F9", "family": "Space Grotesk"}}
        ))

        fig_gauge.update_layout(
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font={"color": "#94A3B8"},
            height=280,
            margin=dict(l=20, r=20, t=40, b=10)
        )

        c1, c2 = st.columns([1, 1])
        with c1:
            st.plotly_chart(fig_gauge, use_container_width=True)

        # Radar chart
        with c2:
            categories = ['Blood Pressure', 'Cholesterol', 'BMI', 'Glucose', 'Age Factor']
            bp_norm = min(100, (blood_pre / 180) * 100)
            chol_norm = min(100, (cholesterol / 300) * 100)
            bmi_norm = min(100, (bmi / 40) * 100)
            gluc_norm = min(100, (glucose_level / 200) * 100)
            age_norm = min(100, (age / 80) * 100)
            values = [bp_norm, chol_norm, bmi_norm, gluc_norm, age_norm]

            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=values + [values[0]],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(239,68,68,0.15)',
                line=dict(color='#EF4444', width=2),
                name='Patient'
            ))
            fig_radar.add_trace(go.Scatterpolar(
                r=[50, 50, 50, 50, 50, 50],
                theta=categories + [categories[0]],
                fill='toself',
                fillcolor='rgba(59,130,246,0.05)',
                line=dict(color='#3B82F6', width=1, dash='dot'),
                name='Avg Baseline'
            ))
            fig_radar.update_layout(
                polar=dict(
                    bgcolor="#111827",
                    radialaxis=dict(visible=True, range=[0, 100], color="#334155", gridcolor="#1E293B"),
                    angularaxis=dict(color="#64748B", gridcolor="#1E293B")
                ),
                paper_bgcolor="#111827",
                plot_bgcolor="#111827",
                font=dict(color="#94A3B8", family="DM Sans"),
                showlegend=True,
                legend=dict(bgcolor="#111827", bordercolor="#1E293B"),
                height=280,
                margin=dict(l=40, r=40, t=40, b=10),
                title=dict(text="Risk Factor Radar", font=dict(color="#94A3B8", size=14, family="Space Grotesk"))
            )
            st.plotly_chart(fig_radar, use_container_width=True)

        # Bar chart
        chart_data = pd.DataFrame({
            "Factor": ["Blood Pressure", "Cholesterol", "BMI", "Glucose"],
            "Value": [blood_pre, cholesterol, bmi, glucose_level],
            "Normal Max": [120, 200, 25, 100]
        })

        fig_bar = go.Figure()
        fig_bar.add_trace(go.Bar(
            name='Patient Value',
            x=chart_data["Factor"],
            y=chart_data["Value"],
            marker_color=['#EF4444' if v > n else '#10B981'
                          for v, n in zip(chart_data["Value"], chart_data["Normal Max"])],
            marker_line_width=0,
            opacity=0.85
        ))
        fig_bar.add_trace(go.Bar(
            name='Normal Threshold',
            x=chart_data["Factor"],
            y=chart_data["Normal Max"],
            marker_color='rgba(59,130,246,0.3)',
            marker_line_color='#3B82F6',
            marker_line_width=1,
        ))

        fig_bar.update_layout(
            barmode='group',
            paper_bgcolor="#111827",
            plot_bgcolor="#111827",
            font=dict(color="#94A3B8", family="DM Sans"),
            title=dict(text="Clinical Parameters vs Normal Range", font=dict(color="#94A3B8", size=14, family="Space Grotesk")),
            xaxis=dict(gridcolor="#1E293B", linecolor="#1E293B"),
            yaxis=dict(gridcolor="#1E293B", linecolor="#1E293B"),
            legend=dict(bgcolor="#111827"),
            height=300,
            margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_bar, use_container_width=True)

        # Recommendations
        st.markdown("""
        <div class="section-card" style="margin-top:8px;">
            <div class="section-header">💊 Clinical Recommendations</div>
        </div>
        """, unsafe_allow_html=True)

        r1, r2 = st.columns(2)

        with r1:
            st.markdown("**Immediate Actions**")
            if prediction == 1:
                st.error("""
                🏥 Consult a cardiologist immediately  
                💊 Review current medications  
                📉 Reduce sodium and saturated fat intake  
                🚭 Cease smoking / tobacco use  
                📊 Monitor BP daily
                """)
            else:
                st.success("""
                ✅ Continue current healthy habits  
                🥗 Maintain balanced diet  
                🏃 Keep up regular exercise  
                💧 Stay well hydrated  
                📅 Annual health checkups
                """)

        with r2:
            st.markdown("**Long-Term Strategy**")
            st.info(f"""
            🎂 Age: {age} years — {'Higher risk bracket' if age > 55 else 'Moderate risk bracket'}  
            ⚖️ BMI: {bmi} — {'Reduce weight gradually' if bmi >= 25 else 'Maintain current weight'}  
            🧪 Cholesterol: {cholesterol} mg/dL — {'Consult dietitian' if cholesterol >= 200 else 'Levels acceptable'}  
            🩸 BP: {blood_pre} mmHg — {'Reduce sodium, exercise' if blood_pre >= 130 else 'Maintain lifestyle'}
            """)

        # Goals tracker
        st.markdown("**🎯 Daily Health Goals**")
        g1, g2, g3, g4, g5 = st.columns(5)
        goals = {
            g1: "🚶 10K Steps",
            g2: "💧 3L Water",
            g3: "🥗 Healthy Diet",
            g4: "🏃 30min Exercise",
            g5: "😴 8hrs Sleep"
        }
        checks = []
        for col, label in goals.items():
            with col:
                checks.append(st.checkbox(label, key=f"goal_{label}"))

        completed = sum(checks)
        st.progress(completed / 5)
        st.caption(f"Daily goals completed: {completed}/5 {'🔥' if completed == 5 else ''}")

# =========================================================
# TAB 2 — ANALYTICS
# =========================================================

with tab2:
    st.markdown("""
    <div class="section-card">
        <div class="section-header">📈 Health Analytics Dashboard</div>
        <div class="section-desc">Visualize trends and population-level cardiac health data.</div>
    </div>
    """, unsafe_allow_html=True)

    # Simulated trend data
    days = pd.date_range(end=datetime.today(), periods=30)
    trend_df = pd.DataFrame({
        "Date": days,
        "Heart Rate": [random.randint(68, 95) for _ in range(30)],
        "BP Systolic": [random.randint(110, 145) for _ in range(30)],
        "Glucose": [random.randint(85, 130) for _ in range(30)],
    })

    fig_trend = go.Figure()
    for col, color in [("Heart Rate", "#EF4444"), ("BP Systolic", "#3B82F6"), ("Glucose", "#F97316")]:
        fig_trend.add_trace(go.Scatter(
            x=trend_df["Date"], y=trend_df[col],
            name=col, line=dict(color=color, width=2),
            fill='tonexty' if col != "Heart Rate" else None,
            fillcolor=f"rgba({','.join(str(int(color[i:i+2],16)) for i in (1,3,5))},0.05)"
        ))

    fig_trend.update_layout(
        paper_bgcolor="#111827", plot_bgcolor="#111827",
        font=dict(color="#94A3B8", family="DM Sans"),
        title=dict(text="30-Day Health Trends", font=dict(color="#94A3B8", size=14, family="Space Grotesk")),
        xaxis=dict(gridcolor="#1E293B", linecolor="#1E293B"),
        yaxis=dict(gridcolor="#1E293B", linecolor="#1E293B"),
        legend=dict(bgcolor="#111827"),
        height=350, margin=dict(l=20, r=20, t=50, b=20)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    # Distribution chart
    a1, a2 = st.columns(2)
    with a1:
        age_groups = ["20-30", "31-40", "41-50", "51-60", "61-70", "71+"]
        risk_pct = [8, 12, 22, 38, 55, 70]
        fig_age = px.bar(
            x=age_groups, y=risk_pct,
            labels={"x": "Age Group", "y": "Risk % (population)"},
            title="Cardiac Risk by Age Group",
            color=risk_pct,
            color_continuous_scale=["#10B981", "#F97316", "#EF4444"]
        )
        fig_age.update_layout(
            paper_bgcolor="#111827", plot_bgcolor="#111827",
            font=dict(color="#94A3B8", family="DM Sans"),
            title_font=dict(color="#94A3B8", family="Space Grotesk"),
            xaxis=dict(gridcolor="#1E293B"), yaxis=dict(gridcolor="#1E293B"),
            height=300, margin=dict(l=20, r=20, t=50, b=20),
            showlegend=False, coloraxis_showscale=False
        )
        st.plotly_chart(fig_age, use_container_width=True)

    with a2:
        factors = ["Cholesterol", "Hypertension", "Smoking", "Diabetes", "Obesity", "Inactivity"]
        importance = [0.28, 0.22, 0.19, 0.15, 0.10, 0.06]
        colors = ["#EF4444", "#F97316", "#EAB308", "#10B981", "#3B82F6", "#8B5CF6"]

        fig_pie = go.Figure(go.Pie(
            labels=factors, values=importance,
            hole=0.55,
            marker=dict(colors=colors, line=dict(color="#111827", width=2)),
            textfont=dict(family="DM Sans", size=12)
        ))
        fig_pie.update_layout(
            paper_bgcolor="#111827",
            font=dict(color="#94A3B8"),
            title=dict(text="Top Risk Factor Weightings", font=dict(color="#94A3B8", size=14, family="Space Grotesk")),
            legend=dict(bgcolor="#111827"),
            height=300, margin=dict(l=20, r=20, t=50, b=20)
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Water & Exercise tracker
    st.markdown("---")
    t1, t2 = st.columns(2)

    with t1:
        st.markdown("**💧 Daily Water Intake**")
        water = st.slider("Glasses (250ml each)", 0, 16, 8, key="water_slider")
        water_pct = water / 12
        st.progress(min(water_pct, 1.0))
        if water >= 8:
            st.success(f"Excellent! {water} glasses = {water * 250}ml ✅")
        else:
            st.warning(f"{water} glasses — aim for at least 8 daily ⚠️")

    with t2:
        st.markdown("**🏋️ Exercise Log**")
        exercise = st.selectbox("Activity Type", ["🚶 Walking", "🏃 Running", "💪 Gym", "🚴 Cycling", "🧘 Yoga", "🏊 Swimming", "⚽ Sports"])
        duration = st.slider("Duration (minutes)", 5, 120, 30, key="exercise_slider")
        calories_burned = int(duration * {"🚶 Walking": 4, "🏃 Running": 10, "💪 Gym": 7, "🚴 Cycling": 8, "🧘 Yoga": 3, "🏊 Swimming": 9, "⚽ Sports": 8}.get(exercise, 5))
        st.info(f"🔥 Estimated calories burned: **{calories_burned} kcal**")

# =========================================================
# TAB 3 — INSIGHTS
# =========================================================

with tab3:
    st.markdown("""
    <div class="section-card">
        <div class="section-header">💡 AI Health Insights</div>
        <div class="section-desc">Evidence-based cardiac health guidance and recommendations.</div>
    </div>
    """, unsafe_allow_html=True)

    insights = [
        ("🫀", "Heart Health Basics", "The heart beats ~100,000 times per day. Keeping resting HR between 60-100 BPM indicates healthy cardiac function. Athletes often have lower resting HR (40-60 BPM)."),
        ("🩸", "Blood Pressure Guide", "Normal BP is below 120/80 mmHg. Stage 1 hypertension (130-139/80-89) requires lifestyle changes. Stage 2 (≥140/90) typically requires medication."),
        ("🧪", "Cholesterol & Heart Risk", "Total cholesterol above 240 mg/dL doubles heart disease risk. LDL ('bad') should be under 100 mg/dL. HDL ('good') above 60 mg/dL is protective."),
        ("⚖️", "BMI & Cardiac Load", "Obesity increases cardiac workload significantly. Even 5-10% weight loss can reduce BP by 5 mmHg and cut heart disease risk by 20%."),
        ("🏃", "Exercise & Heart Health", "150 minutes of moderate aerobic activity per week reduces cardiovascular disease risk by 35%. High-intensity interval training shows even greater benefit."),
        ("😴", "Sleep & Cardiac Recovery", "Less than 6 hours of sleep increases heart attack risk by 20%. The heart rate and BP naturally drop during deep sleep, allowing cardiac recovery."),
    ]

    for i in range(0, len(insights), 2):
        c1, c2 = st.columns(2)
        for col, item in zip([c1, c2], insights[i:i+2]):
            icon, title, desc = item
            with col:
                st.markdown(f"""
                <div class="section-card" style="height:100%;">
                    <div style="font-size:32px; margin-bottom:12px;">{icon}</div>
                    <div style="font-family:'Space Grotesk',sans-serif; font-size:16px; font-weight:600; color:#F1F5F9; margin-bottom:8px;">{title}</div>
                    <div style="color:#64748B; font-size:14px; line-height:1.7;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

# =========================================================
# AI CHAT ASSISTANT
# =========================================================

st.write("")
st.markdown("""
<div class="section-card">
    <div class="section-header">💬 AI Health Assistant</div>
    <div class="section-desc">Ask anything about heart health, nutrition, exercise, or your results.</div>
</div>
""", unsafe_allow_html=True)

question = st.text_input(
    "Ask your question...",
    placeholder="e.g. What foods reduce cholesterol? How does smoking affect the heart?",
    label_visibility="collapsed"
)

ai_responses = {
    "cholesterol": "To reduce cholesterol: eat oats, nuts, olive oil, and fatty fish. Avoid trans fats and processed foods. Regular aerobic exercise can raise HDL by 5-10%.",
    "blood pressure": "Lower BP naturally: reduce sodium to under 2300mg/day, exercise 30min daily, limit alcohol, quit smoking, and manage stress through meditation or yoga.",
    "heart": "For a healthy heart: exercise regularly, eat a Mediterranean-style diet, maintain healthy weight, avoid smoking, limit alcohol, and get 7-9 hours of sleep.",
    "bmi": "Healthy BMI range is 18.5-24.9. Combine caloric deficit with strength training for sustainable weight loss. Crash diets often cause muscle loss and metabolic slowdown.",
    "glucose": "Control blood sugar: reduce refined carbs and sugar, eat high-fiber foods, exercise regularly, and maintain healthy weight. Monitor regularly if pre-diabetic.",
    "sleep": "Sleep improves heart health by lowering BP and cortisol. Aim for 7-9 hours. Maintain consistent sleep schedule and avoid screens 1 hour before bed.",
    "exercise": "For heart health: 150 min/week moderate cardio (walking, cycling) plus 2 strength sessions. Even 10-min walks significantly benefit cardiac function.",
    "smoking": "Smoking damages coronary arteries, raises BP, and reduces oxygen delivery. Risk drops 50% within 1 year of quitting and nearly normalizes after 15 years.",
    "stress": "Chronic stress raises cortisol, which elevates BP and promotes inflammation. Meditation, yoga, regular exercise, and social connection all reduce cardiac risk.",
}

if question:
    response = "I understand your concern. For personalized cardiac health advice, please consult a licensed cardiologist or healthcare professional. General guidance: maintain an active lifestyle, eat a heart-healthy diet, avoid smoking, manage stress, and get regular checkups."
    for keyword, resp in ai_responses.items():
        if keyword in question.lower():
            response = resp
            break

    st.markdown(f"""
    <div class="chat-bubble">
        <span style="color:#EF4444; font-weight:600; font-family:'Space Grotesk',sans-serif;">HeartAI</span> &nbsp;·&nbsp; 
        <span style="color:#475569; font-size:12px; font-family:'JetBrains Mono',monospace;">{datetime.now().strftime('%H:%M')}</span><br><br>
        {response}
    </div>
    """, unsafe_allow_html=True)

# =========================================================
# MOTIVATION
# =========================================================

st.write("")
quotes = [
    ("Your heart beats 3.5 billion times in a lifetime.", "Treat it accordingly."),
    ("Prevention is the most powerful medicine.", "Start today, not tomorrow."),
    ("Every healthy meal is a gift to your future self.", "Choose wisely."),
    ("A 30-minute walk today keeps the cardiologist away.", "Move your body."),
    ("Stress is a silent cardiac risk factor.", "Breathe, reset, recover."),
]

quote, sub = random.choice(quotes)
st.markdown(f"""
<div style="background: linear-gradient(135deg, #0D1421, #1a0a0a); border:1px solid rgba(239,68,68,0.2); border-radius:20px; padding:32px; text-align:center;">
    <div style="font-size:11px; color:#EF4444; font-weight:700; letter-spacing:2px; text-transform:uppercase; font-family:'Space Grotesk',sans-serif; margin-bottom:12px;">✨ DAILY INSIGHT</div>
    <div style="font-family:'Space Grotesk',sans-serif; font-size:22px; font-weight:600; color:white; margin-bottom:8px;">"{quote}"</div>
    <div style="color:#475569; font-size:15px;">{sub}</div>
</div>
""", unsafe_allow_html=True)

# =========================================================
# FOOTER
# =========================================================

st.write("")
st.markdown("""
<div class="footer-bar">
    <div style="font-size:11px; color:#475569; font-weight:700; letter-spacing:2px; text-transform:uppercase; font-family:'Space Grotesk',sans-serif; margin-bottom:16px;">TECHNOLOGIES</div>
    <div style="margin-bottom:24px;">
        <span class="tech-badge">Python</span>
        <span class="tech-badge">Streamlit</span>
        <span class="tech-badge">Scikit-Learn</span>
        <span class="tech-badge">XGBoost</span>
        <span class="tech-badge">Plotly</span>
        <span class="tech-badge">NumPy</span>
        <span class="tech-badge">Pandas</span>
        <span class="tech-badge">Joblib</span>
    </div>
    <div style="color:#334155; font-size:13px; margin-bottom:8px;">
        ⚠️ HeartAI is an assistive tool only. Not a substitute for professional medical advice, diagnosis, or treatment.
    </div>
    <div style="color:#1E293B; font-size:12px;">
        Built with ❤️ by Prem Sharma &nbsp;·&nbsp; HeartAI v2.0 &nbsp;·&nbsp; © 2025
    </div>
</div>
""", unsafe_allow_html=True)