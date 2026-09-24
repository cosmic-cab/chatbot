import json
import os
import streamlit as st
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek

from prompt.prompt import SYSTEM_PROMPT
# Import the centralized tool registry
from tool import ALL_TOOLS

# -----------------------------------------------------------------------------
# 1. Configuration & Agent Initialization
# -----------------------------------------------------------------------------
st.set_page_config(
    page_title="Multi-Tool Chatbot with Trace Logs",
    page_icon="🤖",
    layout="wide",
)

load_dotenv()


@st.cache_resource
def get_agent_executor():
  """Cache the agent setup across reruns."""
  if not os.getenv("DEEPSEEK_API_KEY"):
    st.error("DEEPSEEK_API_KEY is missing from environment variables.")
    st.stop()

  llm = ChatDeepSeek(model="deepseek-chat", temperature=0)

  # Pass ALL_TOOLS directly
  agent = create_agent(model=llm, tools=ALL_TOOLS, system_prompt=SYSTEM_PROMPT)
  return agent


agent_executor = get_agent_executor()

# -----------------------------------------------------------------------------
# 2. Session State Initialization & Sidebar
# -----------------------------------------------------------------------------
if "messages" not in st.session_state:
  st.session_state.messages = []

st.title("🤖 AI Assistant")
st.caption("Ask questions and execute tools automatically.")

with st.sidebar:
  st.header("Settings & Tools")
  if st.button("🗑️ Clear Chat History", use_container_width=True):
    st.session_state.messages = []
    st.rerun()

  st.markdown("---")
  st.markdown("### Available Tools")

  # Dynamically list all available tools safely
  for tool in ALL_TOOLS:
    # Safely get the tool name (StructuredTool uses .name, raw functions use .__name__)
    tool_name = getattr(tool, "name", None) or getattr(
        tool, "__name__", "Unnamed Tool"
    )
    tool_desc = getattr(tool, "description", "No description provided.")

    with st.expander(f"🛠️ `{tool_name}`"):
      st.caption(tool_desc)

# -----------------------------------------------------------------------------
# 3. Dynamic Trace Renderer
# -----------------------------------------------------------------------------
def render_trace_steps(messages):
  """Formats system prompts, AI reasoning, tool calls, and tool outputs dynamically."""
  for idx, msg in enumerate(messages):

    # System Prompt Trace
    if msg.type == "system":
      with st.expander(f"⚙️ Step {idx}: System Prompt", expanded=False):
        st.code(msg.content, language="markdown")

    # AI Thought / Action
    elif msg.type == "ai":
      if hasattr(msg, "tool_calls") and msg.tool_calls:
        for tool_call in msg.tool_calls:
          tool_name = tool_call.get("name", "Unknown Tool")
          tool_args = tool_call.get("args", {})

          with st.expander(
              f"🔧 Step {idx}: Tool Call -> `{tool_name}`", expanded=True
          ):
            st.markdown("**Arguments:**")
            # Generic rendering for any tool's arguments
            _render_generic_payload(tool_args)

      # AI reasoning text before final answer
      if msg.content and idx != len(messages) - 1:
        with st.expander(
            f"🧠 Step {idx}: AI Reasoning", expanded=False
        ):
          st.write(msg.content)

    # Tool Output Response
    elif msg.type == "tool":
      tool_name = getattr(msg, "name", "Tool")
      with st.expander(
          f"📥 Step {idx}: Tool Result (`{tool_name}`)", expanded=False
      ):
        # Try JSON parsing first, fallback to text/code block
        try:
          payload = (
              json.loads(msg.content)
              if isinstance(msg.content, str)
              else msg.content
          )
          st.json(payload)
        except Exception:
          st.code(str(msg.content), language="text")


def _render_generic_payload(payload):
  """Helper to cleanly render any tool payload dynamically."""
  if isinstance(payload, dict):
    # Detect code-like values (e.g., SQL queries, Python scripts)
    for key, val in payload.items():
      if isinstance(val, str) and ("SELECT" in val.upper() or "\n" in val):
        st.markdown(f"**`{key}`:**")
        st.code(
            val,
            language="sql" if "SELECT" in val.upper() else "text",
        )
      else:
        st.json({key: val})
  else:
    st.json(payload)


# -----------------------------------------------------------------------------
# 4. Render Conversation History & User Input
# -----------------------------------------------------------------------------
for chat in st.session_state.messages:
  with st.chat_message("user"):
    st.markdown(chat["user_input"])

  with st.chat_message("assistant"):
    if chat.get("trace"):
      render_trace_steps(chat["trace"])
    st.markdown(chat["final_answer"])

if prompt := st.chat_input("Ask a question..."):
  with st.chat_message("user"):
    st.markdown(prompt)

  with st.chat_message("assistant"):
    with st.spinner("Processing request..."):
      try:
        response = agent_executor.invoke({"messages": [("user", prompt)]})
        all_messages = response.get("messages", [])

        final_answer = (
            all_messages[-1].content if all_messages else "No response generated."
        )

        render_trace_steps(all_messages)
        st.markdown(final_answer)

        st.session_state.messages.append({
            "user_input": prompt,
            "final_answer": final_answer,
            "trace": all_messages,
        })

      except Exception as e:
        st.error(f"An error occurred: {str(e)}")