import uuid
import streamlit as st
from tool import ALL_TOOLS


def render_sidebar():
    """Renders the settings, thread info, and available tools sidebar."""
    with st.sidebar:
        st.header("Settings & Tools")

        # Display current session Thread ID
        st.caption(
            f"**Session Thread ID:** `{st.session_state.thread_id[:8]}...`"
        )

        if st.button("🗑️ Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.session_state.thread_id = str(uuid.uuid4())
            st.rerun()

        st.markdown("---")
        st.markdown("### Available Tools")

        for tool in ALL_TOOLS:
            tool_name = getattr(tool, "name", None) or getattr(
                tool, "__name__", "Unnamed Tool"
            )
            tool_desc = getattr(
                tool, "description", "No description provided."
            )

            with st.expander(f"🛠️ `{tool_name}`"):
                st.caption(tool_desc)