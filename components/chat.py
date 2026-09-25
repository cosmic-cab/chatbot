import streamlit as st
from components.trace import render_trace_steps


def render_chat_interface(agent_executor):
    """Renders existing message history and handles new user chat inputs."""
    # Render past conversation history
    for chat in st.session_state.messages:
        with st.chat_message("user"):
            st.markdown(chat["user_input"])

        with st.chat_message("assistant"):
            if chat.get("trace"):
                render_trace_steps(chat["trace"])
            st.markdown(chat["final_answer"])

    # Render input field and process active requests
    if prompt := st.chat_input("Ask a question..."):
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Processing request..."):
                try:
                    config = {
                        "configurable": {
                            "thread_id": st.session_state.thread_id
                        }
                    }

                    response = agent_executor.invoke(
                        {"messages": [("user", prompt)]}, config=config
                    )

                    all_messages = response.get("messages", [])

                    # Find where the latest user prompt appears in history
                    latest_user_idx = max(
                        i for i, m in enumerate(all_messages) 
                        if getattr(m, "type", None) == "human" or getattr(m, "role", None) == "user"
                    )

                    # Extract only current turn's messages (excluding the user's input prompt itself)
                    current_turn_steps = all_messages[latest_user_idx + 1 :]

                    final_answer = (
                        current_turn_steps[-1].content
                        if current_turn_steps
                        else "No response generated."
                    )

                    render_trace_steps(current_turn_steps)
                    st.markdown(final_answer)

                    st.session_state.messages.append(
                        {
                            "user_input": prompt,
                            "final_answer": final_answer,
                            "trace": current_turn_steps, # Store only this turn's intermediate steps
                        }
                    )

                except Exception as e:
                    st.error(f"An error occurred: {str(e)}")