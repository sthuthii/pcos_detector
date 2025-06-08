import streamlit as st

def check_authentication():
    if "user_id" not in st.session_state or not st.session_state.get("logged_in", False):
        st.warning("You are not logged in. Please log in first.")
        st.stop()
