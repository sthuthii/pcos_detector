import streamlit as st
from utils.auth import login_ui, signup_ui, is_authenticated

from database import initialize_database
initialize_database()

# ✅ Set page config (Streamlit doesn't allow multiple calls)
if "page_configured" not in st.session_state:
    st.set_page_config(page_title="PCOS Tracker", layout="centered", initial_sidebar_state="collapsed")
    st.session_state.page_configured = True

# ✅ Show login/signup UI if not authenticated
if not is_authenticated():
    login_ui()
    signup_ui()
    st.stop()

# ✅ Authenticated: Show Home Page
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

# ✅ Logout Button
if st.button("🚪 Logout"):
    st.session_state.clear()
    st.success("Logged out successfully.")
    st.rerun()
