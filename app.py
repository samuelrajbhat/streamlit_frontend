import streamlit as st
import requests
import os

# Load backend URL from environment variable
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Login", layout="centered")
st.title("🔐 Login")

# Input fields
username = st.text_input("Username", placeholder="username/email")
passsword = st.text_input("Password", type="password")

# Submit button
if st.button("Login", type="primary"):
    try:
        response = requests.post(
            f"{BACKEND_URL}/login",
            data={"username": username, "password":passsword},
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=5
        )
        if response.status_code == 200:
            token_data = response.json()
            st.session_state["access_token"] = token_data["access_token"]
            st.session_state["token_type"] = token_data["token_type"]
            st.success("Login Succesful!")

            st.switch_page("pages/home_page.py")
          
        elif response.status_code == 401:
            st.error("Invalid username or password.")
        else:
            st.error(f'Error: {response.status_code} - {response.text}')
    except requests.exceptions.RequestException as e:
        st.error(f"Network Error: {e}")

