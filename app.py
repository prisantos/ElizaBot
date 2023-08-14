import requests
import streamlit as st

BASE_API_URL = "https://langflow-su78.onrender.com/api/v1/process"
FLOW_ID = "96159c25-9c92-49ee-9ddf-67f0edfeda40"

TWEAKS = {
    "ChatOpenAI-01nzK": {},
    "LLMChain-Clut2": {},
    "PromptTemplate-aMVlP": {},
    "ConversationBufferMemory-31iVt": {}
}


def run_flow(message: str, flow_id: str, tweaks: dict = None) -> dict:
    api_url = f"{BASE_API_URL}/{flow_id}"

    payload = {"inputs": {"text": message}}

    if tweaks:
        payload["tweaks"] = tweaks

    response = requests.post(api_url, json=payload, verify=False)
    return response.json()


def add_bg_from_url():
    st.markdown(f"""
         <style>
         .stApp {{
            background-image: url("https://cdn.pixabay.com/photo/2015/04/23/22/00/tree-736885_1280.jpg");
            background-attachment: fixed;
            background-size: cover;
            min-height: 100vh;
         }}
         @media (max-width: 768px) {{
            .stApp {{
                background-size: contain;
            }}
         }}
         </style>
         """,
                unsafe_allow_html=True)


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
                padding: 10px; /* Adjust padding to your preference */
            }
            </style>
            """,
            unsafe_allow_html=True,
        )

        prompt = st.chat_input(
            "Oi, Sou a Eliza Bot, sua psicóloga virtual. Como você está se sentindo hoje"
        )

        if prompt:
            # adiciona mensagem do usuário no histórico do chat
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
                    response = run_flow(prompt, flow_id=FLOW_ID, tweaks=TWEAKS)
                    answer = response["result"]["text"]
                    message_placeholder.write(answer)

            st.session_state.messages.append({
                "role": "assistant",
                "content": answer,
                "avatar": "icons/assistant.png",
            })


if __name__ == "__main__":

    main()
