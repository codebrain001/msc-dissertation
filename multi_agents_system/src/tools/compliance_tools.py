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
    def __init__(self, input_dir, model_name="gpt-3.5-turbo"):
        super().__init__(input_dir, model_name)
        self.documents = self.load_documents()
        self.initialize_models()
        self.chroma_client = self.initialize_vector_store_client()
        self.gdpr_summary_index = self.create_summary_index(collection_name='gdpr-summary', load_collection_status=True)
        self.gdpr_semantic_search_index = self.create_vector_store_index(collection_name='gdpr-semantic-search', load_collection_status=True)
        self.gdpr_summary_tool, self.gdpr_semantic_search_tool = self.create_query_engine_tools()