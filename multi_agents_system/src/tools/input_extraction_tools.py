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

class InputExtractionTools:
    """
    Class for extracting input documents and creating a summarization and semantic search indices.
    """
    def __init__(self, input_dir, llm_type='openai', model_name="gpt-3.5-turbo"):
        self.input_dir = input_dir
        self.llm_type = llm_type
        self.model_name = model_name
        self.documents = self.load_documents()
        self.initialize_models()
        self.chroma_client = self.initialize_vector_store_client()
        self.input_summary_index = self.create_summary_index()
        self.input_semantic_search_index = self.create_vector_store_index()

    def load_documents(self):
        """
        Load documents from the specified directory.
        """
        try:
            reader = SimpleDirectoryReader(input_dir=self.input_dir, required_exts=['.pdf', '.docx', '.txt', '.md', 'mp3', '.mp4'])
            documents = reader.load_data()
            return documents
        except Exception as e:
            logging.error(f"Error loading documents: {e}")
            return []

    def initialize_models(self):
        """
        Initialize LLM and embedding models based on the specified type.
        """
        try:
            if self.llm_type == 'openai':
                Settings.llm = OpenAI(model=self.model_name)
                Settings.embed_model = OpenAIEmbedding()
            elif self.llm_type == 'mistralai':
                pass
            else:
                raise ValueError(f"Unsupported LLM type: {self.llm_type}")
            self.splitter_strategy = SentenceSplitter()
        except Exception as e:
            logging.error(f"Error initializing models: {e}")

    def initialize_vector_store_client(self):
            """
            Initialize the Chroma vector store client with Persistent client that store data locally in a specified directory
            """
            try:
                persist_vector_store_path = 'multi_agents_system/src/tools/chromadb/'
                chroma_client = chromadb.PersistentClient(path=persist_vector_store_path)
                return chroma_client
            except Exception as e:
                logging.error(f"Error initializing Chroma vector store client: {e}")
                return None

    def create_chroma_db_collection(self, chroma_client, collection_name, load_collection_status=False):
        """
        Create or load a Chroma DB collection for storing vectors.
        """
        try:
            if load_collection_status:
                chroma_collection = chroma_client.get_collection(name=collection_name)
                logging.info(f"Loaded existing Chroma DB collection: {collection_name}")
            else:
                chroma_collection = chroma_client.create_collection(name=collection_name)
                logging.info(f"Created new Chroma DB collection: {collection_name}")
            vector_store_instance = ChromaVectorStore(chroma_collection=chroma_collection)
            return vector_store_instance
        except Exception as e:
            logging.error(f"Error creating or loading Chroma DB collection: {e}")
            return None

    def create_summary_index(self, collection_name, load_collection_status):
        """
        Create or load a summary index for the loaded documents.
        """
        try:
            summary_vector_store_instance = self.create_chroma_db_collection(
            self.chroma_client,
            collection_name,
            load_collection_status
            )
            summary_storage_context = StorageContext.from_defaults(vector_store=summary_vector_store_instance)
            if load_collection_status:
                summary_index = load_indices_from_storage(storage_context=summary_storage_context)
                return summary_index
            else:
                response_synthesizer = get_response_synthesizer(
                llm=Settings.llm, response_mode="tree_summarize", use_async=True
                )
                summary_index = DocumentSummaryIndex.from_documents(
                    documents=self.documents,
                    llm=Settings.llm,
                    transformations=[self.splitter_strategy],
                    response_synthesizer=response_synthesizer,
                    storage_context=summary_storage_context,
                    embed_model=Settings.embed_model,
                    show_progress=True,
                    use_async=True
                )
                return summary_index
        except Exception as e:
            logging.error(f"Error creating or loading summary index: {e}")
            return None

    def create_vector_store_index(self, collection_name, load_collection_status):
        """
        Create a vector store index for semantic search.
        """
        try:
            semantic_search_vector_store_instance = self.create_chroma_db_collection(
            self.chroma_client,
            collection_name,
            load_collection_status
            )
            semantic_search_storage_context = StorageContext.from_defaults(vector_store=semantic_search_vector_store_instance)
            if load_collection_status:
                semantic_search_index = load_indices_from_storage(storage_context=semantic_search_storage_context)
                return semantic_search_index
            else:
                vector_store_index = VectorStoreIndex.from_documents(
                documents=self.documents,
                llm=Settings.llm,
                transformations=[self.splitter_strategy],
                embed_model=Settings.embed_model,
                storage_context=semantic_search_storage_context,
                show_progress=True,
                use_async=True
            )
            return vector_store_index
        except Exception as e:
            logging.error(f"Error creating or loading vector store index: {e}")
            return None

    def create_query_engine_tools(self):
        """
        Create query engine tools for interacting with the summary and vector store indices.
        """
        try:
            self.summary_query_engine = self.input_summary_index.as_query_engine(response_mode="tree_summarize", use_async=True)
            self.vector_store_query_engine = self.input_semantic_search_index.as_query_engine(similarity_top_k=5, llm=Settings.llm)
            self.summary_tool = LlamaIndexTool.from_query_engine(
                self.summary_query_engine,
                name="Summary Index Query Tool",
                description="Use this tool to query summaries over the given document(s)."
            )
            self.vector_store_tool = LlamaIndexTool.from_query_engine(
                self.vector_store_query_engine,
                name="Vector Store Index Query Tool",
                description="Use this tool to semantic search over the given document(s)."
            )
            return self.summary_tool, self.vector_store_tool
        except Exception as e:
            logging.error(f"Error creating or loading query engine tools: {e}")
            return None, None
