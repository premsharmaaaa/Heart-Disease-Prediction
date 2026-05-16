import streamlit as st
import numpy as np
import joblib

# LOAD MODEL & SCALER

model = joblib.load("models/best_model.pkl")
scaler = joblib.load("models/scaler.pkl")


# PAGE TITLE

st.set_page_config(
    page_title="Heart Disease Prediction",
    page_icon="❤️",
    layout="centered"
)

st.title(" Heart Disease Prediction System")

st.write("Enter patient details belostreamlitw to predict heart disease risk.")

# USER INPUTS

age = st.number_input("Age", 1, 120, 30)

blood_pre = st.number_input("Blood Pressure", 50.0, 250.0, 120.0)

cholesterol = st.number_input("Cholesterol", 50.0, 500.0, 200.0)

bmi = st.number_input("BMI", 10.0, 60.0, 25.0)

glucose_level = st.number_input("Glucose Level", 20.0, 400.0, 100.0)


# PREDICTION BUTTON


if st.button("Predict"):

    # Create input array
    input_data = np.array([[
        age,
        blood_pre,
        cholesterol,
        bmi,
        glucose_level
    ]])

    # Scale input
    input_scaled = scaler.transform(input_data)

    # Prediction
    prediction = model.predict(input_scaled)

    # Probability
    probability = model.predict_proba(input_scaled)

    # ==============================
    # OUTPUT
    # ==============================

    st.subheader("Prediction Result")

    if prediction[0] == 1:
        st.error("⚠️ High Risk of Heart Disease")
    else:
        st.success("✅ Low Risk of Heart Disease")

    st.write(f"Prediction Probability: {probability[0][1]:.2f}")

    