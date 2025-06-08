import streamlit as st
import pickle
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import datetime
from database import add_daily_log, get_user_logs, get_average_inputs
from utils.session import check_authentication
check_authentication()

# Load model
model = pickle.load(open("pcos_model.pkl", "rb"))

# Streamlit configuration
st.set_page_config(page_title="Daily Health Entry", layout="wide")


# 3D-style CSS
st.markdown("""
    <style>
    body {
        background-color: #f9fbff;
    }
    .card-style {
        background: linear-gradient(145deg, #ffffff, #e6e6e6);
        box-shadow: 10px 10px 20px #d1d9e6, -10px -10px 20px #ffffff;
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
    }
    .header-font {
        font-size: 36px;
        font-weight: 700;
        color: #333;
        margin-bottom: 10px;
    }
    .sub-font {
        font-size: 18px;
        color: #666;
    }
    .metric-header {
        font-size: 20px;
        font-weight: bold;
        color: #0066cc;
        margin-top: 20px;
    }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown('<div class="header-font">📝 Daily Health Entry</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-font">Please fill in your daily health data to monitor PCOS symptoms over time.</div>', unsafe_allow_html=True)

# 🟡 Authentication Check
# 🔹 Entry Form
st.markdown("---")
st.markdown('<div class="card-style">', unsafe_allow_html=True)
st.header("🩺 Today's Health Details")

col1, col2 = st.columns(2)
with col1:
    Age = st.number_input("Age (years)", 10, 60)
    Weight = st.number_input("Weight (kg)", 30.0, 150.0)
    Height = st.number_input("Height (cm)", 120.0, 200.0)
    Cycle_R_I = st.radio("Cycle Type", ["Regular", "Irregular"])
    Cycle_R_I = 1 if Cycle_R_I == "Regular" else 0
    Cycle_length_days = st.slider("Cycle Length (days)", 0, 60)

with col2:
    Marriage_Status_Yrs = st.slider("Years Since Marriage", 0, 40)
    Pregnant_Y_N = 1 if st.radio("Ever been pregnant?", ["No", "Yes"]) == "Yes" else 0
    Hip = st.number_input("Hip (inches)", 20.0, 60.0)
    Waist = st.number_input("Waist (inches)", 20.0, 60.0)
    Waist_Hip = Waist / Hip if Hip != 0 else 0

# Yes/No fields
def yn_radio(label):
    return 1 if st.radio(label, ["No", "Yes"]) == "Yes" else 0

Weight_gain = yn_radio("Weight gain?")
Hair_growth = yn_radio("Hair growth?")
Skin_darkening = yn_radio("Skin darkening?")
Hair_loss = yn_radio("Hair loss?")
Pimples = yn_radio("Pimples?")
Fast_food = yn_radio("Frequent fast food?")
Reg_exercise = yn_radio("Regular exercise?")
Irregular_periods = yn_radio("Irregular Periods?")

# ✅ Submit Data
if st.button("📥 Submit Today’s Entry"):
    BMI = Weight / ((Height / 100) ** 2)
    data = [
        Age, Weight, Height, BMI, Cycle_R_I, Cycle_length_days,
        Marriage_Status_Yrs, Pregnant_Y_N, Hip, Waist, Waist_Hip,
        Weight_gain, Hair_growth, Skin_darkening, Hair_loss,
        Pimples, Fast_food, Reg_exercise, Irregular_periods
    ]
    add_daily_log(st.session_state["user_id"], data)
    st.session_state["log_submitted_today"] = True
    st.success("✅ Data submitted successfully!")

st.markdown("</div>", unsafe_allow_html=True)  # Close card-style

# 🛎️ Check if today's log exists
logs = get_user_logs(st.session_state["user_id"])
today = datetime.date.today()
logged_today = any(datetime.datetime.strptime(row[0], "%Y-%m-%d").date() == today for row in logs)

if not logged_today:
    st.warning("🔔 You haven’t submitted today’s log yet.")

# 🔍 PCOS Prediction
st.markdown("---")
st.header("🔍 PCOS Risk Prediction")
st.markdown("Click below to predict based on your **average** logged data.")

if st.button("⚡ Predict from My Average Data"):
    avg_data = get_average_inputs(st.session_state["user_id"])
    if None in avg_data:
        st.warning("❗ Please log at least once to generate prediction.")
    else:
        prediction = model.predict(np.array(avg_data).reshape(1, -1))[0]
        confidence = model.predict_proba(np.array(avg_data).reshape(1, -1))[0][prediction]
        if prediction == 1:
            st.error(f"⚠️ You are likely at risk for PCOS.\n\n🧠 Confidence: {confidence:.2f}")
        else:
            st.success(f"✅ You are not likely at risk for PCOS.\n\n🧠 Confidence: {confidence:.2f}")

# 📊 Graphs
st.markdown("---")
st.header("📊 Health Progress Over Time")

if logs:
    df = pd.DataFrame(logs, columns=[
        "Date", "Age", "Weight", "Height", "BMI", "Cycle_R_I", "Cycle_length_days",
        "Marriage_Status_Yrs", "Pregnant_Y_N", "Hip", "Waist", "Waist_Hip_Ratio",
        "Weight_gain_Y_N", "Hair_growth_Y_N", "Skin_darkening_Y_N", "Hair_loss_Y_N",
        "Pimples_Y_N", "Fast_food_Y_N", "Reg_Exercise_Y_N", "Irregular_Periods"
    ])
    df["Date"] = pd.to_datetime(df["Date"])
    df.set_index("Date", inplace=True)

    st.markdown('<div class="metric-header">📈 Choose a metric to view:</div>', unsafe_allow_html=True)
    metric = st.selectbox("", ["Weight", "BMI", "Cycle_length_days", "Waist_Hip_Ratio"])

    fig, ax = plt.subplots(figsize=(10, 5))
    df[metric].plot(ax=ax, marker="o", linestyle="-", color="teal")
    ax.set_title(f"{metric} Over Time", fontsize=16)
    ax.set_ylabel(metric, fontsize=14)
    ax.set_xlabel("Date", fontsize=14)
    st.pyplot(fig)
else:
    st.info("Start logging to view trends over time.")
