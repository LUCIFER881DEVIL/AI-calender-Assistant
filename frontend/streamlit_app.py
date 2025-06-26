# frontend/streamlit_app.py

import streamlit as st
import requests

st.set_page_config(page_title="🧠 Calendar Assistant", page_icon="📅")

st.title("📅 Tailor Talk - Calendar Assistant")
st.markdown("Ask me to book appointments like:\n- *Book a call tomorrow from 3 to 5 PM*\n- *Do I have any slots Friday afternoon?*")

# Initialize message history
if "history" not in st.session_state:
    st.session_state.history = []

# Chat input
user_input = st.chat_input("Type your message...")

if user_input:
    st.session_state.history.append(("user", user_input))

    with st.spinner("Thinking..."):
        res = requests.post("http://localhost:8000/chat", json={"message": user_input})
        bot_reply = res.json().get("response", "Something went wrong.")
        st.session_state.history.append(("bot", bot_reply))

# Display chat history
for sender, msg in st.session_state.history:
    with st.chat_message(sender):
        st.markdown(msg)
