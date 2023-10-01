import streamlit as st
import requests

st.title("ADD PRODUCT ADMIN PANEL")

st.sidebar.title("Program commands: ")
st.sidebar.info("update")
st.sidebar.info("add")

# st.sidebar.success("WoWf-WoWf")


# Initialize chat history
if "adminMessages" not in st.session_state:
    st.session_state.adminMessages = []

# Display chat messages from history on app rerun
for message in st.session_state.adminMessages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if st.session_state.adminMessages == []:
    with st.chat_message("assistant"):
        requests.get("http://fastapi:8080/admin/setToDefault").json()
        st.write("Welcome, Choose update or add")
        st.session_state.adminMessages.append({"role": "assistant", "content": "Welcome, chosee add or update:"})

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
        data = requests.get("http://fastapi:8080/admin/handler/" + prompt.__str__()).json()
        st.write(data)
        st.session_state.adminMessages.append({"role": "assistant", "content": data})

# while True:
#     input_key = str(uuid.uuid4())  # Генеруємо унікальний ключ для кожної ітерації
#
#     prompt = st.chat_input("What is up?", key=input_key)
#     print(prompt)
#
#     if prompt:
#         with st.chat_message("user"):
#             st.markdown(prompt)
#             st.session_state.adminMessages.append({"role": "user", "content": prompt})
#
#         with st.chat_message("assistant"):
#             message_placeholder = st.empty()
#             full_response = ""
#             data = requests.get("http://127.0.0.1:8000/admin/handler/" + prompt.__str__()).json()
#             st.write(data)
#             st.session_state.adminMessages.append({"role": "assistant", "content": data})
#
#         # Вихід з циклу, коли prompt заповнено
#         break
#     else:
#         time.sleep(5)
#         st.warning("When you will already tell")



