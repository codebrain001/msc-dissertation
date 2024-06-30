from llama_index.core import (
    SimpleDirectoryReader,
    DocumentSummaryIndex,
    VectorStoreIndex,
    StorageContext,
    Settings,
    load_indices_from_storage,
    get_response_synthesizer
)

from llama_index.core.node_parser import SentenceSplitter
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.openai import OpenAIEmbedding
from crewai_tools import LlamaIndexTool
import os
import logging
import sys
import nest_asyncio

nest_asyncio.apply()
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

class InputExtractionTools:
    def __init__(self, input_dir, persist_dir, llm_type='openai', model_name="gpt-3.5-turbo"):
        self.input_dir = input_dir
        self.persist_dir = persist_dir
        self.llm_type = llm_type
        self.model_name = model_name
        os.makedirs(self.persist_dir, exist_ok=True)
        self.documents = self.load_documents()
        self.initialize_models()
        self.summary_indices = self.ensure_summary_indices()
        self.vector_store_indices = self.ensure_vector_store_indices()

    def load_documents(self):
        reader = SimpleDirectoryReader(input_dir=self.input_dir, required_exts=['.pdf', '.docx', '.txt', '.md', 'mp3', '.mp4'])
        documents = reader.load_data()
        return documents

    def initialize_models(self):
        if self.llm_type == 'openai':
            Settings.llm = OpenAI(model=self.model_name)
            Settings.embed_model = OpenAIEmbedding()
        elif self.llm_type == 'mistralai':
            pass
        else:
            raise ValueError(f"Unsupported LLM type: {self.llm_type}")
        self.splitter_strategy = SentenceSplitter()

    def ensure_summary_indices(self):
        summary_index_dir = os.path.join(self.persist_dir, 'summary_index')
        if os.path.exists(summary_index_dir):
            return self.load_index(DocumentSummaryIndex, 'summary_index')
        else:
            return self.create_summary_indices()

    def ensure_vector_store_indices(self):
        vector_store_index_dir = os.path.join(self.persist_dir, 'vector_store_index')
        if os.path.exists(vector_store_index_dir):
            return self.load_index(VectorStoreIndex, 'vector_store_index')
        else:
            return self.create_vector_store_indices()

    def create_summary_indices(self):
        response_synthesizer = get_response_synthesizer(
            llm=Settings.llm, response_mode="tree_summarize", use_async=True
        )
        summary_indices = DocumentSummaryIndex.from_documents(
            documents=self.documents,
            llm=Settings.llm,
            transformations=[self.splitter_strategy],
            response_synthesizer=response_synthesizer,
            embed_model=Settings.embed_model,
            show_progress=True,
            use_async=True
        )
        self.persist_index(summary_indices, 'summary_index')
        return summary_indices

    def create_vector_store_indices(self):
        vector_store_indices = VectorStoreIndex.from_documents(
            documents=self.documents,
            llm=Settings.llm,
            transformations=[self.splitter_strategy],
            embed_model=Settings.embed_model,
            show_progress=True,
            use_async=True
        )
        self.persist_index(vector_store_indices, 'vector_store_index')
        return vector_store_indices

    def persist_index(self, index, subdir):
        persist_dir = os.path.join(self.persist_dir, subdir)
        os.makedirs(persist_dir, exist_ok=True)
        index.storage_context.persist(persist_dir)

    def load_index(self, index_class, subdir):
        persist_dir = os.path.join(self.persist_dir, subdir)
        storage_context = StorageContext.from_defaults(persist_dir=persist_dir)
        indices = load_indices_from_storage(storage_context=storage_context)
        return indices

    def create_query_engine_tools(self):
        self.summary_query_engine = self.summary_indices[0].as_query_engine(response_mode="tree_summarize", use_async=True)
        self.vector_store_query_engine = self.vector_store_indices[0].as_query_engine(similarity_top_k=5, llm=Settings.llm)
        self.summary_tool = LlamaIndexTool.from_query_engine(
            self.summary_query_engine,
            name="Summary Index Query Tool",
            description="Use this tool to query over the uploaded preliminary documents using the summary index."
        )
        self.vector_store_tool = LlamaIndexTool.from_query_engine(
            self.vector_store_query_engine,
            name="Vector Store Index Query Tool",
            description="Use this tool to query over the uploaded preliminary documents using the vector store index."
        )
        return self.summary_tool, self.vector_store_tool

