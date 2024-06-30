from crewai_tools import (
    ScrapeWebsiteTool,
    MDXSearchTool,
    SerperDevTool,
    YoutubeVideoSearchTool,
)

class SearchAndScrapeTools:
    """
    A class to initialize and manage various search and scraping tools.
    """

    def __init__(self):
        """
        Initialize all the search and scraping tools.
        """
        self.search_tool = self.create_search_tool()
        self.scrape_tool = self.create_scrape_tool()
        self.youtube_video_search_tool = self.create_youtube_video_search_tool()
        self.market_data_extraction_search_tool = self.create_market_data_extraction_search_tool()

    def create_search_tool(self):
        """
        Create a general search tool using SerperDevTool.

        Returns:
            SerperDevTool: An instance of SerperDevTool for general search.
        """
        return SerperDevTool()

    def create_scrape_tool(self):
        """
        Create a tool to scrape websites.

        Returns:
            ScrapeWebsiteTool: An instance of ScrapeWebsiteTool for scraping websites.
        """
        return ScrapeWebsiteTool()

    def create_youtube_video_search_tool(self):
        """
        Create a tool to search YouTube videos.

        Returns:
            YoutubeVideoSearchTool: An instance of YoutubeVideoSearchTool for YouTube video search.
        """
        return YoutubeVideoSearchTool()


    def create_market_data_extraction_search_tool(self):
        """
        Create a tool to search and extract market data.

        Returns:
            MDXSearchTool: An instance of MDXSearchTool for market data extraction.
        """
        return MDXSearchTool()
