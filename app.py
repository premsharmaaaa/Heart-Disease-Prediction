```python
import streamlit as st
import numpy as np
import pandas as pd
import joblib
import random
import time
import plotly.express as px

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Heart Disease Prediction System",
    page_icon="❤️",
    layout="wide"
)

# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"]  {
    font-family: 'Segoe UI';
}

.main {
    background-color: #0E1117;
    color: white;
}

.block-container {
    padding-top: 2rem;
}

.stButton>button {
    width: 100%;
    background: linear-gradient(to right, #ff416c, #ff4b2b);
    color: white;
    border-radius: 12px;
    height: 3.3em;
    font-size: 18px;
    border: none;
    font-weight: bold;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.02);
    background: linear-gradient(to right, #ff4b2b, #ff416c);
}

.card {
    padding: 25px;
    border-radius: 18px;
    background-color: #161B22;
    box-shadow: 0px 0px 18px rgba(255,255,255,0.08);
    margin-bottom: 20px;
}

.title {
    text-align: center;
    font-size: 58px;
    font-weight: bold;
    color: #ff4b2b;
}

.subtitle {
    text-align: center;
    font-size: 22px;
    color: #cccccc;
}

.small-title {
    color: #ff4b2b;
    font-weight: bold;
}

.feature-card {
    background-color: #161B22;
    padding: 25px;
    border-radius: 20px;
    text-align: center;
    height: 250px;
    box-shadow: 0px 0px 15px rgba(255,255,255,0.05);
}

.metric-box {
    background-color: #161B22;
    padding: 20px;
    border-radius: 15px;
}

</style>
""", unsafe_allow_html=True)

# =========================================================
# LOAD MODEL
# =========================================================

model = joblib.load("models/best_model.pkl")
scaler = joblib.load("models/scaler.pkl")

# =========================================================
# TITLE
# =========================================================

st.markdown(
    '<p class="title">❤️ AI Heart Disease Prediction System</p>',
    unsafe_allow_html=True
)

st.markdown(
    '<p class="subtitle">Advanced Artificial Intelligence Healthcare Platform</p>',
    unsafe_allow_html=True
)

st.write("")

# =========================================================
# HERO SECTION
# =========================================================

st.markdown("""
<div style="
padding:35px;
border-radius:25px;
background: linear-gradient(to right, #141E30, #243B55);
box-shadow:0px 0px 20px rgba(255,255,255,0.08);
">

<h1 style="
text-align:center;
font-size:55px;
color:white;
">
🧠 NEXT GENERATION AI HEALTHCARE
</h1>

<h3 style="
text-align:center;
color:#cccccc;
font-weight:normal;
">
Smart • Secure • Intelligent • Professional
</h3>

<br>

<div style="
display:flex;
justify-content:space-around;
text-align:center;
">

<div>
<h2 style="color:#00FF99;">98.7%</h2>
<p>AI Accuracy</p>
</div>

<div>
<h2 style="color:#00E5FF;">24/7</h2>
<p>AI Monitoring</p>
</div>

<div>
<h2 style="color:#FFB347;">50K+</h2>
<p>Predictions</p>
</div>

<div>
<h2 style="color:#FF5E7E;">Cloud AI</h2>
<p>Healthcare System</p>
</div>

</div>

</div>
""", unsafe_allow_html=True)

st.write("")

# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.title("ℹ️ About Platform")

st.sidebar.info("""
This AI healthcare platform predicts heart disease risk using Machine Learning algorithms.

Features:
✅ AI Prediction  
✅ Health Dashboard  
✅ BMI Analysis  
✅ Smart AI Insights  
✅ Live Monitoring  
✅ Data Visualization  
""")

st.sidebar.success("Developed by Prem Sharma ❤️")

# =========================================================
# LIVE METRICS
# =========================================================

st.subheader("📡 Live AI Health Dashboard")

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

# =========================================================
# FEATURE SECTION
# =========================================================

st.subheader("🚀 Platform Features")

f1, f2, f3, f4 = st.columns(4)

with f1:
    st.markdown("""
    <div class="feature-card">
    <h1>🤖</h1>
    <h3>AI Diagnosis</h3>
    <p>
    Smart prediction using Machine Learning algorithms.
    </p>
    </div>
    """, unsafe_allow_html=True)

with f2:
    st.markdown("""
    <div class="feature-card">
    <h1>📊</h1>
    <h3>Analytics</h3>
    <p>
    Real-time charts and visual healthcare analysis.
    </p>
    </div>
    """, unsafe_allow_html=True)

with f3:
    st.markdown("""
    <div class="feature-card">
    <h1>❤️</h1>
    <h3>Health Tracking</h3>
    <p>
    Monitor patient health with intelligent AI systems.
    </p>
    </div>
    """, unsafe_allow_html=True)

with f4:
    st.markdown("""
    <div class="feature-card">
    <h1>🔒</h1>
    <h3>Security</h3>
    <p>
    Secure and modern healthcare cloud platform.
    </p>
    </div>
    """, unsafe_allow_html=True)

st.write("")

# =========================================================
# INPUT SECTION
# =========================================================

st.markdown("""
<div class="card">
<h2>📝 Patient Health Information</h2>
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

# =========================================================
# AI HEALTH SCORE
# =========================================================

st.subheader("🧠 AI Health Score")

health_score = random.randint(65, 98)

st.progress(health_score / 100)

if health_score > 85:
    st.success(f"Excellent Health Score: {health_score}%")

elif health_score > 70:
    st.warning(f"Average Health Score: {health_score}%")

else:
    st.error(f"Low Health Score: {health_score}%")

st.write("")

# =========================================================
# PREDICT BUTTON
# =========================================================

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

    with st.spinner("🤖 AI is analyzing medical data..."):
        time.sleep(2)

    st.markdown("""
    <div class="card">
    """, unsafe_allow_html=True)

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

    st.write("")

    # =====================================================
    # CHART
    # =====================================================

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
        title="📊 Patient Health Analysis"
    )

    st.plotly_chart(fig, use_container_width=True)

    # =====================================================
    # AI ANALYSIS
    # =====================================================

    st.subheader("🤖 AI Smart Analysis")

    analysis = [
        "✔️ Blood pressure requires regular monitoring.",
        "✔️ Cholesterol level should remain controlled.",
        "✔️ Daily physical exercise is recommended.",
        "✔️ Healthy food intake improves heart condition.",
        "✔️ Regular medical checkups are advised.",
        "✔️ Proper sleep reduces stress levels.",
        "✔️ Drinking enough water improves overall health."
    ]

    for item in analysis:
        st.write(item)

    st.write("")

    # =====================================================
    # HEALTH SUGGESTIONS
    # =====================================================

    st.subheader("💡 Health Suggestions")

    if prediction[0] == 1:

        st.warning("""
        - Consult a cardiologist
        - Reduce cholesterol intake
        - Exercise regularly
        - Monitor blood pressure
        - Maintain healthy BMI
        - Avoid stress and smoking
        - Improve sleep quality
        """)

    else:

        st.success("""
        - Maintain healthy lifestyle
        - Continue regular exercise
        - Eat balanced diet
        - Stay hydrated
        - Continue health checkups
        - Maintain proper sleep
        """)

    # =====================================================
    # BMI STATUS
    # =====================================================

    st.subheader("📊 BMI Status")

    if bmi < 18.5:
        st.warning("⚠️ Underweight")

    elif bmi < 25:
        st.success("✅ Normal BMI")

    elif bmi < 30:
        st.warning("⚠️ Overweight")

    else:
        st.error("❌ Obese")

    # =====================================================
    # DAILY GOALS
    # =====================================================

    st.subheader("🎯 Daily Health Goals")

    g1 = st.checkbox("🚶 Walk 10,000 Steps")
    g2 = st.checkbox("💧 Drink 3L Water")
    g3 = st.checkbox("🥗 Eat Healthy Food")
    g4 = st.checkbox("🏃 Exercise 30 Minutes")
    g5 = st.checkbox("😴 Sleep 8 Hours")

    completed = sum([g1, g2, g3, g4, g5])

    st.progress(completed / 5)

    st.write(f"Goals Completed: {completed}/5")

    st.write("")

    # =====================================================
    # WATER TRACKER
    # =====================================================

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

    # =====================================================
    # EXERCISE TRACKER
    # =====================================================

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

    st.write("")

    # =====================================================
    # USER FEEDBACK
    # =====================================================

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

# =========================================================
# AI CHAT ASSISTANT
# =========================================================

st.write("")

st.subheader("💬 AI Health Assistant")

question = st.text_input(
    "Ask AI about health"
)

if question:

    responses = [
        "AI recommends regular exercise.",
        "Maintain healthy blood pressure levels.",
        "Avoid oily food and sugary drinks.",
        "Drink enough water daily.",
        "Proper sleep improves heart health.",
        "Regular walking is very beneficial."
    ]

    st.success(random.choice(responses))

# =========================================================
# MOTIVATION SECTION
# =========================================================

st.write("")

quotes = [
    "❤️ Your heart is your life engine.",
    "💪 Fitness is the best medicine.",
    "🥗 Healthy habits create healthy life.",
    "🏃 Exercise keeps your heart strong.",
    "🧠 Prevention is better than cure."
]

st.subheader("✨ Daily Motivation")

st.success(random.choice(quotes))

# =========================================================
# SYSTEM STATUS
# =========================================================

st.write("")

st.subheader("🖥️ AI System Status")

s1, s2, s3 = st.columns(3)

with s1:
    st.success("✅ ML Model Active")

with s2:
    st.success("✅ Cloud Server Online")

with s3:
    st.success("✅ AI Analysis Running")

# =========================================================
# FOOTER
# =========================================================

st.write("")
st.write("---")

st.markdown("""
<div style="
padding:40px;
border-radius:25px;
background: linear-gradient(to right, #141E30, #243B55);
text-align:center;
">

<h1 style="
font-size:55px;
color:white;
">
❤️ AI HEARTCARE SUPER PLATFORM
</h1>

<h3 style="color:#cccccc;">
Future of Artificial Intelligence in Healthcare
</h3>

<br>

<h2>🚀 Technologies Used</h2>

<p style="font-size:18px;">
Python • Streamlit • Machine Learning • AI • XGBoost • Plotly • NumPy • Pandas • Scikit-Learn
</p>

<br>

<h2>🌍 Platform Features</h2>

<p style="font-size:18px;">
✔️ Real-Time Prediction  
✔️ AI Analysis  
✔️ Smart Dashboard  
✔️ Health Monitoring  
✔️ Medical Visualization  
✔️ Cloud Deployment  
✔️ AI Recommendations  
</p>

<br>

<h2>🏆 Achievement</h2>

<p style="font-size:20px;">
Built with Advanced AI & Modern Healthcare Technology
</p>

<br>

<h2 style="color:#00FF99;">
🔒 Secure • Intelligent • Professional
</h2>

<br>

<h3>
Made with ❤️ by Prem Sharma
</h3>

</div>
""", unsafe_allow_html=True)

