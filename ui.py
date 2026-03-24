import streamlit as st
import requests
import json

API_URL = "http://127.0.0.1:8001/ask"

st.set_page_config(page_title="AI Guardrails Chat", page_icon="🤖", layout="centered")

st.title("🤖 AI Guardrails Chat")
st.caption("Safe AI assistant with real-time guardrails")

# -------- Sidebar -------- #
with st.sidebar:
    st.header("⚙️ Controls")

    if st.button("Clear Chat"):
        st.session_state.messages = []

    st.divider()

    st.subheader("📜 Recent Logs")

    try:
        with open("logs.json", "r") as f:
            logs = json.load(f)

        if logs:
            for log in reversed(logs[-5:]):  # last 5 logs
                st.write(f"**Input:** {log['input']}")
                st.write(f"**Status:** {log['status']}")
                st.divider()
        else:
            st.write("No logs yet")

    except:
        st.write("No logs file found")

# -------- Chat History -------- #
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

# -------- User Input -------- #
user_input = st.chat_input("Type your message...")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.write(user_input)

    # Get response from backend
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                response = requests.post(API_URL, json={"query": user_input})
                result = response.json()

                if "response" in result:
                    bot_reply = result["response"]
                else:
                    bot_reply = f"Error: {result}"

            except Exception as e:
                bot_reply = f"Error: {str(e)}"

            st.write(bot_reply)

    # Save assistant message
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})