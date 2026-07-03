import streamlit as st
from backend import get_progress


def render_progress():

    st.title("📈 Progress Dashboard")

    data = get_progress()

    progress = data["progress"]

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Problems Solved",
            progress["total_solved"],
        )

    with col2:
        st.metric(
            "Accuracy",
            f"{progress['accuracy_percentage']}%",
        )

    with col3:
        st.metric(
            "Mastered Topics",
            progress["mastered_topics"],
        )

    st.divider()

    st.subheader("Weak Topics")

    if progress["weak_topics"]:

        for topic in progress["weak_topics"]:
            st.write(f"• {topic}")

    else:
        st.success("No weak topics!")