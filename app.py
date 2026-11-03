import os

import streamlit as st
from google import genai
from google.genai import types

st.set_page_config(
    page_title="Chitti Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Chitti Chatbot")
st.caption("Your friendly AI assistant, powered by Google Gemini.")

# Read the key from Render environment variables first, then Streamlit secrets.
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("GEMINI_API_KEY")
    except Exception:
        api_key = None

if not api_key:
    st.warning(
        "The chatbot is deployed, but it needs a Gemini API key before it can answer. "
        "In your Render dashboard, open this service → Environment and add "
        "GEMINI_API_KEY with your Google AI Studio API key, then save and redeploy."
    )
    st.link_button(
        "Get a Gemini API key",
        "https://aistudio.google.com/apikey",
    )
    st.stop()

MODEL_NAME = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
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

    contents = []
    for message in st.session_state.messages:
        role = "user" if message["role"] == "user" else "model"
        contents.append(
            types.Content(
                role=role,
                parts=[types.Part.from_text(text=message["content"])],
            )
        )

    with st.chat_message("assistant"):
        with st.spinner("Chitti is thinking..."):
            try:
                response = client.models.generate_content(
                    model=MODEL_NAME,
                    contents=contents,
                    config=types.GenerateContentConfig(
                        system_instruction=SYSTEM_INSTRUCTION,
                        temperature=0.7,
                    ),
                )
                answer = response.text or "I couldn't generate a text response. Please try again."
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as exc:
                st.error(
                    "I couldn't reach Gemini. Check that your API key is valid, "
                    "the selected model is available, and your API quota has not been exceeded."
                )
                st.caption(f"Technical details: {exc}")
                # Remove the unanswered prompt so the user can retry.
                if st.session_state.messages and st.session_state.messages[-1]["role"] == "user":
                    st.session_state.messages.pop()
