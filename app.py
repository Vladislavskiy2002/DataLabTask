import threading
from typing import List

import schedule
import streamlit as st
import random
import time

import requests

st.title("COFFEE SHOt")

st.sidebar.success("Select a demo above.")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

flag = False
# with st.chat_message("assistant"):
#     dat = requests.get("http://127.0.0.1:8000/startprogram").json()
#     if dat == "Welcome at the coffee shoP What would you like?":
#         st.write(dat)
#         st.session_state.messages.append({"role": "assistant", "content": dat})
# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        # schedule.clear()
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        data = requests.get("http://127.0.0.1:8000/handler/" + prompt.__str__()).json()
        st.write(data)
        st.session_state.messages.append({"role": "assistant", "content": data})
    #     assistant_response = random.choice(
    #         [
    #                 "Hello there! How can I assist you today?",
    #                 "Hi, human! Is there anything I can help you with?",
    #                 "Do you need help?",
    #         ]
    #         )
    #     # Simulate stream of response with milliseconds delay
    #     for chunk in assistant_response.split():
    #         full_response += chunk + " "
    #         time.sleep(0.05)
    #         # Add a blinking cursor to simulate typing
    #         message_placeholder.markdown(full_response + "")
    #     message_placeholder.markdown(full_response)
    # # Add assistant response to chat history
    # st.session_state.messages.append({"role": "assistant", "content": full_response})