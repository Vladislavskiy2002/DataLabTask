import threading
from typing import List

import schedule
import streamlit as st
import random
import time

import requests

st.title("ADD PRODUCT ADMIN PANEL")

st.sidebar.success("WoWf-WoWf")


# Initialize chat history
if "adminMessages" not in st.session_state:
    st.session_state.adminMessages = []
#
# if not st.session_state.messages:
#     with st.chat_message("assistant"):
#         st.write("Welcome, enter the type of product:")

# Display chat messages from history on app rerun
for message in st.session_state.adminMessages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.adminMessages == []:
    with st.chat_message("assistant"):
        requests.get("http://127.0.0.1:8000/admin/setToDefault").json()
        st.write("Welcome, enter the type of product:")
        st.session_state.adminMessages.append({"role": "assistant", "content": "Welcome, enter the type of product:"})


# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        st.markdown(prompt)
        # schedule.clear()
        st.session_state.adminMessages.append({"role": "user", "content": prompt})
        # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        data = requests.get("http://127.0.0.1:8000/admin/handler/" + prompt.__str__()).json()
        st.write(data)
        st.session_state.adminMessages.append({"role": "assistant", "content": data})

        # 2
        #