"""
Public Opinion Search Toolkit for AI Agents (Tavily)

Version: 1.5
Last Updated: 2025-08-22

This script breaks down complex Tavily search functionality into a series of focused,
minimal-parameter standalone tools designed for AI Agent invocation. Agents only need
to select the appropriate tool based on task intent without understanding complex
parameter combinations. All tools default to searching 'news' (topic='news').

New Features:
- Added `basic_search_news` tool for standard, general news searches.
- Each search result now includes `published_date` (news publication date).

Main Tools:
- basic_search_news: (New) Execute standard, fast general news search.
- deep_search_news: Perform most comprehensive deep analysis of topics.
- search_news_last_24_hours: Get latest developments within 24 hours.
- search_news_last_week: Get major reports from the past week.
- search_images_for_news: Find images related to news topics.
- search_news_by_date: Search within specified historical date range.
"""

import os
import sys
from typing import List, Dict, Any, Optional

# Add utils directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
root_dir = os.path.dirname(os.path.dirname(current_dir))
utils_dir = os.path.join(root_dir, 'utils')
if utils_dir not in sys.path:
    sys.path.append(utils_dir)

from retry_helper import with_graceful_retry, SEARCH_API_RETRY_CONFIG
from dataclasses import dataclass, field

# Before running, ensure Tavily library is installed: pip install tavily-python
try:
    from tavily import TavilyClient
except ImportError:
    raise ImportError("Tavily library not installed, please run `pip install tavily-python` to install.")

# --- 1. Data Structure Definitions ---

@dataclass
class SearchResult:
    """
    Web search result data class
    Contains published_date attribute to store news publication date
    """
    title: str
    url: str
    content: str
    score: Optional[float] = None
    raw_content: Optional[str] = None
    published_date: Optional[str] = None

@dataclass
class ImageResult:
    """Image search result data class"""
    url: str
    description: Optional[str] = None

@dataclass
class TavilyResponse:
    """Encapsulates complete Tavily API return result for passing between tools"""
    query: str
    answer: Optional[str] = None
    results: List[SearchResult] = field(default_factory=list)
    images: List[ImageResult] = field(default_factory=list)
    response_time: Optional[float] = None


# --- 2. Core Client and Specialized Toolset ---

