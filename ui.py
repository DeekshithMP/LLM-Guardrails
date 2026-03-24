import streamlit as st
import os
from groq import Groq
from classifier import classify_prompt

# Page config
st.set_page_config(
    page_title="AI Guardrails Chat",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Guardrails Chat")
st.caption("Safe AI assistant with real-time guardrails")

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Sidebar
with st.sidebar:
    st.header("⚙️ Controls")
    if st.button("Clear Chat"):
        st.session_state.messages = []

# Chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# User input
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Assistant response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                # -------- CLASSIFIER -------- #
                result = classify_prompt(user_input)
                category = result["category"]
                confidence = result["confidence"]

                # -------- BLOCK IF UNSAFE -------- #
                if category != "safe":
                    bot_reply = f"🚫 Blocked: {category} detected (confidence: {confidence:.2f})"

                else:
                    # -------- LLM CALL -------- #
                    completion = client.chat.completions.create(
                        model="llama-3.1-8b-instant",
                        messages=[
                            {"role": "system", "content": "You are a helpful AI assistant."},
                            {"role": "user", "content": user_input}
                        ]
                    )

                    bot_reply = completion.choices[0].message.content

            except Exception as e:
                bot_reply = f"❌ Error: {str(e)}"

            st.write(bot_reply)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})