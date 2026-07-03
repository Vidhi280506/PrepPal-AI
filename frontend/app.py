import streamlit as st
from backend import ask_preppal
from chat_page import render_chat
from progress_page import render_progress
from review_page import render_review
from settings_page import render_settings

# ---------------- Page Config ----------------

st.set_page_config(
    page_title="PrepPal AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------- Session State ----------------

if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": (
                "👋 Hi! I'm PrepPal AI.\n\n"
                "I can:\n"
                "- Recommend DSA problems\n"
                "- Explain algorithms\n"
                "- Give hints\n"
                "- Show your progress"
            ),
        }
    ]

# ---------------- Sidebar ----------------

with st.sidebar:

    st.title("🎯 PrepPal AI")

    st.markdown("---")

    st.subheader("Navigation")

    page = st.radio(
        "Navigation",
        [
            "💬 Chat",
            "📈 Progress",
            "📚 Review Queue",
            "⚙️ Settings",
        ],
        label_visibility="collapsed",
    )
    
    if page == "💬 Chat":
        render_chat()
        
    if page == "📈 Progress":
        render_progress()
    
    elif page == "📚 Review Queue":
        render_review()
    
    elif page == "⚙️ Settings":
        render_settings()