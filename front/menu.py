# import streamlit as st
# import requests
#
# st.title("COFFEE SHOt")
#
# st.sidebar.title("Program commands: ")
# st.sidebar.info("I'd like a")
# st.sidebar.info("I don't want a")
# st.sidebar.info("Show all")
# st.sidebar.info("That's all")
# st.sidebar.info("What's")
#
#
# # Initialize chat history
# if "messages" not in st.session_state:
#     st.session_state.messages = []
#
# # Display chat messages from history on app rerun
# for message in st.session_state.messages:
#     with st.chat_message(message["role"]):
#         st.markdown(message["content"])
#
# if st.session_state.messages == []:
#     with st.chat_message("assistant"):
#         requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/setToDefault").json()
#         st.write("Welcome, what can I get you")
#         st.session_state.messages.append({"role": "assistant", "content": "Welcome, what can I get you"})
# flag = False
# #
# # Accept user input
# if prompt := st.chat_input("What is up?"):
#     # Display user message in chat message container
#     with st.chat_message("user"):
#         st.markdown(prompt)
#         # schedule.clear()
#         st.session_state.messages.append({"role": "user", "content": prompt})
#         # Display assistant response in chat message container
#     with st.chat_message("assistant"):
#         message_placeholder = st.empty()
#         full_response = ""
#         data = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/handler/" + prompt.__str__()).json()
#         st.write(data)
#         st.session_state.messages.append({"role": "assistant", "content": data})

import streamlit as st
import requests
import asyncio

st.title("COFFEE SHOt")

st.sidebar.title("Program commands: ")
st.sidebar.info("I'd like a")
st.sidebar.info("I don't want a")
st.sidebar.info("Show all")
st.sidebar.info("That's all")
st.sidebar.info("What's")


async def wait_for_input():
    prompt = st.chat_input("What is up?")
    if prompt:
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)
            st.session_state.messages.append({"role": "user", "content": prompt})
            # Display assistant response in chat message container
        with st.chat_message("assistant"):
            data = requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/handler/" + prompt.__str__()).json()
            st.write(data)
            st.session_state.messages.append({"role": "assistant", "content": data})
    await asyncio.sleep(15)  # Очікуємо 2 секунди
    st.warning("Please go ahead when you are ready.")

# Головна функція для відображення інтерфейсу користувача
def main():
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if st.session_state.messages == []:
        with st.chat_message("assistant"):
            requests.get("https://fastapi-project-k2w6seoxja-uc.a.run.app/handler/").json()
            st.write("Welcome, what can I get you")
            st.session_state.messages.append({"role": "assistant", "content": "Welcome, what can I get you"})
    asyncio.run(wait_for_input())

# Викликаємо головну функцію
if __name__ == "__main__":
    main()