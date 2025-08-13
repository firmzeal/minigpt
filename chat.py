from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
import streamlit as st
import os
from dotenv import load_dotenv

# Load token from .env if available
load_dotenv()

st.set_page_config(page_title="Mini Chat", page_icon="💬")
st.title("💬 Mini-ChatGPT with Memory")

# Initialize chat history
if "history" not in st.session_state:
    st.session_state.history = []

def generate_response(user_input):
    credential = os.environ.get("GITHUB_TOKEN")
    if not credential:
        st.error("Missing GITHUB_TOKEN. Please set it in your environment or .env file.")
        return

    model = AzureAIChatCompletionsModel(
        endpoint="https://models.github.ai/inference",
        model="openai/gpt-4.1",
        credential=credential
    )

    # Build context from history
    context = "\n".join([f"User: {u}\nBot: {b}" for u, b in st.session_state.history])
    full_prompt = f"{context}\nUser: {user_input}"

    response = model.invoke(full_prompt)
    bot_reply = response.content

    # Save to history
    st.session_state.history.append((user_input, bot_reply))

# Display chat messages
for user_msg, bot_msg in st.session_state.history:
    with st.chat_message("user"):
        st.markdown(user_msg)
    with st.chat_message("assistant"):
        st.markdown(bot_msg)

# Chat input
if prompt := st.chat_input("Type your message..."):
    # Show user message immediately
    with st.chat_message("user"):
        st.markdown(prompt)
    generate_response(prompt)
    # Show bot reply
    with st.chat_message("assistant"):
        st.markdown(st.session_state.history[-1][1])
