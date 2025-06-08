import streamlit as st
from utils.auth import login_ui, signup_ui, is_authenticated

# Set page config (only once!)
if not is_authenticated():
    st.set_page_config(page_title="Login", layout="centered", initial_sidebar_state="collapsed")
else:
    st.set_page_config(page_title="Home", layout="centered")

# Show login/signup only if not logged in
if not is_authenticated():
    login_ui()
    signup_ui()
    st.stop()

# 🏠 Main page content if authenticated
st.markdown("""
    <h1 style='text-align: center; color: #d81b60;'>Welcome to Your PCOS Tracker 🌸</h1>
    <p style='text-align: center; font-size: 18px;'>Your cozy space to log, track & predict your health 🧘‍♀️💖</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### ✍️ Start Logging")
    st.info("Head over to the **Daily Log** page and input your health stats for today!")

with col2:
    st.markdown("#### 🔮 Predict PCOS Risk")
    st.success("Check your PCOS risk using your average health data.")

st.markdown("""
<hr>
<h4 style='color:#6a1b9a;'>💡 Tip of the Day</h4>
<p style='color:#4a148c;'>Drink enough water and get 7-8 hours of sleep to improve hormonal balance 💧🌙</p>
""", unsafe_allow_html=True)

# Logout button
if st.button("Logout"):
    st.session_state.user = None
    st.success("Logged out successfully.")
    st.experimental_rerun()
