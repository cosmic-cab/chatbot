from typing import Dict, Any
from langchain_core.messages import AIMessage, ToolMessage
from agent import init_agent

agent = init_agent()

def run_agent_and_capture_trace(user_prompt: str, thread_id: str) -> Dict[str, Any]:
    config = {"configurable": {"thread_id": thread_id}}
    state = agent.invoke({"messages": [("user", user_prompt)]}, config=config)
    messages = state.get("messages", [])
    
    executed_tools = []
    tool_calls_detail = []
    tool_outputs = []
    final_response = ""
    
    for msg in messages:
        # Capture tool names and their input arguments (e.g., SQL queries, search queries)
        if isinstance(msg, AIMessage) and msg.tool_calls:
            for tc in msg.tool_calls:
                executed_tools.append(tc["name"])
                tool_calls_detail.append({
                    "tool_name": tc["name"],
                    "args": tc.get("args", {})
                })
        
        # Capture raw execution output
        if isinstance(msg, ToolMessage):
            tool_outputs.append({
                "tool_name": msg.name if hasattr(msg, "name") else "unknown_tool",
                "content": msg.content
            })

        if isinstance(msg, AIMessage) and msg.content and not msg.tool_calls:
            final_response = msg.content
            
    return {
        "executed_tools": list(set(executed_tools)),
        "tool_calls_detail": tool_calls_detail,
        "tool_outputs": tool_outputs,
        "final_response": final_response
    }