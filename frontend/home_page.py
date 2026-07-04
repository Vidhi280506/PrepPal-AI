import streamlit as st
from backend import get_progress


def render_home():

    st.title("🤖 PrepPal AI")

    st.subheader("Your Personal AI Coding Mentor")

    st.caption(
        "Master DSA with personalized practice, AI coaching and progress tracking."
    )

    st.divider()

    try:

        data = get_progress()

        progress = data["progress"]

    except Exception:

        progress = {
            "total_solved": 0,
            "accuracy_percentage": 0,
            "mastered_topics": 0,
            "weak_topics": [],
        }

    weak_topic = (
        progress["weak_topics"][0]
        if progress["weak_topics"]
        else "None 🎉"
    )

    st.success(
        f"""
## 👋 Welcome Back!

You're making great progress.

Today's recommended focus:

### **{weak_topic}**
"""
    )

    st.divider()

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        st.metric(
            "✅ Solved",
            progress["total_solved"],
        )

    with c2:
        st.metric(
            "🎯 Accuracy",
            f"{progress['accuracy_percentage']}%",
        )

    with c3:
        st.metric(
            "🏆 Mastered",
            progress["mastered_topics"],
        )

    with c4:
        st.metric(
            "📚 Reviews",
            len(progress["weak_topics"]),
        )

    st.divider()

    st.subheader("🚀 Quick Actions")

    a, b, c = st.columns(3)

    with a:

        if st.button(
            "💬 Start Chat",
            use_container_width=True,
        ):
            st.session_state.page = "💬 Chat"
            st.rerun()

    with b:

        if st.button(
            "📈 View Progress",
            use_container_width=True,
        ):
            st.session_state.page = "📈 Progress"
            st.rerun()

    with c:

        if st.button(
            "📚 Continue Review",
            use_container_width=True,
        ):
            st.session_state.page = "📚 Review Queue"
            st.rerun()

    st.divider()

    st.subheader("💡 AI Recommendation")

    if progress["weak_topics"]:

        st.warning(
            f"""
Today's recommendation:

Spend at least **30 minutes** solving
**{weak_topic}** problems.

After that, review yesterday's mistakes.
"""
        )

    else:

        st.success(
            """
Amazing!

No weak topics detected.

Try solving a Hard problem today.
"""
        )

    st.divider()

    st.caption("PrepPal AI • Version 1.0")