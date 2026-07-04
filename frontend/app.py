import streamlit as st
#from backend import ask_preppal
from chat_page import render_chat
from progress_page import render_progress
from review_page import render_review
from settings_page import render_settings
from home_page import render_home
from pathlib import Path
from architecture_page import render_architecture

# ---------------- Page Config ----------------
def load_css():
    css = Path("frontend/styles/style.css").read_text()
    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )

st.set_page_config(
    page_title="PrepPal AI",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_css()

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

    if "page" not in st.session_state:
        st.session_state.page = "🏠 Home"

    page = st.radio(
        "Navigation",
        [
            "🏠 Home",
            "💬 Chat",
            "📈 Progress",
            "📚 Review Queue",
            "⚙️ Settings",
            "🏗 Architecture",
        ],
        index=[
            "🏠 Home",
            "💬 Chat",
            "📈 Progress",
            "📚 Review Queue",
            "⚙️ Settings",
            "🏗 Architecture",
        ].index(st.session_state.page),
        label_visibility="collapsed",
    )

    st.session_state.page = page

if page == "🏠 Home":
    render_home()

if page == "💬 Chat":
    render_chat()
        
if page == "📈 Progress":
    render_progress()
    
elif page == "📚 Review Queue":
    render_review()
    
elif page == "⚙️ Settings":
    render_settings()

elif page == "🏗 Architecture":
    render_architecture()