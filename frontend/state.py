import logging
from typing import Any

import streamlit as st

from frontend.services.api import AgentFlowAPI

logger = logging.getLogger("agentflow.frontend.state")


def init_session_state() -> None:
    """
    Initialize all Streamlit session state variables if they do not exist.
    """
    if "current_thread" not in st.session_state:
        st.session_state.current_thread = None
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "conversation_list" not in st.session_state:
        st.session_state.conversation_list = None
    if "selected_conversation" not in st.session_state:
        st.session_state.selected_conversation = None
    if "uploaded_files" not in st.session_state:
        st.session_state.uploaded_files = []  # Current thread's pending/uploaded files list
    if "provider" not in st.session_state:
        st.session_state.provider = "openai"
    if "temperature" not in st.session_state:
        st.session_state.temperature = 0.7
    if "history_cache" not in st.session_state:
        st.session_state.history_cache = {}  # Cache mapping thread_id -> {messages, summary}
    if "generating" not in st.session_state:
        st.session_state.generating = False
    if "pending_input" not in st.session_state:
        st.session_state.pending_input = None


def load_conversations(force_refresh: bool = False) -> list[dict[str, Any]]:
    """
    Load the conversation list from the backend (or session state cache if available).
    """
    if st.session_state.conversation_list is None or force_refresh:
        try:
            conversations = AgentFlowAPI.get_conversations()
            st.session_state.conversation_list = conversations
        except Exception as e:
            logger.error(f"Error loading conversations: {e}")
            st.session_state.conversation_list = []
    return st.session_state.conversation_list


def set_active_conversation(conversation_id: str) -> None:
    """
    Selects a conversation, loads its history (using cache or API), and sets the active session.
    """
    st.session_state.current_thread = conversation_id
    st.session_state.selected_conversation = conversation_id
    st.session_state.uploaded_files = []  # Reset files for the new thread

    # Use cache if available to make loading instantaneous
    if conversation_id in st.session_state.history_cache:
        cached = st.session_state.history_cache[conversation_id]
        st.session_state.messages = cached["messages"]
        st.session_state.summary = cached.get("summary")
        logger.info(f"Loaded conversation {conversation_id} history from cache.")
    else:
        try:
            data = AgentFlowAPI.get_history(conversation_id)
            messages = [
                {"role": msg["role"], "content": msg["content"]}
                for msg in data.get("messages", [])
                if msg["role"] not in ("system", "tool")
            ]
            summary = data.get("summary")
            st.session_state.messages = messages
            st.session_state.summary = summary

            # Cache it
            st.session_state.history_cache[conversation_id] = {
                "messages": messages,
                "summary": summary,
            }
            logger.info(f"Fetched and cached conversation {conversation_id} history.")
        except Exception as e:
            st.session_state.messages = []
            st.session_state.summary = None
            logger.error(f"Error loading thread history: {e}")
            raise RuntimeError(f"Error loading thread history: {e}")


def create_new_session() -> str:
    """
    Creates a new conversation thread, initializes its state, and updates the cache instantly.
    """
    try:
        new_id = AgentFlowAPI.create_thread()
        if new_id:
            st.session_state.current_thread = new_id
            st.session_state.selected_conversation = new_id
            st.session_state.messages = []
            st.session_state.summary = None
            st.session_state.uploaded_files = []

            # Initialize empty history cache
            st.session_state.history_cache[new_id] = {"messages": [], "summary": None}

            # Update conversation list cache instantly
            new_conv = {
                "conversation_id": new_id,
                "message_count": 0,
                "summary": "New Chat",
            }
            if st.session_state.conversation_list is None:
                st.session_state.conversation_list = [new_conv]
            else:
                st.session_state.conversation_list.insert(0, new_conv)

            return new_id
        else:
            raise RuntimeError("Backend did not return thread_id.")
    except Exception as e:
        logger.error(f"Could not generate a new thread: {e}")
        raise RuntimeError(f"Could not generate a new thread: {e}")


def delete_session(conversation_id: str) -> None:
    """
    Deletes a conversation session, removes it from cache, and resets active state if deleted.
    """
    try:
        AgentFlowAPI.delete_thread(conversation_id)

        # Remove from local list cache
        if st.session_state.conversation_list:
            st.session_state.conversation_list = [
                c
                for c in st.session_state.conversation_list
                if c["conversation_id"] != conversation_id
            ]

        # Remove from history cache
        if conversation_id in st.session_state.history_cache:
            del st.session_state.history_cache[conversation_id]

        # Reset current thread if it was the one deleted
        if st.session_state.current_thread == conversation_id:
            st.session_state.current_thread = None
            st.session_state.selected_conversation = None
            st.session_state.messages = []
            st.session_state.summary = None
            st.session_state.uploaded_files = []
    except Exception as e:
        logger.error(f"Failed to delete thread: {e}")
        raise RuntimeError(f"Failed to clear thread: {e}")


def rename_session(conversation_id: str, summary: str) -> None:
    """
    Renames a conversation thread, updating both the backend and local state caches.
    """
    try:
        AgentFlowAPI.rename_thread(conversation_id, summary)

        # Update list cache
        if st.session_state.conversation_list:
            for c in st.session_state.conversation_list:
                if c["conversation_id"] == conversation_id:
                    c["summary"] = summary
                    break

        # Update history cache summary
        if conversation_id in st.session_state.history_cache:
            st.session_state.history_cache[conversation_id]["summary"] = summary

        # Update current summary if active
        if st.session_state.current_thread == conversation_id:
            st.session_state.summary = summary
    except Exception as e:
        logger.error(f"Failed to rename thread: {e}")
        raise RuntimeError(f"Failed to rename thread: {e}")
