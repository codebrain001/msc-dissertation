from crewai_tools import LlamaIndexTool
from llama_index.core import Settings

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
    Class for compliance tools consisting of GDPR summary and semantic search index tools.
    """
    def __init__(self, input_dir, model_name, api_key, load_collection_status):
        super().__init__(input_dir, model_name, api_key, load_collection_status)
        self.gdpr_summary_index = self.create_summary_index('gdpr-summary', load_collection_status)
        self.gdpr_semantic_search_index = self.create_vector_store_index('gdpr-semantic-search', load_collection_status)
        self.gdpr_summary_tool, self.gdpr_semantic_search_tool = self.create_compliance_query_engine_tools()

    def create_compliance_query_engine_tools(self):
        """
        Create query engine tools specifically for GDPR compliance.
        """
        try:
            self.gdpr_summary_query_engine = self.gdpr_summary_index.as_query_engine(response_mode="tree_summarize", use_async=True)
            self.gdpr_vector_store_query_engine = self.gdpr_semantic_search_index.as_query_engine(similarity_top_k=5, llm=Settings.llm)
            self.gdpr_summary_tool = LlamaIndexTool.from_query_engine(
                self.gdpr_summary_query_engine,
                name="GDPR Summary Index Query Tool",
                description="Use this tool to query summaries over the given document(s) for GDPR compliance."
            )
            self.gdpr_vector_store_tool = LlamaIndexTool.from_query_engine(
                self.gdpr_vector_store_query_engine,
                name="GDPR Vector Store Index Query Tool",
                description="Use this tool to semantic search over the given document(s) for GDPR compliance."
            )
            return self.gdpr_summary_tool, self.gdpr_vector_store_tool
        except Exception as e:
            logging.error(f"Error creating query engine tools: {e}")
            return None, None
