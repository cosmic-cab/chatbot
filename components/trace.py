import json
import streamlit as st


def _render_generic_payload(payload):
    if isinstance(payload, dict):
        for key, val in payload.items():
            if isinstance(val, str) and (
                "SELECT" in val.upper() or "\n" in val
            ):
                st.markdown(f"**`{key}`:**")
                st.code(
                    val,
                    language="sql" if "SELECT" in val.upper() else "text",
                )
            else:
                st.json({key: val})
    else:
        st.json(payload)

# trace.py

def render_trace_steps(messages):
    """Formats system prompts, AI reasoning, tool calls, and tool outputs dynamically."""
    total_msgs = len(messages)
    for idx, msg in enumerate(messages):
        # System Prompt Trace
        if msg.type == "system":
            with st.expander(f"⚙️ Step {idx}: System Prompt", expanded=False):
                st.code(msg.content, language="markdown")

        # AI Thought / Action
        elif msg.type == "ai":
            # 1. Tool Call Expander
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                for tool_call in msg.tool_calls:
                    tool_name = tool_call.get("name", "Unknown Tool")
                    tool_args = tool_call.get("args", {})

                    with st.expander(
                        f"🔧 Step {idx}: Tool Call -> `{tool_name}`",
                        expanded=True,
                    ):
                        st.markdown("**Arguments:**")
                        _render_generic_payload(tool_args)

            # 2. Reasoning Expander (Skip if this is the final message in the turn)
            is_last_message = (idx == total_msgs - 1)
            if msg.content and not is_last_message:
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
                try:
                    payload = (
                        json.loads(msg.content)
                        if isinstance(msg.content, str)
                        else msg.content
                    )
                    st.json(payload)
                except Exception:
                    st.code(str(msg.content), language="text")