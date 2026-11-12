import streamlit as st

from components.sidebar_chat import render_chat_sidebar
from components.chat_ui import render_chat_ui

# ==========================================================
# Page Configuration
# ==========================================================
st.set_page_config(
    page_title="Medical Chat",
    page_icon="💬",
    layout="wide",
)

# ==========================================================
# Validate Upload Session
# ==========================================================
if "session_id" not in st.session_state:
    st.error("No active upload session found.")

    if st.button("← Return to Home"):
        st.switch_page("app.py")

    st.stop()

# ==========================================================
# Sidebar
# ==========================================================
render_chat_sidebar()

# ==========================================================
# Page Header
# ==========================================================
st.title("💬 Medical AI Assistant")
st.caption("Your AI-powered assistant for analyzing uploaded medical reports.")
st.markdown("---")

# ==========================================================
# Chat Interface
# ==========================================================
render_chat_ui()
