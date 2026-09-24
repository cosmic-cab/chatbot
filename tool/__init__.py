# tool/__init__.py
from tool.sql import execute_sql_query
from tool.web import web_search_tool
# from tool.calculator import calculate_statistics

# Export all active tools in a single list
ALL_TOOLS = [
    execute_sql_query,
    web_search_tool,
    # calculate_statistics,
]