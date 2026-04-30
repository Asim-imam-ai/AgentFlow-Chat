from tavily import TavilyClient
from config.settings import settings
import logging
from typing import Dict, Any, List

# Setup basic logging
logger = logging.getLogger(__name__)


class TavilySearch:
    """
    Wrapper class for Tavily Search API.
    Handles API calls, errors, and response formatting.
    """

    def __init__(self):
        if not settings.TAVILY_API_KEY:
            raise ValueError("❌ TAVILY_API_KEY is missing in settings")

        self.client = TavilyClient(api_key=settings.TAVILY_API_KEY)

    def search(self,query: str,max_results: int = 5,include_answer: bool = True) -> Dict[str, Any]:
        """
        Perform a web search using Tavily.
        Args:
            query (str): Search query
            max_results (int): Number of results to return
            include_answer (bool): Include summarized answer

        Returns:
            Dict: Cleaned search response
        """

        try:
            logger.info(f"🔍 Tavily search query: {query}")

            response = self.client.search(
                query=query,
                max_results=max_results,
                include_answer=include_answer,
            )

            return self._format_response(response)

        except Exception as e:
            logger.error(f"❌ Tavily search failed: {str(e)}")
            return {
                "query": query,
                "answer": "Error fetching search results",
                "results": [],
                "error": str(e),
            }

    def _format_response(self, response: Dict[str, Any]) -> Dict[str, Any]:
        """
        Clean and standardize Tavily response
        """

        results: List[Dict[str, Any]] = []

        for item in response.get("results", []):
            results.append({
                "title": item.get("title"),
                "url": item.get("url"),
                "content": item.get("content"),
            })

        return {
            "query": response.get("query"),
            "answer": response.get("answer"),
            "results": results,
        }


# Singleton instance (recommended for reuse)
tavily_client = TavilySearch()


# Simple function interface (for agents/tools)
def tavily_search(query: str) -> Dict[str, Any]:
    """
    Public function to be used by agents or LangChain tools.
    """
    return tavily_client.search(query)