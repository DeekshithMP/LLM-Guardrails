import streamlit as st
import os
from dotenv import load_dotenv
from groq import Groq
from classifier import classify_prompt
import pandas as pd

# Load env variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# -------- PAGE CONFIG -------- #

st.set_page_config(
    page_title="AI Guardrails Chat",
    page_icon="🤖",
    layout="centered"
)

st.title("🤖 AI Guardrails Chat")
st.caption("Safe AI assistant with real-time guardrails")

# -------- SESSION STATE -------- #

if "messages" not in st.session_state:
    st.session_state.messages = []

if "logs" not in st.session_state:
    st.session_state.logs = []

# -------- SIDEBAR -------- #

with st.sidebar:
    st.header("⚙️ Controls")

    threshold = st.slider("Safety Threshold", 0.1, 0.9, 0.6)

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.logs = []
    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.session_state.logs = []

    st.divider()
    st.subheader("📝 Recent Searches")

    if st.session_state.logs:
        for log in reversed(st.session_state.logs[-5:]):
            st.write(f"**Query:** {log['text']}")
            st.write(f"Category: {log['category']} ({log['confidence']:.2f})")
            st.divider()
    else:
        st.write("No searches yet.")

# -------- CONTAINERS -------- #

chat_container = st.container()
dashboard_container = st.container()

# -------- CHAT -------- #

with chat_container:

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.write(msg["content"])

    user_input = st.chat_input("Type your message...")

    if user_input:
        st.session_state.messages.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.write(user_input)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    result = classify_prompt(user_input)
                    category = result["category"]
                    confidence = result["confidence"]

                    # Log
                    st.session_state.logs.append({
                        "text": user_input,
                        "category": category,
                        "confidence": confidence
                    })

                    # -------- BALANCED BLOCK LOGIC -------- #

                    if category != "safe":

                        # Strong block
                        if confidence >= threshold:
                            bot_reply = f"🚫 Blocked: {category} detected (confidence: {confidence:.2f})"

                        # Medium confidence → warning
                        elif confidence >= 0.4:
                            bot_reply = f"⚠️ Potentially unsafe: {category} (confidence: {confidence:.2f})"

                        # Low confidence → allow
                        else:
                            completion = client.chat.completions.create(
                                model="llama-3.1-8b-instant",
                                messages=[
                                    {"role": "system", "content": "You are a helpful AI assistant."},
                                    {"role": "user", "content": user_input}
                                ]
                            )
                            bot_reply = completion.choices[0].message.content

                    else:
                        # SAFE → allow
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

# -------- DASHBOARD -------- #

with dashboard_container:

    st.divider()
    st.subheader("📊 Real-Time Guardrails Dashboard")

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

        st.write("### Recent Activity")
        st.dataframe(df.tail(5), use_container_width=True)

    else:
        st.info("Start chatting to see real-time analytics.")