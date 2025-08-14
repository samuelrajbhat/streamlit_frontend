import streamlit as st

st.set_page_config(page_title="Home Page", layout="centered")

st.title("🏠 Home Page")

st.write(st.session_state.get("access_token")) # type: ignore