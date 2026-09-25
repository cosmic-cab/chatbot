import os
from dotenv import load_dotenv
from langchain.agents import create_agent
from langchain_deepseek import ChatDeepSeek
from langgraph.checkpoint.memory import MemorySaver

from prompt.prompt import SYSTEM_PROMPT
from tool import ALL_TOOLS

# Load environment variables
load_dotenv()


def init_agent():
    """Instantiates and returns the configured agent executor with memory checkpointer.

    Raises:
        ValueError: If DEEPSEEK_API_KEY is not configured in environment variables.
    """
    if not os.getenv("DEEPSEEK_API_KEY"):
        raise ValueError("DEEPSEEK_API_KEY is missing from environment variables.")

    llm = ChatDeepSeek(model="deepseek-chat", temperature=0)

    # MemorySaver keeps track of state keyed by thread_id
    checkpointer = MemorySaver()

    agent = create_agent(
        model=llm,
        tools=ALL_TOOLS,
        system_prompt=SYSTEM_PROMPT,
        checkpointer=checkpointer,
    )
    return agent