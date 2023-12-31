import streamlit as st
import requests

st.title("HISTORY")

st.sidebar.success("MEw-MeW")

# Initialize chat history
if "history-messages" not in st.session_state:
    st.session_state.messages = []

flag = False
    # Display user message in chat message container
data = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/allproducts/chathistory").json()
with st.chat_message("assistant"):
    st.write("ENTER ORDER ID")
if prompt := st.chat_input("ORDER ID"):
    if prompt.isdecimal():
        data = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/allproducts/chathistory/" + prompt).json()
        if len(data) == 0:
            with st.chat_message("assistant"):
                st.write("USER WITH ID: " + prompt + " ISN'T EXIST")
        else:
            for item in data:
                with st.chat_message("user"):
                    st.write(item[0])
                with st.chat_message("assistant"):
                    st.write(item[1])
    else:
        with st.chat_message("assistant"):
            st.write("ID MUST BE NUMBER")