import streamlit as st
import pyrebase

# 🔐 Firebase config from secrets.toml
firebaseConfig = {
    "apiKey": st.secrets["API_KEY"],
    "authDomain": st.secrets["AUTH_DOMAIN"],
    "projectId": st.secrets["PROJECT_ID"],
    "storageBucket": st.secrets["STORAGE_BUCKET"],
    "messagingSenderId": st.secrets["MESSAGING_SENDER_ID"],
    "appId": st.secrets["APP_ID"],
    "databaseURL": st.secrets["DATABASE_URL"]
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

def is_authenticated():
    return "user" in st.session_state and st.session_state.user is not None

def login_ui():
    with st.expander("🔐 Login", expanded=True):
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login"):
            try:
                user = auth.sign_in_with_email_and_password(email, password)
                st.session_state.user = user
                st.success("Logged in successfully!")
                st.rerun()  # rerun immediately, so error below won't show
            except Exception:
                st.error("Login failed. Please check your credentials.")


def signup_ui():
    with st.expander("🆕 Sign Up"):
        email = st.text_input("Email", key="signup_email")
        password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Sign Up"):
            try:
                user = auth.create_user_with_email_and_password(email, password)
                st.success("Account created successfully! You can now log in.")
            except Exception as e:
                st.error("Signup failed. Please try again.")
