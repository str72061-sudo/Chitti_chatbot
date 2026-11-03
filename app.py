import os

import streamlit as st
from groq import Groq

st.set_page_config(
    page_title="Chitti Chatbot",
    page_icon="🤖",
    layout="centered",
)

st.title("🤖 Chitti Chatbot")
st.caption("Your friendly AI assistant, powered by Groq.")

api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except Exception:
        api_key = None

if not api_key:
    st.warning(
        "Chitti needs a Groq API key. Add GROQ_API_KEY in your Render "
        "service's Environment settings, then redeploy."
    )
    st.link_button("Get a Groq API key", "https://console.groq.com/keys")
    st.stop()

MODEL_NAME = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
SYSTEM_INSTRUCTION = (
    "You are Chitti, a helpful, friendly AI assistant. "
    "Answer clearly and accurately. Use simple language when appropriate. "
    "If you are unsure, say so rather than making up facts."
)

client = Groq(api_key=api_key)

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

    with st.chat_message("assistant"):
        with st.spinner("Chitti is thinking..."):
            try:
                completion = client.chat.completions.create(
                    model=MODEL_NAME,
                    messages=[
                        {"role": "system", "content": SYSTEM_INSTRUCTION},
                        *st.session_state.messages,
                    ],
                    temperature=0.7,
                    max_completion_tokens=2048,
                )
                answer = completion.choices[0].message.content or (
                    "I couldn't generate a text response. Please try again."
                )
                st.markdown(answer)
                st.session_state.messages.append(
                    {"role": "assistant", "content": answer}
                )
            except Exception as error:
                st.error(
                    "I couldn't reach Groq. Check that GROQ_API_KEY is correct "
                    "and active, and that your Groq account has available usage."
                )
                st.session_state.messages.pop()
