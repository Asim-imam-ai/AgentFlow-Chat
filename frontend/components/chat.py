import time

import streamlit as st

from frontend.components.uploader import render_attachment_chips, render_uploader
from frontend.services.api import AgentFlowAPI
from frontend.state import create_new_session, load_conversations
from frontend.utils import show_error


def simulate_streaming(text: str) -> None:
    """
    Simulate a word-by-word streaming typing effect for assistant responses.
    """
    message_placeholder = st.empty()
    full_response = ""
    for chunk in text.split(" "):
        full_response += chunk + " "
        message_placeholder.markdown(full_response + "▌")
        time.sleep(0.02)
    message_placeholder.markdown(full_response)


def render_chat() -> None:
    """
    Renders the central chat area, displaying conversation history,
    thinking status indicator, removable attachment chips, and the chat input box.
    """
    active_id = st.session_state.current_thread
    summary = "New Chat"

    # Resolve the active conversation summary
    if active_id:
        conversations = load_conversations()
        for c in conversations:
            if c["conversation_id"] == active_id:
                summary = c.get("summary") or f"Thread {active_id[:8]}"
                break

        st.subheader(f"💬 {summary}")
        st.markdown("---")
    else:
        st.subheader("🤖 Start a Conversation")
        st.info("Select a thread in the sidebar or send a message below to begin.")
        st.markdown("---")

    # Render message history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Process pending input if any
    pending_input = st.session_state.get("pending_input", None)
    if pending_input:
        response_text = ""
        try:
            # 1. Create a session/thread if not active
            if not st.session_state.current_thread:
                try:
                    create_new_session()
                except Exception as e:
                    st.session_state.pending_input = None
                    st.session_state.generating = False
                    show_error(f"Failed to create session: {e}")
                    st.rerun()
                    return

            provider = st.session_state.get("provider", "openai")
            temp = st.session_state.get("temperature", 0.7)
            conv_id = st.session_state.current_thread

            # 2. Show assistant thinking message
            with st.chat_message("assistant"):
                with st.spinner("AgentFlow is thinking..."):
                    # Pass the attached files summary to the agent if any (RAG)
                    # We can construct a message details object or let backend handle uploaded files context
                    # Backend reads uploaded files directly from its upload folder for matching.
                    data = AgentFlowAPI.send_chat(
                        message=pending_input,
                        conversation_id=conv_id,
                        provider=provider,
                        temperature=temp,
                    )
                    response_text = data.get("response", "")

                    if data.get("conversation_id"):
                        st.session_state.current_thread = data["conversation_id"]
                        st.session_state.selected_conversation = data["conversation_id"]

                    # Update local caches with summary changes
                    if data.get("summary"):
                        # Save in list cache
                        conversations = load_conversations()
                        for c in conversations:
                            if c["conversation_id"] == conv_id:
                                c["summary"] = data["summary"]
                                break

            # 3. Simulate streaming/typing
            with st.chat_message("assistant"):
                simulate_streaming(response_text)

            # 4. Save response to state
            st.session_state.messages.append(
                {"role": "assistant", "content": response_text}
            )

            # Update history cache
            if conv_id in st.session_state.history_cache:
                st.session_state.history_cache[conv_id]["messages"] = (
                    st.session_state.messages
                )
                if data.get("summary"):
                    st.session_state.history_cache[conv_id]["summary"] = data["summary"]

        except Exception as e:
            show_error(f"Error communicating with backend: {e}")
        finally:
            st.session_state.pending_input = None
            st.session_state.generating = False
            st.session_state.uploaded_files = []  # Clear attachments on success
            st.rerun()

    # Layout for attachment chips and uploader above chat input
    if active_id:
        render_attachment_chips()
        render_uploader()

    # User chat input
    generating = st.session_state.get("generating", False)
    user_input = st.chat_input("Ask AgentFlow...", disabled=generating)

    if user_input and not generating:
        st.session_state.generating = True
        st.session_state.pending_input = user_input
        st.session_state.messages.append({"role": "user", "content": user_input})
        st.rerun()
