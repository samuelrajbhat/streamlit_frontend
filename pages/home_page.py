import streamlit as st
import os
import requests
import pandas as pd
import json

# Load backend URL from environment variable
BACKEND_URL = os.getenv("BACKEND_URL", "http://127.0.0.1:8000")

st.set_page_config(page_title="Home", layout="centered")
st.title("🏠 Home Page")

# Protect route: require login
if "access_token" not in st.session_state:
    st.warning("You must log in first.")
    st.switch_page("app.py")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Whats up?"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        

# user_input = st.chat_input("Enter your question!")
# if user_input:
    # with st.chat_message("user"):
    #     st.write(user_input)
    # st.write(f"User has sent the following prompt: {user_input}")
    with st.chat_message("assistant"):
        message_placeholder= st.empty()
        collected_text = ""
        try:
            response = requests.post(
                f"{BACKEND_URL}/ai/ask",
                json={"messages": prompt},
                headers={"Content-Type": "application/json",
                        "Authorization": f"Bearer {st.session_state['access_token']}"},
                timeout=30,
                stream=True
            )
            
        
            if response.status_code == 200:
                
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        collected_text += chunk.decode()
                        message_placeholder.markdown(collected_text)
                # Save assistant message in history
                # check if  its a table to respond it
                try:
                    data= json.loads(collected_text)
                    if isinstance(data, list) and all(isinstance(i, dict) for i in data):
                        df = pd.DataFrame(data)
                        message_placeholder.dataframe(df)
                        collected_text= df.to_markdown()
                except Exception:
                    pass
                st.session_state.messages.append({"role": "assistant", "content": collected_text})
            else:
                st.error(f'Error: {response.status_code} - {response.text}')

        # elif response.status_code == 401:
        #     st.error("Invalid username or password.")
        # else:
        #     st.error(f'Error: {response.status_code} - {response.text}')
        except requests.exceptions.RequestException as e:
            st.error(f"Network Error: {e}")


