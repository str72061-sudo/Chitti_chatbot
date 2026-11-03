import os

import streamlit as st
from google import genai

st.set_page_config(
    page_title="Chitti Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Chitti Chatbot")
st.caption("Your friendly AI assistant, powered by Google Gemini.")

api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

if not api_key:
    st.warning(
        "Chitti needs a Gemini API key. Add GEMINI_API_KEY in your Render "
        "service's Environment settings, then redeploy."
    )
    st.link_button("Get a Gemini API key", "https://aistudio.google.com/apikey")
    st.stop()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
SYSTEM_INSTRUCTION = (
    "You are Chitti, a helpful, friendly AI assistant. "
    "Answer clearly and accurately. Use simple language when appropriate. "
    "If you are unsure, say so rather than making up facts."
)

client = genai.Client(api_key=api_key)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.sidebar:
    st.subheader("About Chitti")
    st.write("Ask questions, explore ideas, or get help with everyday tasks.")
    st.caption(f"Model: {MODEL_NAME}")
    if st.button("🗑️ Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Message Chitti...")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    conversation = "\n".join(
        f'{ "User" if item["role"] == "user" else "Chitti" }: {item["content"]}'
        for item in st.session_state.messages
    )

    with st.chat_message("assistant"):
        with st.spinner("Chitti is thinking..."):
            try:
                # The Interactions API supports Google's newer AQ authorization keys.
                interaction = client.interactions.create(
                    model=MODEL_NAME,
                    input=conversation,
                    system_instruction=SYSTEM_INSTRUCTION,
                    store=False,
                )
                answer = interaction.output_text or (
                    "I couldn't generate a text response. Please try again."
                )
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            except Exception:
                st.error(
                    "I couldn't reach Gemini. Check the GEMINI_API_KEY in Render, "
                    "that the key is active, and that your Gemini API quota is available."
                )
                if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                    st.session_state.messages.pop()
