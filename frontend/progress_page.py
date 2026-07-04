import streamlit as st
from backend import get_progress
import pandas as pd

def render_progress():

    st.title("📈 Progress Dashboard")

    try:
        with st.spinner("Loading your progress..."):
            data = get_progress()
            progress = data["progress"]

    except Exception as e:
        st.error("⚠️ Unable to load your progress.")
        st.caption(str(e))
        return

    st.markdown("### 📊 Your Coding Journey")

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.metric(
            label="✅ Problems Solved",
            value=progress["total_solved"],
        )

    with col2:
        st.metric(
            label="🎯 Accuracy",
            value=f"{progress['accuracy_percentage']}%",
        )

    with col3:
        st.metric(
            label="🏆 Mastered Topics",
            value=progress["mastered_topics"],
        )
    
    with col4:
        st.metric(
            label="🔥 Streak",
            value="3 Days",
            delta="+1"
        )

    with col5:
        st.metric(
            label="⭐ Rank",
            value="Beginner",
        )
    
    st.divider()

    st.subheader("📊 Overall Accuracy")

    accuracy = progress["accuracy_percentage"] / 100

    st.progress(accuracy)

    st.caption(f"Current Accuracy: {progress['accuracy_percentage']}%")

    st.divider()

    left, right = st.columns([2, 1])

    with left:

        st.subheader("🎯 Topics to Focus")

        if progress["weak_topics"]:

            for topic in progress["weak_topics"]:

                st.markdown(f"### 📌 {topic}")

                st.progress(0.20)

                st.caption("Estimated Mastery: 20%")

        else:
            st.success("🎉 No weak topics. Excellent work!")

    with right:

        st.subheader("💡 Today's Goal")

        st.info(
            f"""
Practice **2-3 problems** from:

**{progress['weak_topics'][0] if progress['weak_topics'] else 'Any Topic'}**
"""
        )

    st.divider()

    st.subheader("🚀 Motivation")

    solved = progress["total_solved"]

    if solved < 10:

        st.info(
            "Every expert was once a beginner. Keep solving one problem at a time!"
        )

    elif solved < 50:

        st.success(
            "You're building great momentum. Stay consistent!"
        )

    else:

        st.balloons()

        st.success(
            "Outstanding! You're becoming interview ready!"
        )
    
    st.divider()

    st.subheader("🧠 Study Insights")

    if progress["accuracy_percentage"] < 40:

        st.error(
            """
            Focus on solving easier problems first.

            Accuracy is currently low.

            Recommendation:
            • Revise Arrays
            • Solve Easy questions
            • Don't rush Medium problems
            """
        )

    elif progress["accuracy_percentage"] < 70:

        st.warning(
            """
            You're improving steadily.

            Recommendation:
            • Increase consistency
            • Attempt more Medium problems
            """
        )

    else:

        st.success(
            """
            Excellent performance.

            Recommendation:
            Start solving Hard problems.
            """
        )
    
    st.divider()

    st.subheader("📈 Problems Solved This Week")

    activity = pd.DataFrame(
        {
            "Problems Solved": [1, 2, 1, 3, 2, 0, 4],
        },
        index=["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"],
    )

    st.bar_chart(activity)

    

    st.divider()

    st.subheader("📚 Problems by Topic")

    topics = pd.DataFrame(
        {
            "Topic": [
                "Arrays",
                "Strings",
                "Trees",
                "Graphs",
                "DP",
            ],
            "Problems": [
                5,
                2,
                3,
                1,
                1,
            ],
        }
    )

    st.bar_chart(
        topics.set_index("Topic")
    )