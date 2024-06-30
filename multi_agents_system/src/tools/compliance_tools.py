from crewai_tools import ScrapeWebsiteTool, PDFSearchTool

class ComplianceTools:
    """
    A class to initialize and manage compliance tools.
    """

    def __init__(self):
        """
        Initialize all the compliance tools.
        """
        self.scrape_tool = self.create_GDPR_summary_tool()

    def create_GDPR_summary_tool(self):
        """
        Create a scraper tool for scaping the GDPR summary page

        Returns:
            ScrapeWebsiteTool: An instance of ScrapeWebsiteTool for scraping the GDPR summary page.
        """
        return ScrapeWebsiteTool(website_url='https://www.gdprsummary.com/gdpr-summary/')

    def create_GDPR_quick_access_reference_tool(self):
        """
        Create a scraper tool for scaping the GDPR quick access page for referencing purposes for the various chapters and respective articles.

        Returns:
            ScrapeWebsiteTool: An instance of ScrapeWebsiteTool for scraping the GDPR quick access page.
        """
        return ScrapeWebsiteTool(website_url='https://gdpr-info.eu/')

    def create_GDPR_semantic_search_tool(self):
        """
        Create a RAG pipeline for semantic searches with the official GDPR PDF document.

        Returns:
            PDFSearchTool: An instance of PDFSearchTool for the GDPR RAG pipeline.
        """
        return PDFSearchTool(pdf='./multi_agents_system/src/tools/data/documents/Official_GDPR.pdf')