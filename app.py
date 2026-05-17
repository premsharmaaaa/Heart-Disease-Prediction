import streamlit as st
import numpy as np
import joblib
import pandas as pd
import plotly.express as px
from datetime import datetime

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Heart Disease AI System",
    page_icon="❤️",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: 'Segoe UI';
}

.main {
    background-color: #0E1117;
    color: white;
}

/* TITLE */

.title {
    text-align: center;
    font-size: 55px;
    font-weight: bold;
    color: #FF4B2B;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #CCCCCC;
    margin-bottom: 30px;
}

/* CARD */

.card {
    background-color: #161B22;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0px 0px 20px rgba(255,255,255,0.08);
    margin-top: 20px;
}

/* BUTTON */

.stButton>button {
    width: 100%;
    background: linear-gradient(to right, #ff416c, #ff4b2b);
    color: white;
    border-radius: 12px;
    height: 3.2em;
    font-size: 20px;
    border: none;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.02);
    background: linear-gradient(to right, #ff4b2b, #ff416c);
}

/* METRIC */

.metric-card {
    background: #161B22;
    padding: 20px;
    border-radius: 15px;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# =========================================
# LOAD MODEL
# =========================================

model = joblib.load("models/best_model.pkl")
scaler = joblib.load("models/scaler.pkl")

# =========================================
# HEADER
# =========================================

st.markdown(
    '<p class="title">❤️ Heart Disease Prediction AI</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Advanced Machine Learning Based Healthcare System</p>',
    unsafe_allow_html=True
)

# =========================================
# SIDEBAR
# =========================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/2966/2966486.png",
    width=120
)

st.sidebar.title("🩺 About Project")

st.sidebar.info("""
This AI system predicts the risk of heart disease
using Machine Learning algorithms.

Technologies Used:
- Python
- Streamlit
- Scikit-learn
- XGBoost
- NumPy
- Plotly
""")

st.sidebar.success("Developed by Prem ❤️")

st.sidebar.write("### 📅 Current Time")
st.sidebar.write(datetime.now().strftime("%d-%m-%Y %H:%M:%S"))

# =========================================
# INPUT SECTION
# =========================================

st.markdown("## 🧾 Enter Patient Details")

col1, col2 = st.columns(2)

with col1:

    age = st.slider(
        "Age",
        1,
        120,
        30
    )

    blood_pre = st.slider(
        "Blood Pressure",
        50,
        250,
        120
    )

    cholesterol = st.slider(
        "Cholesterol",
        50,
        500,
        200
    )

with col2:

    bmi = st.slider(
        "BMI",
        10,
        60,
        25
    )

    glucose_level = st.slider(
        "Glucose Level",
        20,
        400,
        100
    )

# =========================================
# HEALTH METRICS
# =========================================

st.write("")

m1, m2, m3 = st.columns(3)

with m1:
    st.metric(
        label="Blood Pressure",
        value=f"{blood_pre}"
    )

with m2:
    st.metric(
        label="BMI",
        value=f"{bmi}"
    )

with m3:
    st.metric(
        label="Glucose",
        value=f"{glucose_level}"
    )

# =========================================
# PREDICT BUTTON
# =========================================

st.write("")

if st.button("🔍 Predict Heart Disease Risk"):

    # INPUT ARRAY

    input_data = np.array([[
        age,
        blood_pre,
        cholesterol,
        bmi,
        glucose_level
    ]])

    # SCALE INPUT

    input_scaled = scaler.transform(input_data)

    # PREDICTION

    prediction = model.predict(input_scaled)

    probability = model.predict_proba(input_scaled)

    risk_score = probability[0][1]

    # =====================================
    # RESULT CARD
    # =====================================

    st.markdown('<div class="card">', unsafe_allow_html=True)

    st.subheader("🩺 Prediction Result")

    # RESULT

    if prediction[0] == 1:
        st.error("⚠️ High Risk of Heart Disease")
    else:
        st.success("✅ Low Risk of Heart Disease")

    # =====================================
    # PROGRESS BAR
    # =====================================

    st.write("### Risk Probability")

    st.progress(float(risk_score))

    st.write(
        f"## {risk_score * 100:.2f}% Risk Probability"
    )

    # =====================================
    # RISK LEVEL
    # =====================================

    if risk_score < 0.30:
        st.success("🟢 Risk Level: LOW")

    elif risk_score < 0.70:
        st.warning("🟡 Risk Level: MEDIUM")

    else:
        st.error("🔴 Risk Level: HIGH")

    # =====================================
    # PIE CHART
    # =====================================

    chart_data = pd.DataFrame({
        "Category": ["Healthy", "Heart Disease"],
        "Value": [
            1 - risk_score,
            risk_score
        ]
    })

    fig = px.pie(
        chart_data,
        values="Value",
        names="Category",
        title="Heart Disease Analysis"
    )

    st.plotly_chart(fig, use_container_width=True)

    # =====================================
    # HEALTH SUGGESTIONS
    # =====================================

    st.subheader("💡 Health Suggestions")

    if prediction[0] == 1:

        st.warning("""
        - Consult a cardiologist immediately
        - Reduce oily food intake
        - Exercise daily
        - Maintain healthy BMI
        - Monitor blood pressure regularly
        - Reduce cholesterol intake
        - Avoid smoking and alcohol
        """)

    else:

        st.success("""
        - Maintain healthy lifestyle
        - Continue regular exercise
        - Eat balanced diet
        - Drink enough water
        - Regular health checkups
        - Maintain proper sleep schedule
        """)

    # =====================================
    # PATIENT SUMMARY
    # =====================================

    st.subheader("📋 Patient Summary")

    summary = pd.DataFrame({
        "Feature": [
            "Age",
            "Blood Pressure",
            "Cholesterol",
            "BMI",
            "Glucose Level"
        ],

        "Value": [
            age,
            blood_pre,
            cholesterol,
            bmi,
            glucose_level
        ]
    })

    st.table(summary)

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# FOOTER
# =========================================

st.write("")
st.write("---")

st.markdown("""
<center>

### ❤️ Heart Disease Prediction AI System

Made with Streamlit, Machine Learning & Artificial Intelligence

Developed by Prem Sharma

</center>
""", unsafe_allow_html=True)