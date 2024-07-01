from llama_index.core import (
    SimpleDirectoryReader,
    DocumentSummaryIndex,
    VectorStoreIndex,
    StorageContext,
    Settings,
    get_response_synthesizer,
    load_indices_from_storage
)
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from crewai_tools import LlamaIndexTool

import os
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
    def __init__(self, input_dir, llm_type='openai', model_name="gpt-3.5-turbo"):
        super().__init__(input_dir, llm_type, model_name)
        self.documents = self.load_documents()
        self.initialize_models()
        self.chroma_client = self.initialize_vector_store_client()
        self.gdpr_summary_index = self.create_summary_index('gdpr-summary')
        self.gdpr_semantic_search_index = self.create_vector_store_index('gdpr-semantic-search')
        self.gdpr_summary_tool, self.gdpr_semantic_search_tool = self.create_query_engine_tools()