class TavilyNewsAgency:
    """
    A client containing various specialized news public opinion search tools.
    Each public method is designed as a tool for AI Agent independent invocation.
    """

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize client.
        Args:
            api_key: Tavily API key, if not provided it will be read from TAVILY_API_KEY environment variable.
        """
        if api_key is None:
            api_key = os.getenv("TAVILY_API_KEY")
            if not api_key:
                raise ValueError("Tavily API Key not found! Please set TAVILY_API_KEY environment variable or provide during initialization")
        self._client = TavilyClient(api_key=api_key)

    @with_graceful_retry(SEARCH_API_RETRY_CONFIG, default_return=TavilyResponse(query="Search failed"))
    def _search_internal(self, **kwargs) -> TavilyResponse:
        """Internal generic search executor, all tools ultimately call this method"""
        try:
            kwargs['topic'] = 'general'
            api_params = {k: v for k, v in kwargs.items() if v is not None}
            response_dict = self._client.search(**api_params)

            search_results = [
                SearchResult(
                    title=item.get('title'),
                    url=item.get('url'),
                    content=item.get('content'),
                    score=item.get('score'),
                    raw_content=item.get('raw_content'),
                    published_date=item.get('published_date')
                ) for item in response_dict.get('results', [])
            ]

            image_results = [ImageResult(url=item.get('url'), description=item.get('description')) for item in response_dict.get('images', [])]

            return TavilyResponse(
                query=response_dict.get('query'), answer=response_dict.get('answer'),
                results=search_results, images=image_results,
                response_time=response_dict.get('response_time')
            )
        except Exception as e:
            print(f"Error occurred during search: {str(e)}")
            raise e  # Let retry mechanism catch and handle

    # --- Agent-available tool methods ---

    def basic_search_news(self, query: str, max_results: int = 7) -> TavilyResponse:
        """
        [TOOL] Basic News Search: Execute standard, fast news search.
        This is the most commonly used general search tool, suitable when uncertain about specific search needs.
        Agent can provide search query (query) and optional maximum results (max_results).
        """
        print(f"--- TOOL: Basic News Search (query: {query}) ---")
        return self._search_internal(
            query=query,
            max_results=max_results,
            search_depth="basic",
            include_answer=False
        )

    def deep_search_news(self, query: str) -> TavilyResponse:
        """
        [TOOL] Deep News Analysis: Perform the most comprehensive, in-depth search on a topic.
        Returns AI-generated "advanced" detailed summary answer and up to 20 most relevant news results. Suitable for comprehensive understanding of event background.
        Agent only needs to provide search query (query).
        """
        print(f"--- TOOL: Deep News Analysis (query: {query}) ---")
        return self._search_internal(
            query=query, search_depth="advanced", max_results=20, include_answer="advanced"
        )

    def search_news_last_24_hours(self, query: str) -> TavilyResponse:
        """
        [TOOL] Search News Last 24 Hours: Get latest developments on a topic.
        This tool specifically finds news published within the past 24 hours. Suitable for tracking breaking events or latest developments.
        Agent only needs to provide search query (query).
        """
        print(f"--- TOOL: Search News Last 24 Hours (query: {query}) ---")
        return self._search_internal(query=query, time_range='d', max_results=10)

    def search_news_last_week(self, query: str) -> TavilyResponse:
        """
        [TOOL] Search News Last Week: Get major news reports from the past week on a topic.
        Suitable for weekly public opinion summary or review.
        Agent only needs to provide search query (query).
        """
        print(f"--- TOOL: Search News Last Week (query: {query}) ---")
        return self._search_internal(query=query, time_range='w', max_results=10)

    def search_images_for_news(self, query: str) -> TavilyResponse:
        """
        [TOOL] Search Images for News: Search for images related to a news topic.
        This tool returns image links and descriptions, suitable for scenarios requiring illustrations for reports or articles.
        Agent only needs to provide search query (query).
        """
        print(f"--- TOOL: Search Images for News (query: {query}) ---")
        return self._search_internal(
            query=query, include_images=True, include_image_descriptions=True, max_results=5
        )

    def search_news_by_date(self, query: str, start_date: str, end_date: str) -> TavilyResponse:
        """
        [TOOL] Search News by Date Range: Search news within a specific historical time period.
        This is the only tool requiring Agent to provide detailed time parameters. Suitable for analyzing specific historical events.
        Agent needs to provide query (query), start date (start_date) and end date (end_date), all in 'YYYY-MM-DD' format.
        """
        print(f"--- TOOL: Search News by Date Range (query: {query}, from: {start_date}, to: {end_date}) ---")
        return self._search_internal(
            query=query, start_date=start_date, end_date=end_date, max_results=15
        )


# --- 3. Testing and Usage Examples ---

def print_response_summary(response: TavilyResponse):
    """Simplified print function to display test results, now shows publication date"""
    if not response or not response.query:
        print("Failed to get valid response.")
        return

    print(f"\nQuery: '{response.query}' | Time: {response.response_time}s")
    if response.answer:
        print(f"AI Summary: {response.answer[:120]}...")
    print(f"Found {len(response.results)} webpages, {len(response.images)} images.")
    if response.results:
        first_result = response.results[0]
        date_info = f"(Published: {first_result.published_date})" if first_result.published_date else ""
        print(f"First result: {first_result.title} {date_info}")
    print("-" * 60)


if __name__ == "__main__":
    # Before running, please ensure you have set the TAVILY_API_KEY environment variable

    try:
        # Initialize "news agency" client, which internally contains all tools
        agency = TavilyNewsAgency()

        # Scenario 1: Agent performs a regular, fast search
        response1 = agency.basic_search_news(query="Latest Olympic Games results", max_results=5)
        print_response_summary(response1)

        # Scenario 2: Agent needs comprehensive understanding of "Global chip technology competition" background
        response2 = agency.deep_search_news(query="Global chip technology competition")
        print_response_summary(response2)

        # Scenario 3: Agent needs to track latest news on "GTC Conference"
        response3 = agency.search_news_last_24_hours(query="Nvidia GTC Conference latest announcement")
        print_response_summary(response3)

        # Scenario 4: Agent needs to find material for a weekly report on "autonomous driving"
        response4 = agency.search_news_last_week(query="Autonomous driving commercial deployment")
        print_response_summary(response4)

        # Scenario 5: Agent needs to find news images of "Webb Space Telescope"
        response5 = agency.search_images_for_news(query="Webb Space Telescope latest discoveries")
        print_response_summary(response5)

        # Scenario 6: Agent needs to research Q1 2025 news on "AI regulations"
        response6 = agency.search_news_by_date(
            query="AI regulations",
            start_date="2025-01-01",
            end_date="2025-03-31"
        )
        print_response_summary(response6)

    except ValueError as e:
        print(f"Initialization failed: {e}")
        print("Please ensure TAVILY_API_KEY environment variable is correctly set.")
    except Exception as e:
        print(f"Unknown error occurred during testing: {e}")