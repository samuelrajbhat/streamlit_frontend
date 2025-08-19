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
    st.switch_page("app.py")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# if prompt := st.chat_input("Whats up?"):
#     st.session_state.messages.append({"role": "user", "content": prompt})
#     with st.chat_message("user"):
#         st.markdown(prompt)
        

user_input = st.chat_input("Enter your question!")
if user_input:
    with st.chat_message("user"):
        st.write(user_input)
    # st.write(f"User has sent the following prompt: {user_input}")
    with st.chat_message("assistant"):
        message_placeholder= st.empty()
        collected_text = ""
        try:
            response = requests.post(
                f"{BACKEND_URL}/ai/ask",
                json={"messages": user_input},
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
                        # st.chat_message("assistant").write(result)  # update live
            else:
                st.error(f'Error: {response.status_code} - {response.text}')

        # elif response.status_code == 401:
        #     st.error("Invalid username or password.")
        # else:
        #     st.error(f'Error: {response.status_code} - {response.text}')
        except requests.exceptions.RequestException as e:
            st.error(f"Network Error: {e}")


