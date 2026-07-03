import streamlit as st

st.title("📈 Progress Dashboard")

st.metric("Problems Solved", 42)
st.metric("Accuracy", "78%")
st.metric("Current Streak", "5 Days")

st.divider()

st.subheader("Weak Topics")

st.write("• Graphs")
st.write("• Dynamic Programming")

st.divider()

st.subheader("Today's Goal")

st.success("Solve 3 Graph problems today.")