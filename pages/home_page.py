import streamlit as st
import os
import requests

# Load backend URL from environment variable
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Home", layout="centered")
st.title("🏠 Home Page")

# Protect route: require login
if "access_token" not in st.session_state:
    st.warning("You must log in first.")
    st.switch_page("Login.py")

st.success("Welcome! You are logged in.")
user_input = st.chat_input("Enter your question!")
if user_input:
    try:
        response = requests.post(
            f"{BACKEND_URL}/ai/ask",
            json={"messages": user_input},
            headers={"Content-Type": "application/json",
                     "Authorization": f"Bearer {st.session_state['access_token']}"},
            timeout=5,
            stream=True
        )
        if response.status_code == 200:
            result = ""
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    result += chunk.decode()
                    st.chat_message("assistant").write(result)  # update live
        else:
            st.error(f'Error: {response.status_code} - {response.text}')

        # elif response.status_code == 401:
        #     st.error("Invalid username or password.")
        # else:
        #     st.error(f'Error: {response.status_code} - {response.text}')
    except requests.exceptions.RequestException as e:
        st.error(f"Network Error: {e}")


