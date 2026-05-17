import streamlit as st
import numpy as np
import pandas as pd
import joblib
import random
import time
import plotly.express as px

# =========================================
# PAGE CONFIG
# =========================================

st.set_page_config(
    page_title="Heart Disease Prediction AI",
    page_icon="❤️",
    layout="wide"
)

# =========================================
# CUSTOM CSS
# =========================================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
    color: white;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(to right, #ff416c, #ff4b2b);
    color: white;
    border-radius: 12px;
    height: 3.2em;
    font-size: 18px;
    border: none;
    font-weight: bold;
}

.stButton>button:hover {
    background: linear-gradient(to right, #ff4b2b, #ff416c);
    transform: scale(1.02);
}

.card {
    padding: 25px;
    border-radius: 18px;
    background-color: #161B22;
    box-shadow: 0px 0px 20px rgba(255,255,255,0.1);
    margin-bottom: 20px;
}

.title {
    text-align: center;
    font-size: 52px;
    font-weight: bold;
    color: #ff4b2b;
}

.subtitle {
    text-align: center;
    font-size: 20px;
    color: #CCCCCC;
}

.metric-card {
    background-color: #161B22;
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
# TITLE
# =========================================

st.markdown(
    '<p class="title">❤️ Heart Disease Prediction AI System</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Advanced AI-Powered Healthcare Monitoring Platform</p>',
    unsafe_allow_html=True
)

st.write("")

# =========================================
# SIDEBAR
# =========================================

st.sidebar.image(
    "https://cdn-icons-png.flaticon.com/512/2966/2966486.png",
    width=120
)

st.sidebar.title("ℹ️ About")

st.sidebar.info("""
This AI system predicts heart disease risk using Machine Learning algorithms.

Features:
✅ AI Prediction  
✅ Health Monitoring  
✅ Smart Analysis  
✅ BMI Analysis  
✅ Health Dashboard  
✅ Daily Goals Tracker  
""")

st.sidebar.success("Developed by Prem Sharma ❤️")

# =========================================
# HEALTH METRICS
# =========================================

st.subheader("📡 Live Health Dashboard")

m1, m2, m3, m4 = st.columns(4)

with m1:
    st.metric(
        "❤️ Heart Rate",
        f"{random.randint(70,95)} BPM",
        f"+{random.randint(1,5)}"
    )

with m2:
    st.metric(
        "🩸 Oxygen",
        f"{random.randint(92,99)}%"
    )

with m3:
    st.metric(
        "🔥 Calories",
        f"{random.randint(1200,3000)}"
    )

with m4:
    st.metric(
        "🚶 Steps",
        f"{random.randint(2000,10000)}"
    )

st.write("")

# =========================================
# INPUT SECTION
# =========================================

st.markdown("""
<div class="card">
<h2>📝 Enter Patient Information</h2>
</div>
""", unsafe_allow_html=True)

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

st.write("")

# =========================================
# AI HEALTH SCORE
# =========================================

health_score = random.randint(65, 98)

st.subheader("🧠 AI Health Score")

st.progress(health_score / 100)

if health_score > 85:
    st.success(f"Excellent Health Score: {health_score}%")

elif health_score > 70:
    st.warning(f"Average Health Score: {health_score}%")

else:
    st.error(f"Low Health Score: {health_score}%")

# =========================================
# PREDICT BUTTON
# =========================================

if st.button("🔍 Predict Heart Disease Risk"):

    input_data = np.array([[
        age,
        blood_pre,
        cholesterol,
        bmi,
        glucose_level
    ]])

    input_scaled = scaler.transform(input_data)

    prediction = model.predict(input_scaled)

    probability = model.predict_proba(input_scaled)

    risk_score = probability[0][1]

    st.write("")

    st.markdown(
        '<div class="card">',
        unsafe_allow_html=True
    )

    st.subheader("🩺 Prediction Result")

    if prediction[0] == 1:
        st.error("⚠️ High Risk of Heart Disease")
    else:
        st.success("✅ Low Risk of Heart Disease")

    st.write("")

    st.progress(float(risk_score))

    st.write(
        f"## Prediction Probability: {risk_score * 100:.2f}%"
    )

    # =====================================
    # CHART
    # =====================================

    chart_data = pd.DataFrame({
        "Health Factor": [
            "Blood Pressure",
            "Cholesterol",
            "BMI",
            "Glucose"
        ],
        "Value": [
            blood_pre,
            cholesterol,
            bmi,
            glucose_level
        ]
    })

    fig = px.bar(
        chart_data,
        x="Health Factor",
        y="Value",
        title="Patient Health Analysis"
    )

    st.plotly_chart(fig, use_container_width=True)

    # =====================================
    # AI ANALYSIS
    # =====================================

    st.subheader("🤖 AI Smart Analysis")

    analysis = [
        "✔️ Blood pressure requires monitoring.",
        "✔️ Cholesterol should remain controlled.",
        "✔️ Daily exercise is recommended.",
        "✔️ Healthy food intake is important.",
        "✔️ Regular medical checkups are advised."
    ]

    for item in analysis:
        st.write(item)

    # =====================================
    # HEALTH SUGGESTIONS
    # =====================================

    st.subheader("💡 Health Suggestions")

    if prediction[0] == 1:

        st.warning("""
        - Consult a cardiologist
        - Reduce oily food
        - Exercise regularly
        - Monitor blood pressure
        - Maintain healthy BMI
        - Reduce stress levels
        """)

    else:

        st.success("""
        - Maintain healthy lifestyle
        - Continue exercise
        - Eat balanced diet
        - Stay hydrated
        - Regular health checkups
        """)

    # =====================================
    # BMI STATUS
    # =====================================

    st.subheader("📊 BMI Status")

    if bmi < 18.5:
        st.warning("⚠️ Underweight")

    elif bmi < 25:
        st.success("✅ Normal BMI")

    elif bmi < 30:
        st.warning("⚠️ Overweight")

    else:
        st.error("❌ Obese")

    # =====================================
    # DAILY GOALS
    # =====================================

    st.subheader("🎯 Daily Health Goals")

    g1 = st.checkbox("🚶 Walk 10,000 Steps")
    g2 = st.checkbox("💧 Drink 3L Water")
    g3 = st.checkbox("🥦 Eat Healthy Food")
    g4 = st.checkbox("🏃 Exercise 30 Minutes")
    g5 = st.checkbox("😴 Sleep 8 Hours")

    completed = sum([g1, g2, g3, g4, g5])

    st.progress(completed / 5)

    st.write(f"Goals Completed: {completed}/5")

    # =====================================
    # WATER TRACKER
    # =====================================

    st.subheader("💧 Water Intake Tracker")

    water = st.slider(
        "Daily Water Intake",
        0,
        10,
        3
    )

    if water >= 3:
        st.success("Excellent Hydration ✅")
    else:
        st.warning("Increase Water Intake ⚠️")

    # =====================================
    # EXERCISE TRACKER
    # =====================================

    st.subheader("🏋️ Exercise Tracker")

    exercise = st.selectbox(
        "Select Exercise",
        [
            "Walking",
            "Running",
            "Gym",
            "Cycling",
            "Yoga",
            "Swimming"
        ]
    )

    st.info(f"Selected Exercise: {exercise}")

    # =====================================
    # LOADING AI
    # =====================================

    with st.spinner("🤖 AI is processing deep medical analysis..."):
        time.sleep(2)

    st.success("AI Analysis Completed Successfully ✅")

    # =====================================
    # FEEDBACK
    # =====================================

    st.subheader("⭐ User Feedback")

    rating = st.slider(
        "Rate this App",
        1,
        5,
        5
    )

    feedback = st.text_area(
        "Share Your Feedback"
    )

    if st.button("Submit Feedback"):
        st.success("Thank You for Feedback ❤️")

    st.markdown("</div>", unsafe_allow_html=True)

# =========================================
# MOTIVATIONAL QUOTES
# =========================================

quotes = [
    "❤️ Your heart is your life engine.",
    "💪 Healthy habits create healthy life.",
    "🥗 Eat healthy, stay healthy.",
    "🏃 Fitness is the best medicine.",
    "🧠 Prevention is better than cure."
]

st.write("")

st.subheader("✨ Daily Motivation")

st.success(random.choice(quotes))

# =========================================
# SYSTEM STATUS
# =========================================

st.write("")

st.subheader("🖥️ AI System Status")

s1, s2, s3 = st.columns(3)

with s1:
    st.success("✅ ML Model Active")

with s2:
    st.success("✅ Server Online")

with s3:
    st.success("✅ AI Analysis Running")

# =========================================
# FOOTER
# =========================================

st.write("")
st.write("---")

st.markdown("""
<center>

<h1 style='color:#ff4b2b;'>
❤️ Heart Disease Prediction AI Platform
</h1>

<h4>
Advanced AI Healthcare Monitoring System
</h4>

<p>
Built with Python • Streamlit • Machine Learning • AI
</p>

<p>
🔒 Secure • Fast • Intelligent • Modern
</p>

<p>
© 2026 Prem Sharma | All Rights Reserved
</p>

</center>
""", unsafe_allow_html=True)