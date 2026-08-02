import streamlit as st

def render_settings() -> None:
    """
    Renders Model Provider selectbox and Temperature slider settings.
    Uses st.session_state keys directly to avoid warnings.
    """
    st.markdown("### Settings")
    
    st.selectbox(
        "Model Provider",
        options=["openai", "gemini"],
        key="provider"
    )
    
    st.slider(
        "Temperature",
        min_value=0.0,
        max_value=1.0,
        step=0.1,
        key="temperature"
    )
