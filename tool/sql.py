import psycopg2
from psycopg2.extras import RealDictCursor
from langchain_core.tools import tool

DB_CONFIG = {
    "dbname": "mydatabase",
    "user": "myuser",
    "password": "mypassword",
    "host": "localhost",
    "port": "5432"
}

def get_db_connection():
    """Establishes and returns a database connection."""
    return psycopg2.connect(**DB_CONFIG)

@tool
def execute_sql_query(query: str) -> str:
    """
    Executes a PostgreSQL SELECT query against the database and returns the result.
    Use this tool whenever you need data about provinces, weather, roads, railways, ports, or land use.
    Input must be a valid SELECT SQL query.
    """
    cleaned_query = query.strip()
    if not cleaned_query.lower().startswith("select"):
        return "Error: Security constraint. Only SELECT queries are allowed."

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        cursor.execute(cleaned_query)
        results = cursor.fetchall()
        cursor.close()
        conn.close()

        if not results:
            return "Query executed successfully, but returned no results."

        return str(results)
    except Exception as e:
        return f"Database Error: {str(e)}"