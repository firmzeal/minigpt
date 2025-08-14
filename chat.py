from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
import streamlit as st
import os
import time
from dotenv import load_dotenv

load_dotenv()
st.set_page_config(page_title="Mini Chat", page_icon="💬")
st.title("💬 Mini-ChatGPT with Memory By Firmzeal")

if "history" not in st.session_state:
    st.session_state.history = []

def generate_response(user_input):
    credential = os.environ.get("GITHUB_TOKEN")
    if not credential:
        st.error("Missing GITHUB_TOKEN. Please set it in your environment or .env file.")
        return None

    model = AzureAIChatCompletionsModel(
        endpoint="https://models.github.ai/inference",
        model="openai/gpt-4.1",
        credential=credential
    )

    context = "\n".join([f"User: {u}\nBot: {b}" for u, b in st.session_state.history])
    full_prompt = f"{context}\nUser: {user_input}"
    response = model.invoke(full_prompt)
    return response.content

for user_msg, bot_msg in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg)

if prompt := st.chat_input("Type your message..."):
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        placeholder = st.empty()
        placeholder.markdown("Thinking...")
        bot_reply = generate_response(prompt)

        if bot_reply:
            typed_text = ""
            for char in bot_reply:
                typed_text += char
                placeholder.markdown(typed_text)
                time.sleep(0.02)

    if bot_reply:
        st.session_state.history.append((prompt, bot_reply))