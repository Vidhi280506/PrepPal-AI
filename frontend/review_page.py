import streamlit as st
from backend import get_review_queue

def render_review():

    #data = get_review_queue()

    #review_problems = data["due_reviews"]

    try:
        with st.spinner("Loading your review queue..."):
            data = get_review_queue()
            review_problems = data["due_reviews"]

    except Exception as e:
        st.error(" Unable to load your review queue.")
        st.caption(str(e))
        return

    st.title("📚 Review Queue")

    st.caption("Problems you should revisit.")

    st.divider()

    if not review_problems:

        st.success("🎉 Great job!")

        st.info(
            "You have no pending review problems."
        )

        return

    for problem in review_problems:

        with st.container(border=True):

            st.subheader(problem["problem_title"])

            col1, col2 = st.columns(2)

            with col1:
                st.write(f"**Topic:** {problem['topic']}")

            with col2:
                st.write(f"**Status:** Review")

            if st.button(
                f"Solve Again - {problem['problem_title']}",
                use_container_width=True,
            ):
                st.success(
                    f"Opening {problem['problem_title']}..."
                )