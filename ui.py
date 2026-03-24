import streamlit as st
import os
from groq import Groq
from classifier import classify_prompt
import pandas as pd

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

# -------- SESSION STATE -------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "logs" not in st.session_state:
    st.session_state.logs = []

if "view" not in st.session_state:
    st.session_state.view = "Chat"

# -------- SIDEBAR -------- #

with st.sidebar:
    st.header("⚙️ Controls")

    # View selector
    view_option = st.radio("View Mode", ["Chat", "Dashboard"])

    st.session_state.view = view_option

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.logs = []

# -------- CHAT VIEW -------- #

if st.session_state.view == "Chat":

    # Show chat history
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    # User input
    user_input = st.chat_input("Type your message...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    # -------- CLASSIFIER -------- #
                    result = classify_prompt(user_input)
                    category = result["category"]
                    confidence = result["confidence"]

                    # -------- LOGGING -------- #
                    st.session_state.logs.append({
                        "text": user_input,
                        "category": category,
                        "confidence": confidence
                    })

                    # -------- BLOCK -------- #
                    if category != "safe":
                        bot_reply = f"🚫 Blocked: {category} detected (confidence: {confidence:.2f})"

                    else:
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

        st.session_state.messages.append({"role": "assistant", "content": bot_reply})

# -------- DASHBOARD VIEW -------- #

elif st.session_state.view == "Dashboard":

    st.subheader("📊 Guardrails Dashboard")

    if st.session_state.logs:
        df = pd.DataFrame(st.session_state.logs)

        total = len(df)
        blocked = len(df[df["category"] != "safe"])
        safe = len(df[df["category"] == "safe"])

        col1, col2, col3 = st.columns(3)

        col1.metric("Total Prompts", total)
        col2.metric("Blocked", blocked)
        col3.metric("Safe", safe)

        st.write("### Category Distribution")
        st.bar_chart(df["category"].value_counts())

    else:
        st.info("No data yet. Start chatting to see analytics.")