import streamlit as st
from frontend.state import load_conversations, set_active_conversation, delete_session, rename_session
from frontend.utils import show_error

def render_conversation_list() -> None:
    """
    Renders the scrollable conversation list in the sidebar.
    Supports selecting, renaming, and deleting conversations.
    """
    st.markdown("### Conversations")
    
    # Initialize editing state if not present
    if "editing_thread_id" not in st.session_state:
        st.session_state.editing_thread_id = None

    try:
        conversations = load_conversations()
        if not conversations:
            st.info("No active threads.")
            return

        for conv in conversations:
            conv_id = conv["conversation_id"]
            summary = conv.get("summary") or f"Thread {conv_id[:8]}"
            is_active = (st.session_state.current_thread == conv_id)

            # Check if this thread is being edited
            if st.session_state.editing_thread_id == conv_id:
                # Editing mode
                new_name = st.text_input(
                    "Rename Chat",
                    value=summary,
                    key=f"edit_val_{conv_id}",
                    label_visibility="collapsed"
                )
                
                col_save, col_cancel = st.columns(2)
                with col_save:
                    if st.button("💾 Save", key=f"save_{conv_id}", use_container_width=True):
                        try:
                            rename_session(conv_id, new_name)
                            st.session_state.editing_thread_id = None
                            st.rerun()
                        except Exception as e:
                            show_error(f"Failed to rename: {e}")
                with col_cancel:
                    if st.button("❌", key=f"cancel_{conv_id}", use_container_width=True):
                        st.session_state.editing_thread_id = None
                        st.rerun()
            else:
                # Normal mode
                col_btn, col_edit, col_del = st.columns([0.7, 0.15, 0.15])
                
                with col_btn:
                    btn_type = "primary" if is_active else "secondary"
                    if st.button(summary, key=f"sel_{conv_id}", use_container_width=True, type=btn_type):
                        try:
                            set_active_conversation(conv_id)
                            st.rerun()
                        except Exception as e:
                            show_error(f"Error: {e}")
                            
                with col_edit:
                    if st.button("✏️", key=f"btn_edit_{conv_id}", help="Rename Thread"):
                        st.session_state.editing_thread_id = conv_id
                        st.rerun()
                        
                with col_del:
                    if st.button("🗑️", key=f"btn_del_{conv_id}", help="Delete Thread"):
                        try:
                            delete_session(conv_id)
                            st.rerun()
                        except Exception as e:
                            show_error(f"Error deleting chat: {e}")
            
    except Exception as e:
        st.error(f"Error loading conversation list: {e}")
