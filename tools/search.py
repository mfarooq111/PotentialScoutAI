from tavily import TavilyClient

from config import settings


tavily_client = TavilyClient(
    api_key=settings.TAVILY_API_KEY
)


def search_web(query: str, max_results: int = 5):
    response = tavily_client.search(
        query=query,
        search_depth="basic",
        max_results=max_results
    )

    return response.get("results", [])


import json
from langchain_core.tools import tool


@tool
def web_search_tool(query: str, max_results: int = 5) -> str:
    """Search the web for company information, services, products, and business opportunities."""

    results = search_web(query, max_results)

    return json.dumps(results, ensure_ascii=False, indent=2)