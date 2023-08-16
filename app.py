import os
import streamlit as st
from langflow import load_flow_from_json
import openai

openai_api_key = os.environ.get("OPENAI_API_KEY")
chat_openai_node = openai.ChatOpenAI(openai_api_key=openai_api_key)

flow = load_flow_from_json("flow/elizabot.json", chat_openai_node)


def add_bg_from_url():
    st.markdown(
        """
        <style>
        .stApp {
            background-image: url("https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg");
            background-attachment: fixed;
            background-size: cover;
            min-height: 100vh;
        }
        @media (max-width: 768px) {
            .stApp {
                background-size: cover;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def main():
    st.set_page_config(page_title="Eliza Bot", page_icon="🤖")
    add_bg_from_url()
    st.title("Eliza Bot")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message["avatar"]):
            st.write(message["content"])

    with st.container():
        st.markdown(
            """
            <style>
            .stChatFloatingInputContainer {
                background-image: url("https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg");
                background-attachment: fixed;
                background-size: cover;
                padding: 10px;
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        prompt = st.chat_input(
            "Oi, Sou a Eliza Bot, sua psicóloga virtual. Como você está se sentindo hoje?"
        )

        if prompt:
            st.session_state.messages.append({
                "role": "user",
                "content": prompt,
                "avatar": "icons/user.png"
            })

            with st.chat_message("user", avatar="icons/user.png"):
                st.write(prompt)

            with st.chat_message("assistant", avatar="icons/assistant.png"):
                message_placeholder = st.empty()
                with st.spinner(text="Digitando..."):
                    user_input = {"text": prompt}
                    response = flow(user_input)
                    answer = response["text"]
                    message_placeholder.write(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "avatar": "icons/assistant.png",
            })


if __name__ == "__main__":
    main()
