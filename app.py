import uuid
import streamlit as st

from agent import init_agent
from components.chat import render_chat_interface
from components.sidebar import render_sidebar

# Page config must remain at the top level
st.set_page_config(
    page_title="Multi-Tool Chatbot with Trace Logs",
    page_icon="🤖",
    layout="wide",
)


@st.cache_resource
def get_agent_executor():
    """Cache the agent setup across Streamlit reruns."""
    try:
        return init_agent()
    except ValueError as e:
        st.error(str(e))
        st.stop()


agent_executor = get_agent_executor()

# Session State Initialization
if "messages" not in st.session_state:
    st.session_state.messages = []

if "thread_id" not in st.session_state:
    st.session_state.thread_id = str(uuid.uuid4())

st.title("🤖 AI Assistant")
st.caption("Ask questions and execute tools automatically.")

# Render UI Modules
render_sidebar()
render_chat_interface(agent_executor)