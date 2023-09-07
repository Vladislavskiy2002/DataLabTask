from typing import List

import streamlit as st
import random
import time

import requests

st.title("Simple chat")


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
    # Add user message to chat history
    if prompt.startswith("I'd like a "):
        prompt = prompt.replace("I'd like a ", '', 1) #I'd like a banana
        print("prompt: " + prompt)
        data = requests.get("http://127.0.0.1:8000/menus/" + prompt.__str__()).json()

        ##st.chat_input("Would you like anything else?")
        st.write(data)
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("Would you like anything else?")
        st.session_state.messages.append({"role": "assistant", "content": "Would you like anything else?"})
        time.sleep(0.5)
    if prompt.startswith("I don't want a "):
        prompt = prompt.replace("I don't want a ", '', 1)  # I'd like a banana
        print("prompt: " + prompt)
        data = requests.get("http://127.0.0.1:8000/product/remove/" + prompt.__str__()).json()
        st.write(data)
    if prompt.startswith("That's all"):
        with st.chat_message("assistant"):
            message_placeholder = st.empty()
            message_placeholder.markdown("YOUR ORDER IS: ")
            data = requests.get("http://127.0.0.1:8000/product/all/" + prompt.__str__())
            st.write(data)
    st.session_state.messages.append({"role": "user", "content": prompt})

# Display assistant response in chat message container
with st.chat_message("assistant"):
    message_placeholder = st.empty()
    full_response = ""

    assistant_response = random.choice(
        [
            "Hello there! How can I assist you today?",
            "Hi, human! Is there anything I can help you with?",
            "Do you need help?",
        ]
    )
    # Simulate stream of response with milliseconds delay
    for chunk in assistant_response.split():
        full_response += chunk + " "
        time.sleep(0.05)
        # Add a blinking cursor to simulate typing
        message_placeholder.markdown(full_response + "")
    message_placeholder.markdown(full_response)
# Add assistant response to chat history
st.session_state.messages.append({"role": "assistant", "content": full_response})