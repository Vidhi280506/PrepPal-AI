# frontend/chat_page.py

import streamlit as st
from backend import ask_preppal


def render_chat():

    st.title("💬 PrepPal AI Coach")

    st.caption("Your personal DSA mentor")

    st.divider()

    for message in st.session_state.messages:

        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    prompt = st.chat_input("Ask PrepPal anything...")

    if prompt:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": prompt,
            }
        )

        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):

            with st.spinner("PrepPal is thinking..."):

                try:
                    reply = ask_preppal(prompt)

                except Exception as e:
                    reply = f"⚠️ Error:\n\n{e}"

                st.markdown(reply)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": reply,
            }
        )