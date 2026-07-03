import streamlit as st


def render_settings():

    st.title("⚙️ Settings")

    st.divider()

    st.subheader("Preferences")

    theme = st.selectbox(
        "Theme",
        ["Dark", "Light"],
    )

    difficulty = st.selectbox(
        "Preferred Difficulty",
        ["Easy", "Medium", "Hard"],
    )

    notifications = st.toggle(
        "Enable Notifications",
        value=True,
    )

    dev_mode = st.toggle(
        "Development Mode",
        value=True,
    )

    st.divider()

    st.subheader("Account")

    st.button(
        "Clear Chat History",
        use_container_width=True,
    )

    st.button(
        "Reset Progress",
        use_container_width=True,
    )

    st.success("Settings saved automatically.")