import streamlit as st

from frontend.components.conversation_list import render_conversation_list
from frontend.components.settings import render_settings
from frontend.state import create_new_session
from frontend.utils import show_error


def render_sidebar() -> None:
    """
    Renders the sidebar layout consisting of the logo, New Conversation button,
    conversation list, and settings selectors.
    """
    with st.sidebar:
        # 1. AgentFlow logo
        st.title("🧠 AgentFlow")
        st.subheader("Autonomous AI Assistant")
        st.markdown("---")

        # 2. New Conversation button
        if st.button("➕ New Conversation", use_container_width=True, type="primary"):
            try:
                create_new_session()
                st.rerun()
            except Exception as e:
                show_error(f"Could not create new conversation: {e}")

        st.markdown("---")

        # 3. Conversation history list
        render_conversation_list()

        st.markdown("---")

        # 4. Settings section (Model Provider and Temperature)
        render_settings()
