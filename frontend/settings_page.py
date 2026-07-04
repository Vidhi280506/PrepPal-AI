import streamlit as st


def render_settings():

    st.title("⚙️ Settings")

    st.caption("Configure and monitor your PrepPal AI environment.")

    st.divider()

    # ---------------- AI Configuration ---------------- #

    st.subheader("🤖 AI Configuration")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(
            "AI Model",
            "Gemini 2.5 Flash",
        )

        st.metric(
            "Development Mode",
            "Enabled",
        )

    with col2:

        st.metric(
            "AI Status",
            "🟢 Connected",
        )

        st.metric(
            "Response Mode",
            "Multi-Agent",
        )

    st.divider()

    # ---------------- Backend Status ---------------- #

    st.subheader("💾 Backend Status")

    b1, b2 = st.columns(2)

    with b1:

        st.success("🟢 SQLite Database")

        st.success("🟢 MCP Server")

    with b2:

        st.success("🟢 Google ADK")

        st.success("🟢 Streamlit Frontend")

    st.divider()

    # ---------------- Project Information ---------------- #

    st.subheader("📊 Project Information")

    info1, info2 = st.columns(2)

    with info1:

        st.metric(
            "Version",
            "1.0.0",
        )

        st.metric(
            "Build",
            "Portfolio Edition",
        )

    with info2:

        st.metric(
            "Language",
            "Python",
        )

        st.metric(
            "Framework",
            "Streamlit",
        )

    st.divider()

    # ---------------- Technology Stack ---------------- #

    st.subheader("🛠 Technology Stack")

    st.markdown(
        """
- 🤖 Google Gemini 2.5 Flash
- 🧠 Google Agent Development Kit (ADK)
- 🔗 Model Context Protocol (MCP)
- 💾 SQLite Database
- 🐍 Python
- 🎨 Streamlit
"""
    )

    st.divider()

    # ---------------- Architecture ---------------- #

    st.subheader("🏗 System Architecture")

    st.code(
        """
User
   │
   ▼
Streamlit Frontend
   │
   ▼
Google ADK Runner
   │
   ▼
Root Agent
   │
   ├───────────────┐
   ▼               ▼
Coach Agent    Tracker Agent
   │               │
   └───────┬───────┘
           ▼
      MCP Server
           ▼
      SQLite Database
""",
        language="text",
    )

    st.divider()

    # ---------------- About ---------------- #

    st.subheader("📖 About PrepPal")

    st.info(
        """
PrepPal is an AI-powered DSA interview preparation platform.

It combines Google's Agent Development Kit (ADK),
Gemini AI, Model Context Protocol (MCP),
and SQLite to deliver personalized coding practice,
progress tracking, and intelligent recommendations.
"""
    )

    st.divider()

    st.caption(
        "Made with ❤️ by Vidhi Gadhari"
    )
    