import streamlit as st
import requests

st.title("ADD PRODUCT ADMIN PANEL")

st.sidebar.title("Program commands: ")
st.sidebar.info("update")
st.sidebar.info("add")
st.sidebar.info("stock")

# Initialize chat history
if "adminMessages" not in st.session_state:
    st.session_state.adminMessages = []

# Display chat messages from history on app rerun
for message in st.session_state.adminMessages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.adminMessages == []:
    with st.chat_message("assistant"):
        requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/admin/setToDefault").json()
        st.write("Welcome, Choose update,add or stock")
        st.session_state.adminMessages.append({"role": "assistant", "content": "Welcome, Choose update,add or stock"})

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
        data = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/admin/handler/" + prompt.__str__()).json()
        st.write(data)
        st.session_state.adminMessages.append({"role": "assistant", "content": data})



