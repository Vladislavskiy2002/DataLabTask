import streamlit as st
import requests
import time

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
        requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/setToDefault").json()
        st.write("Welcome, what can I get you")
        st.session_state.messages.append({"role": "assistant", "content": "Welcome, what can I get you"})
flag = False
#
start_time = time.time()
# Accept user input
if prompt := st.chat_input("What is up?"):
    # Display user message in chat message container
    with st.chat_message("user"):
        end_time = time.time()
        execution_time = end_time - start_time
        st.write(f'Час виконання: {execution_time:.2f} секунд')
        st.markdown(prompt)
        # schedule.clear()
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        data = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/handler/" + prompt.__str__()).json()
        st.write(data)
        st.session_state.messages.append({"role": "assistant", "content": data})
