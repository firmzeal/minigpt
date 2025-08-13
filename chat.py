
from langchain_azure_ai.chat_models import AzureAIChatCompletionsModel
import streamlit as st
import os
from dotenv import load_dotenv

# Load token from .env if available
load_dotenv()

st.title("Mini-ChatGPT with Memory")

# Initialize session state for chat history
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
    st.info(bot_reply)

# Chat UI
with st.form("chat_interface"):
    text = st.text_area("Enter your message:")
    submitted = st.form_submit_button("Submit")
    if submitted and text.strip():
        generate_response(text)

# Display chat history
if st.session_state.history:
    st.subheader("Conversation history")
    for user_msg, bot_msg in st.session_state.history:
        st.write(f"**You:** {user_msg}")
        st.write(f"**Bot:** {bot_msg}")
# Clear chat history button
if st.button("Clear Chat History"):
    st.session_state.history = []
    st.success("Chat history cleared.")
    st.rerun()

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by fm")
st.markdown("Powered by [Azure AI](https://azure.microsoft.com/en-us/services/cognitive-services/azure-openai-service/) and [Streamlit](https://streamlit.io/).")
