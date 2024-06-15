# Simple calculator tools
from llama_index.core.agent import ReActAgent
from llama_index.llms.openai import OpenAI
from llama_index.llms.mistralai import MistralAI
from llama_index.llms.anthropic import Anthropic
from llama_index.core.llms import ChatMessage
from  llama_index.core.tools import BaseTool, FunctionTool
import os

# # Define tools
# def multiply(a: int, b: int) -> int:
#     return a * b

# def add(a: int, b: int) -> int:
#     return a + b

# def subtract(a: int, b: int) -> int:
#     return a - b

# def divide(a: int, b: int) -> int:
#     return a / b

# # Creating tools out of these functions as follows:
# multiply_tool = FunctionTool.from_defaults(fn=multiply, name="multiply")
# add_tool = FunctionTool.from_defaults(fn=add, name="add")
# subtract_tool = FunctionTool.from_defaults(fn=subtract, name="subtract")
# divide_tool = FunctionTool.from_defaults(fn=divide, name="divide")

# # Instatiate openai GPT4
# open_api_key = os.getenv("OPENAI_API_KEY")
# mistral_api_key = os.getenv("MISTRAL_API_KEY")
# llm = MistralAI(model="mistral-small", api_key=mistral_api_key)
# agent = ReActAgent.from_tools([multiply_tool, add_tool, subtract_tool, divide_tool], llm=llm, verbose=True)

# response = agent.chat('What is 20 + (2*4) / 6?')
# print(response)

# # Check the prompt
# prompt_dict = agent.get_prompts()
# for k,v in prompt_dict.items():
#     print(f"Prompt: {k}, \n\nValue: {v.template} v")

# RAG QueryEnginer Tools
from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    load_index_from_storage
)

from llama_index.core.tools import QueryEngineTool, ToolMetadata
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core import Settings

mistral_api_key = os.getenv("MISTRAL_API_KEY")

Settings.llm = MistralAI(model="mistral-small", api_key=mistral_api_key)
Settings.embed_model = MistralAIEmbedding(model_name='mistral-embed', api_key=mistral_api_key)

# PERSIST_DIR = './local_storage'
# try:
#     storage_context = StorageContext.from_defaults(persist_dir=PERSIST_DIR)
#     index = load_index_from_storage(storage_context)

try:
    storage_context = StorageContext.from_defaults(
        persist_dir="./storage/lyft"
    )
    lyft_index = load_index_from_storage(storage_context)

    storage_context = StorageContext.from_defaults(
        persist_dir="./storage/uber"
    )
    uber_index = load_index_from_storage(storage_context)

    index_loaded = True
except:
    index_loaded = False

if not index_loaded:
    # load data
    lyft_docs = SimpleDirectoryReader(
        input_files=["./data/10k/lyft_2021.pdf"]
    ).load_data()
    uber_docs = SimpleDirectoryReader(
        input_files=["./data/10k/uber_2021.pdf"]
    ).load_data()

    # build index
    lyft_index = VectorStoreIndex.from_documents(lyft_docs)
    uber_index = VectorStoreIndex.from_documents(uber_docs)

    # persist index
    lyft_index.storage_context.persist(persist_dir="./storage/lyft")
    uber_index.storage_context.persist(persist_dir="./storage/uber")

# Create the query engines
lyft_engine = lyft_index.as_query_engine(similarity_top_k=3)
uber_engine = uber_index.as_query_engine(similarity_top_k=3)

# Define tools on top of this query engines
query_engine_tools = [
    QueryEngineTool(
        query_engine=lyft_engine,
        metadata=ToolMetadata(
            name="lyft_10k",
            description=(
                "Provides information about Lyft financials for year 2021. "
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
    QueryEngineTool(
        query_engine=uber_engine,
        metadata=ToolMetadata(
            name="uber_10k",
            description=(
                "Provides information about Uber financials for year 2021. "
                "Use a detailed plain text question as input to the tool."
            ),
        ),
    ),
]

# Create the agent based on the two query engine tools
agent = ReActAgent.from_tools(query_engine_tools, llm=Settings.llm, verbose=True)

response = agent.chat('Compare the growth of Uber and Lyft')
print(response)
