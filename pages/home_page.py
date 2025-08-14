import streamlit as st

st.set_page_config(page_title="Home", layout="centered")
st.title("🏠 Home Page")

# Protect route: require login
if "access_token" not in st.session_state:
    st.warning("You must log in first.")
    st.switch_page("Login.py")

st.success("Welcome! You are logged in.")
st