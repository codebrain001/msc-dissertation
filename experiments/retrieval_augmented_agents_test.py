from llama_index.core.agent import AgentRunner
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.llms.openai import OpenAI
from llama_index.llms.mistralai import MistralAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core import Settings
import os

mistral_api_key = os.getenv("MISTRAL_API_KEY")
# Settings.llm = MistralAI(model="mistral-small", api_key=mistral_api_key)
# e mistral-small does not support function calling API. hence I will utilize OpenAI
open_api_key = os.getenv("OPENAI_API_KEY")
Settings.llm = OpenAI(model="gpt-3.5-turbo", api_key=open_api_key)
Settings.embed_model = MistralAIEmbedding(model_name='mistral-embed', api_key=mistral_api_key)


# Define tools
def multiply(a: int, b: int) -> int:
    return a * b

def add(a: int, b: int) -> int:
    return a + b

def subtract(a: int, b: int) -> int:
    return a - b

def divide(a: int, b: int) -> int:
    return a / b

def useless_function(a: int, b: int) -> int:
    pass

# Creating tools out of these functions as follows:
multiply_tool = FunctionTool.from_defaults(fn=multiply, name="multiply")
add_tool = FunctionTool.from_defaults(fn=add, name="add")
subtract_tool = FunctionTool.from_defaults(fn=subtract, name="subtract")
divide_tool = FunctionTool.from_defaults(fn=divide, name="divide")

useless_tools = [
    FunctionTool.from_defaults(fn=useless_function, name=f'useless_tool_{str(index)}') for index in range(5)
]
# Wrap all tools in a list
all_tools = [multiply_tool, add_tool, subtract_tool, divide_tool] + useless_tools

# Define an object index over these tools
from llama_index.core import VectorStoreIndex
from llama_index.core.objects import ObjectIndex

obj_index = ObjectIndex.from_objects(all_tools, index_cls=VectorStoreIndex)

agent_worker = FunctionCallingAgentWorker.from_tools(
    tool_retriever=obj_index.as_retriever(similarity_top_k=2),
    llm=Settings.llm,
    verbose=True,
    allow_parallel_tool_calls=False,
)

agent = AgentRunner(agent_worker, verbose=True)

response = agent.chat('What is 20 + (2*4) ?')
print(response)