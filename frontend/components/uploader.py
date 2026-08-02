import time

import streamlit as st

from frontend.services.api import AgentFlowAPI
from frontend.utils import show_error


def render_uploader() -> None:
    """
    Renders the document uploader within the chat area.
    Presents a button/popover for file selection, shows upload progress,
    and updates the active thread's attachments.
    """
    with st.popover("📎 Ingest Document"):
        uploaded_file = st.file_uploader(
            "Select TXT, MD, CSV, or PDF",
            type=["txt", "md", "csv", "pdf"],
            key="chat_file_uploader",
            label_visibility="visible",
        )

        if uploaded_file is not None:
            file_key = f"uploaded_{uploaded_file.name}_{uploaded_file.size}"
            if file_key not in st.session_state:
                # Ingest document and show progress bar
                progress_bar = st.progress(0, text="Uploading document...")
                for percent in range(1, 101, 20):
                    time.sleep(0.05)
                    progress_bar.progress(percent, text=f"Uploading... {percent}%")

                try:
                    file_bytes = uploaded_file.read()
                    conversation_id = st.session_state.get("current_thread")
                    res = AgentFlowAPI.upload_file(
                        file_bytes,
                        uploaded_file.name,
                        conversation_id=conversation_id,
                    )
                    progress_bar.progress(100, text="Upload successful!")
                    st.session_state[file_key] = True

                    if uploaded_file.name not in st.session_state.uploaded_files:
                        st.session_state.uploaded_files.append(uploaded_file.name)
                        chunks = res.get("chunks", "?")
                        st.toast(
                            f"✅ Indexed {uploaded_file.name} ({chunks} chunks) into this conversation!"
                        )

                    time.sleep(0.5)
                    st.rerun()
                except Exception as e:
                    progress_bar.empty()
                    show_error(f"Ingestion failed: {e}")


def render_attachment_chips() -> None:
    """
    Displays attachment chips representing files staged to be sent or indexed.
    Allows users to remove attachments before sending messages.
    """
    if st.session_state.uploaded_files:
        st.markdown("** st.session_state attachments:**")
        cols = st.columns(len(st.session_state.uploaded_files))
        for idx, filename in enumerate(list(st.session_state.uploaded_files)):
            with cols[idx]:
                st.info(f"📄 {filename}")
                if st.button(
                    "✕ Remove",
                    key=f"del_file_{filename}",
                    help="Remove attachment",
                    use_container_width=True,
                ):
                    st.session_state.uploaded_files.remove(filename)
                    st.rerun()
