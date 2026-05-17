import streamlit as st
import numpy as np
import joblib

# ==============================
# PAGE CONFIG
# ==============================

st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="wide"
)

# ==============================
# CUSTOM CSS
# ==============================

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
    border-radius: 10px;
    height: 3em;
    font-size: 18px;
    border: none;
}

.stButton>button:hover {
    background: linear-gradient(to right, #ff4b2b, #ff416c);
    color: white;
}

.card {
    padding: 25px;
    border-radius: 15px;
    background-color: #161B22;
    box-shadow: 0px 0px 15px rgba(255,255,255,0.1);
    margin-bottom: 20px;
}

.title {
    text-align: center;
    font-size: 45px;
    font-weight: bold;
    color: #ff4b2b;
}

.subtitle {
    text-align: center;
    font-size: 18px;
    color: #cfcfcf;
}

</style>
""", unsafe_allow_html=True)

# ==============================
# LOAD MODEL
# ==============================

model = joblib.load("models/best_model.pkl")
scaler = joblib.load("models/scaler.pkl")

# ==============================
# TITLE
# ==============================

st.markdown('<p class="title">❤️ Heart Disease Prediction System</p>', unsafe_allow_html=True)

st.markdown(
    '<p class="subtitle">AI-powered system to predict heart disease risk</p>',
    unsafe_allow_html=True
)

st.write("")

# ==============================
# SIDEBAR
# ==============================

st.sidebar.header("ℹ️ About")

st.sidebar.info(
    """
    This application predicts heart disease risk using Machine Learning.

    Enter patient details and click Predict.
    """
)

st.sidebar.success("Developed by Prem ❤️")

# ==============================
# INPUT SECTION
# ==============================

col1, col2 = st.columns(2)

with col1:
    age = st.slider("Age", 1, 120, 30)

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

# ==============================
# PREDICT BUTTON
# ==============================

if st.button("🔍 Predict Heart Disease Risk"):

    input_data = np.array([[
        age,
        blood_pre,
        cholesterol,
        bmi,
        glucose_level
    ]])

    # Scale data
    input_scaled = scaler.transform(input_data)

    # Prediction
    prediction = model.predict(input_scaled)

    # Probability
    probability = model.predict_proba(input_scaled)

    risk_score = probability[0][1]

    st.write("")

    # ==========================
    # RESULT CARD
    # ==========================

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

    # Probability bar
    st.progress(float(risk_score))

    st.write(
        f"### Prediction Probability: {risk_score * 100:.2f}%"
    )

    # Health suggestions
    st.write("")

    st.subheader("💡 Health Suggestions")

    if prediction[0] == 1:
        st.warning("""
        - Consult a cardiologist
        - Reduce cholesterol intake
        - Exercise regularly
        - Monitor blood pressure
        - Maintain healthy BMI
        """)
    else:
        st.success("""
        - Maintain healthy lifestyle
        - Continue regular exercise
        - Eat balanced diet
        - Regular health checkups
        """)

    st.markdown("</div>", unsafe_allow_html=True)

# ==============================
# FOOTER
# ==============================

st.write("")
st.write("---")

st.markdown(
    """
    <center>
    Made with ❤️ using Streamlit & Machine Learning
    </center>
    """,
    unsafe_allow_html=True
)