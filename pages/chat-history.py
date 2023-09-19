import threading
from typing import List

import schedule
import streamlit as st
import random
import time

import requests

st.title("COFFEE HISTORY")

st.sidebar.success("MEw-MeW")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []


# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])

flag = False
    # Display user message in chat message container
data = requests.get("http://127.0.0.1:8000/allproducts/chathistory").json()
with st.chat_message("assistant"):
    st.write("ENTER ORDER ID")
if prompt := st.chat_input("ORDER ID"):
    data = requests.get("http://127.0.0.1:8000/allproducts/chathistory/" + prompt).json()
    for item in data:
        with st.chat_message("user"):
            st.write(item[0])
        with st.chat_message("assistant"):
            st.write(item[1])