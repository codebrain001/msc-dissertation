import logging
import sys
import nest_asyncio

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

from tools.input_extraction_tools import InputExtractionTools

class ComplianceTools(InputExtractionTools):
    """
    Class for compliance tools consisting of GDPR summary and semantic search index tools
    """
    def __init__(self, input_dir, model_name="gpt-3.5-turbo",  load_collection_status=True):
        super().__init__(input_dir, model_name, load_collection_status)
        self.gdpr_summary_index = self.create_summary_index('gdpr-summary', load_collection_status=True)
        self.gdpr_semantic_search_index = self.create_vector_store_index('gdpr-semantic-search', load_collection_status=self.load_collection_status)
        self.gdpr_summary_tool, self.gdpr_semantic_search_tool = self.create_query_engine_tools()