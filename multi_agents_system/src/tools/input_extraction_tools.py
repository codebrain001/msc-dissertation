from llama_index.core import (
    SimpleDirectoryReader,
    DocumentSummaryIndex,
    VectorStoreIndex,
    StorageContext,
    Settings,
    get_response_synthesizer,
)
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb
from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
from crewai_tools import LlamaIndexTool

import os
import logging
import sys
import nest_asyncio
from dotenv import load_dotenv

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Load environment variables
dotenv_path = 'multi_agents_system/src/.env'
load_dotenv(dotenv_path=dotenv_path)
openai_api_key = os.getenv("OPENAI_API_KEY")
mistral_api_key = os.getenv("MISTRAL_API_KEY")

# Vector store persistent directory
persist_vector_store_path = 'multi_agents_system/src/tools/chromadb/'

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

class InputExtractionTools:
    """
    Class for extracting input documents and creating a summarization and semantic search indices.
    """
    def __init__(self, input_dir, model_name, load_collection_status):
        self.input_dir = input_dir
        self.model_name = model_name
        self.load_collection_status = load_collection_status
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
            if self.model_name in ["gpt-3.5-turbo", "gpt-4o"]:
                Settings.llm = OpenAI(model_name=self.model_name, api_key=openai_api_key)
                Settings.embed_model = OpenAIEmbedding(model_name='text-embedding-3-small', api_key=openai_api_key)
            elif self.model_name in ["open-mixtral-8x22b", "mistral-medium"]:
                Settings.llm = MistralAI(model_name=self.model_name, api_key=mistral_api_key)
                Settings.embed_model = MistralAIEmbedding(model_name="mistral-embed", api_key=mistral_api_key)
            else:
                logging.error(f"Invalid LLM: {self.model_name}")
            self.splitter_strategy = SentenceSplitter()
        except Exception as e:
            logging.error(f"Error initializing models: {e}")

    def initialize_vector_store_client(self):
        """
        Initialize the Chroma vector store client
        """
        try:
            chroma_client = chromadb.PersistentClient(path=persist_vector_store_path)
            return chroma_client
        except Exception as e:
            logging.error(f"Error iinitializing vector store client: {e}")
            return None


    def create_chroma_db_collection(self, chroma_client, collection_name, load_collection_status):
        """
        Create or load a Chroma DB collection for storing vectors.
        """
        # Check the model name and add the appropriate suffix
        if self.model_name in ["gpt-3.5-turbo", "gpt-4o"]:
            collection_name_suffix = "openai"
        elif self.model_name in ["open-mixtral-8x22b", "mistral-medium"]:
            collection_name_suffix = "mistral"
        else:
            logging.error(f"Invalid LLM, cannot create collection name suffix for model: {self.model_name}")
            return None  # Return if model name is invalid

        # Add the suffix to the collection name
        collection_name = f"{collection_name}-{collection_name_suffix}"

        try:
            collections_list = [col.name for col in chroma_client.list_collections()]
            logging.info(f'Collections list: {collections_list}')

            if load_collection_status:
                # Load the collection
                if collection_name in collections_list:
                    chroma_collection = chroma_client.get_collection(name=collection_name)
                    logging.info(f"Loaded existing Chroma DB collection: {collection_name}")
                else:
                    logging.error(f"Collection {collection_name} does not exist.")
                    return None
            else:
                # Delete existing collection if it exists
                if collection_name in collections_list:
                    try:
                        chroma_client.delete_collection(name=collection_name)
                        logging.info(f"Deleted existing Chroma DB collection: {collection_name}")
                    except Exception as e:
                        logging.error(f"Error deleting existing Chroma DB collection: {e}")
                        return None

                # Create new collection
                try:
                    chroma_collection = chroma_client.create_collection(name=collection_name)
                    logging.info(f"Created new Chroma DB collection: {collection_name}")
                except Exception as e:
                    logging.error(f"Error creating Chroma DB collection: {e}")
                    return None  # Return if creation failed

            vector_store_instance = ChromaVectorStore(chroma_collection=chroma_collection)
            logging.info(f"Chroma DB collection created or loaded successfully: {collection_name}")
            return vector_store_instance

        except Exception as e:
            logging.error(f"Error creating Chroma DB collection: {e}")
            return None


    def create_summary_index(self, collection_name='msc-dissertation-001-input-summary', load_collection_status=None):
        """
        Create a summary index for the loaded documents.
        """
        if load_collection_status is None:
            load_collection_status = self.load_collection_status

        try:
            logging.info(f"Creating or loading summary vector store with collection name: {collection_name}")
            summary_vector_store_instance = self.create_chroma_db_collection(
                self.chroma_client,
                collection_name,
                load_collection_status
            )
            if not summary_vector_store_instance:
                logging.error("Failed to create or load summary vector store instance.")
                return None

            summary_storage_context = StorageContext.from_defaults(vector_store=summary_vector_store_instance)
            response_synthesizer = get_response_synthesizer(
                llm=Settings.llm, response_mode="tree_summarize", use_async=True
            )
            if load_collection_status:
                logging.info("Loading Document summary index from existing vector store")
                summary_index =  VectorStoreIndex.from_vector_store(
                    vector_store=summary_vector_store_instance,
                    storage_context=summary_storage_context
                )
            else:
                logging.info("Creating DocumentSummaryIndex from documents")
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
            logging.info("DocumentSummaryIndex created successfully")
            return summary_index
        except Exception as e:
            logging.error(f"Error creating summary index: {e}")
            return None


    def create_vector_store_index(self, collection_name='msc-dissertation-001-input-semantic-search', load_collection_status=None):
        """
        Create a vector store index for semantic search.
        """
        if load_collection_status is None:
            load_collection_status = self.load_collection_status

        try:
            logging.info(f"Creating or loading semantic search vector store with collection name: {collection_name}")
            semantic_search_vector_store_instance = self.create_chroma_db_collection(
                self.chroma_client,
                collection_name,
                load_collection_status,
            )
            if not semantic_search_vector_store_instance:
                logging.error("Failed to create or load semantic search vector store instance.")
                return None

            semantic_search_storage_context = StorageContext.from_defaults(vector_store=semantic_search_vector_store_instance)

            if load_collection_status:
                logging.info("Loading vector store index from existing vector store")
                vector_store_index = VectorStoreIndex.from_vector_store(
                    vector_store=semantic_search_vector_store_instance,
                    storage_context=semantic_search_storage_context
                )
            else:
                logging.info("Creating vector store index from documents")
                vector_store_index = VectorStoreIndex.from_documents(
                    documents=self.documents,
                    llm=Settings.llm,
                    transformations=[self.splitter_strategy],
                    embed_model=Settings.embed_model,
                    storage_context=semantic_search_storage_context,
                    show_progress=True,
                    use_async=True
                )
            logging.info("Vector store index created successfully")
            return vector_store_index
        except Exception as e:
            logging.error(f"Error creating vector store index: {e}")
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
            logging.error(f"Error creating query engine tools: {e}")
            return None, None