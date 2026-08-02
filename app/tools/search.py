import logging

from langchain_core.tools import tool
from tavily import TavilyClient

from app.core.settings import settings
from app.tools.registry import tool_registry

logger = logging.getLogger("agentflow.tools.search")


@tool("web_search")
def search_tool(query: str) -> str:
    """
    Search the web for up-to-date information, news, fact-checking, or details on any topic.
    """
    if not settings.TAVILY_API_KEY:
        return "Error: Tavily Web Search API key is not configured. Please set TAVILY_API_KEY."

    try:
        client = TavilyClient(api_key=settings.TAVILY_API_KEY)
        logger.info(f"Running web search for: '{query}'")
        response = client.search(query=query, max_results=3)

        results = response.get("results", [])
        if not results:
            return f"No search results found for query: '{query}'"

        formatted_results = []
        for r in results:
            title = r.get("title", "No Title")
            url = r.get("url", "No URL")
            content = r.get("content", "No Content")
            formatted_results.append(
                f"Title: {title}\nURL: {url}\nContent: {content}\n"
            )

        return "\n---\n".join(formatted_results)
    except Exception as e:
        logger.error(f"Tavily search failed: {e}")
        return f"Web search failed due to error: {e!s}"


# Register tool
tool_registry.register(search_tool)
