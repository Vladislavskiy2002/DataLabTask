import streamlit as st
import requests

st.title("COFFEE SHOt")

st.sidebar.title("Program commands: ")
st.sidebar.info("I'd like a")
st.sidebar.info("I don't want a")
st.sidebar.info("Show all")
st.sidebar.info("That's all")


# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.messages == []:
    with st.chat_message("assistant"):
        requests.get("http://fastapi:8080/setToDefault").json()
        st.write("Welcome, what can I get you")
        st.session_state.messages.append({"role": "assistant", "content": "Welcome, what can I get you"})
flag = False
#
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
        data = requests.get("http://fastapi:8080/handler/" + prompt.__str__()).json()
        st.write(data)
        st.session_state.messages.append({"role": "assistant", "content": data})
