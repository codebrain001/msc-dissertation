from crewai_tools import (
    SerperDevTool,
    ScrapeWebsiteTool,
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