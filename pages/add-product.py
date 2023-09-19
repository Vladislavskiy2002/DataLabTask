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
        data = requests.get("http://127.0.0.1:8000/admin/handler/" + prompt.__str__()).json()
        st.write(data)
        st.session_state.messages.append({"role": "assistant", "content": data})