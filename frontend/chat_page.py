import streamlit as st

from backend import ask_preppal, get_progress


def send_message(prompt: str):
    """
    Sends a prompt to PrepPal and updates chat history.
    """

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    with st.chat_message("assistant", avatar="🤖"):

        with st.spinner(
            "🧠 AI Coach is analyzing your request..."
        ):

            try:
                reply = ask_preppal(prompt)

            except Exception as e:
                reply = f"⚠️ **Error**\n\n{e}"

            st.success("### 🤖 PrepPal")

            st.markdown(reply)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": reply,
        }
    )


def render_chat():

    st.title("🤖 PrepPal AI")

    st.subheader("Your Personal DSA Mentor")

    st.caption(
        "Master Data Structures & Algorithms with personalized AI guidance."
    )

    st.divider()

    # ---------------- Load Progress ---------------- #

    try:
        progress_data = get_progress()["progress"]

    except Exception:

        progress_data = {
            "total_solved": 0,
            "accuracy_percentage": 0,
            "mastered_topics": 0,
            "weak_topics": [],
        }

    weak_topic = (
        progress_data["weak_topics"][0]
        if progress_data["weak_topics"]
        else "Any Topic"
    )
    
    # ---------------- AI Coach Dashboard ---------------- #

    st.subheader("🧠 AI Coach")

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric(
            "Solved",
            progress_data["total_solved"],
        )

    with m2:
        st.metric(
            "Accuracy",
            f"{progress_data['accuracy_percentage']}%",
        )

    with m3:
        st.metric(
            "Today's Focus",
            weak_topic,
        )

    with m4:
        st.metric(
            "AI Status",
            "🟢 Online",
        )

    st.divider()

    st.subheader("📊 Today's Session")

    user_msgs = sum(
        1 for m in st.session_state.messages
        if m["role"] == "user"
    )

    assistant_msgs = sum(
        1 for m in st.session_state.messages
        if m["role"] == "assistant"
    )

    c1, c2 = st.columns(2)

    with c1:
        st.info(f"💬 Questions Asked\n\n**{user_msgs}**")

    with c2:
        st.info(f"🤖 AI Responses\n\n**{assistant_msgs}**")

    st.divider()
    # ---------------- Welcome Card ---------------- #

    if len(st.session_state.messages) <= 1:

        st.success(
            f"""
## 👋 Welcome Back!

Ready for today's interview preparation?

Your AI mentor has analyzed your progress and prepared personalized recommendations.

Here's your current progress:

- ✅ Problems Solved: **{progress_data['total_solved']}**
- 🎯 Accuracy: **{progress_data['accuracy_percentage']}%**
- 🏆 Mastered Topics: **{progress_data['mastered_topics']}**

### 📌 Today's Focus

**{weak_topic}**

Strengthen this topic to improve your interview readiness.
"""
        )

        st.subheader("💡 Suggested Prompts")

        col1, col2 = st.columns(2)

        suggestions = [

            f"Recommend a {weak_topic} problem",

            f"Explain {weak_topic}",

            "Show my progress",

            "Review my weak topics",

            "Give me today's challenge",

            "Create a 7-day DSA study plan",

            "Explain Binary Search",

            "Give me a Medium Graph problem",
        ]

        for i, suggestion in enumerate(suggestions):

            column = col1 if i % 2 == 0 else col2

            with column:

                if st.button(
                    suggestion,
                    key=f"suggestion_{i}",
                    use_container_width=True,
                ):
                    send_message(suggestion)

        st.divider()

    # ---------------- Chat History ---------------- #

    for message in st.session_state.messages:

        with st.chat_message(
            message["role"],
            avatar="👤" if message["role"] == "user" else "🤖",
        ):
            st.markdown(message["content"])

    # ---------------- Chat Input ---------------- #
    if len(st.session_state.messages) <= 1:

        st.info(
            "💡 Tip: Ask for a coding problem, an explanation, your progress, or a personalized study plan."
        )

    prompt = st.chat_input("Ask PrepPal anything...")

    if prompt:  
        send_message(prompt)

    st.divider()

    st.caption(
        """
        🤖 Powered by Google Gemini • Google ADK • MCP • SQLite

        PrepPal AI v1.0
        """
    )