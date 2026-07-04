import streamlit as st
from backend import get_review_queue


def render_review():

    try:
        with st.spinner("Loading your review queue..."):
            data = get_review_queue()
            review_problems = data["due_reviews"]

    except Exception as e:
        st.error("⚠️ Unable to load your review queue.")
        st.caption(str(e))
        return

    st.title("📚 Review Queue")
    st.caption("Strengthen your weak areas by revisiting these problems.")

    st.divider()

    if not review_problems:

        st.success("🎉 Amazing!")

        st.info(
            "You have completed every scheduled review."
        )

        st.balloons()

        return

    st.metric(
        "📌 Problems Waiting for Review",
        len(review_problems),
    )

    st.divider()

    # ---------------- Difficulty Mapping ---------------- #

    difficulty_map = {
        "Two Sum": "Easy",
        "Trapping Rain Water": "Hard",
        "Longest Substring Without Repeating Characters": "Medium",
        "Merge Intervals": "Medium",
        "Number of Islands": "Medium",
        "Coin Change": "Medium",
    }

    # ---------------- Recommendation Mapping ---------------- #

    recommendation_map = {
        "Arrays":
            "Focus on HashMap, Two Pointers, and Sliding Window techniques.",

        "Strings":
            "Practice Sliding Window and Frequency Counting problems.",

        "Trees":
            "Strengthen DFS, BFS, and Recursive Traversals.",

        "Graphs":
            "Revise DFS, BFS, and Union-Find concepts.",

        "Dynamic Programming":
            "Write the recurrence relation before coding.",

        "DP":
            "Write the recurrence relation before coding.",
    }

    # ---------------- Cards ---------------- #

    for index, problem in enumerate(review_problems, start=1):

        difficulty = difficulty_map.get(
            problem["problem_title"],
            "Medium",
        )

        recommendation = recommendation_map.get(
            problem["topic"],
            "Focus on understanding the algorithm before optimizing."
        )

        with st.container(border=True):

            header1, header2 = st.columns([4, 1])

            with header1:

                st.subheader(
                    f"{index}. {problem['problem_title']}"
                )

            with header2:

                st.warning("🔄 Due for Review")

            st.write("")

            info1, info2, info3 = st.columns(3)

            with info1:

                st.metric(
                    "🏷 Topic",
                    problem["topic"],
                )

            with info2:

                st.metric(
                    "⚡ Difficulty",
                    difficulty,
                )

            with info3:

                st.metric(
                    "📅 Due",
                    "Today",
                )

            st.info(
                f"""
### 💡 Recommendation

{recommendation}

Try solving the problem **without looking at your previous solution**.

Focus on understanding the **approach**, not memorizing the code.
"""
            )

            button1, button2 = st.columns(2)

            with button1:

                if st.button(
                    "🚀 Solve Again",
                    key=f"solve_{index}",
                    use_container_width=True,
                ):

                    st.success(
                        f"Opening {problem['problem_title']}..."
                    )

            with button2:

                if st.button(
                    "💡 View Hint",
                    key=f"hint_{index}",
                    use_container_width=True,
                ):

                    if problem["topic"] == "Arrays":

                        hint = (
                            "Think about using a HashMap or Two Pointer approach."
                        )

                    elif problem["topic"] == "Strings":

                        hint = (
                            "Consider using a Sliding Window technique."
                        )

                    elif problem["topic"] == "Trees":

                        hint = (
                            "Recursive DFS is usually the cleanest solution."
                        )

                    elif problem["topic"] == "Graphs":

                        hint = (
                            "Can this be solved using DFS or BFS?"
                        )

                    else:

                        hint = (
                            "Break the problem into smaller subproblems before coding."
                        )

                    st.info(f"**Hint:** {hint}")

            st.divider()