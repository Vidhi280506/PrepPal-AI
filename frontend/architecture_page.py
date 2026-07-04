import streamlit as st


def render_architecture():

    st.title("🏗 PrepPal AI Architecture")

    st.caption(
        "An overview of the multi-agent architecture powering PrepPal AI."
    )

    st.divider()

    st.subheader("🧠 High-Level Architecture")

    st.code(
"""
            👤 User
                │
                ▼
      🖥 Streamlit Frontend
                │
                ▼
       🤖 Google ADK Runner
                │
                ▼
          🧠 Root Agent
          ┌───────────────┐
          ▼               ▼
    👨‍🏫 Coach Agent   📊 Tracker Agent
          │               │
          └───────┬───────┘
                  ▼
           🔗 MCP Server
                  │
                  ▼
          💾 SQLite Database
""",
language="text"
    )

    st.divider()

    st.subheader("⚙️ Request Flow")

    st.markdown(
"""
1️⃣ User sends a question through the Streamlit interface.

2️⃣ Google ADK receives the request.

3️⃣ The Root Agent decides which specialized agent should handle it.

4️⃣ Coach Agent recommends coding problems, explains concepts, and creates study plans.

5️⃣ Tracker Agent retrieves progress, weak topics, and review queue.

6️⃣ MCP Server securely accesses the SQLite database.

7️⃣ The response is returned to the user.
"""
    )

    st.divider()

    st.subheader("🤖 AI Components")

    c1, c2 = st.columns(2)

    with c1:

        st.info(
"""
### 👨‍🏫 Coach Agent

Responsible for

- Problem recommendations
- Algorithm explanations
- Interview guidance
- Study plans
"""
        )

    with c2:

        st.info(
"""
### 📊 Tracker Agent

Responsible for

- Progress tracking
- Weak topic detection
- Review scheduling
- Performance analytics
"""
        )

    st.divider()

    st.subheader("🛠 Technology Stack")

    st.markdown(
"""
| Layer | Technology |
|-------|------------|
| Frontend | Streamlit |
| AI Framework | Google ADK |
| LLM | Gemini 2.5 Flash |
| Agent Communication | MCP |
| Database | SQLite |
| Backend | Python |
"""
    )

    st.divider()

    st.subheader("💡 Why Multi-Agent?")

    st.success(
"""
Instead of using a single AI agent, PrepPal separates responsibilities.

✅ Coach Agent focuses on learning.

✅ Tracker Agent focuses on analytics.

This makes the system easier to extend, maintain and scale.
"""
    )

    st.divider()

    st.caption("PrepPal AI • Architecture Overview • Version 1.0")

"""
🎯 Why PrepPal?

PrepPal is an AI-powered interview preparation platform that combines:

• Google Agent Development Kit (ADK)
• Multi-Agent Architecture
• Model Context Protocol (MCP)
• Gemini 2.5 Flash
• SQLite

to deliver personalized coding guidance, adaptive problem recommendations, and progress tracking.
"""