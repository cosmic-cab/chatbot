# tool/web_search.py
from ddgs import DDGS
from langchain_core.tools import tool

@tool
def web_search_tool(query: str, max_results: int = 5) -> str:
    """
    Searches the live web using DuckDuckGo to get up-to-date information, news, or general real-time facts.
    Use this tool when the information is not stored in the database or requires recent external context.
    """
    try:
        results = []
        with DDGS() as ddgs:
            # text search using ddgs
            search_results = ddgs.text(query, max_results=max_results)
            for r in search_results:
                results.append(f"Title: {r.get('title')}\nURL: {r.get('href')}\nSnippet: {r.get('body')}\n")

        if not results:
            return "No web search results found for the query."

        return "\n---\n".join(results)
    except Exception as e:
        return f"Web Search Error: {str(e)}"