import streamlit as st

from frontend.components.chat import render_chat
from frontend.components.sidebar import render_sidebar
from frontend.services.api import AgentFlowAPI
from frontend.state import init_session_state, load_conversations

# Set page config for a widescreen layout resembling ChatGPT/Claude
st.set_page_config(
    page_title="AgentFlow - Professional AI Chat Dashboard",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 1. Initialize Session State Variables
init_session_state()

# 2. Pre-load conversation list into session state cache for instant rendering
load_conversations()

# 3. Render Sidebar components (logo, buttons, conversations list, and settings)
render_sidebar()

# 4. Verify Backend Connection
health = AgentFlowAPI.get_health()
if health.get("status") == "unhealthy":
    st.error(
        "🚨 AgentFlow Backend server is unreachable! Please start the FastAPI backend service."
    )

# 5. Render main application chat window
render_chat()
