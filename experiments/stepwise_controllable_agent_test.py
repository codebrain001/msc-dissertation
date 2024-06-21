from llama_index.llms.openai import OpenAI
from llama_index.core.llms import ChatMessage
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.core.agent import AgentRunner, ReActAgent
from llama_index.core import Settings
import os

# Set up openai key
open_api_key = os.getenv("OPENAI_API_KEY")
Settings.llm = OpenAI(model="gpt-3.5-turbo", api_key=open_api_key)

# Define tools
def multiply(a: int, b: int) -> int:
    return a * b

def add(a: int, b: int) -> int:
    return a + b

def subtract(a: int, b: int) -> int:
    return a - b

def divide(a: int, b: int) -> int:
    return a / b

# Creating tools out of these functions as follows:
multiply_tool = FunctionTool.from_defaults(fn=multiply, name="multiply")
add_tool = FunctionTool.from_defaults(fn=add, name="add")
subtract_tool = FunctionTool.from_defaults(fn=subtract, name="subtract")
divide_tool = FunctionTool.from_defaults(fn=divide, name="divide")

# Setup agent
agent_worker = FunctionCallingAgentWorker.from_tools([multiply_tool, add_tool, subtract_tool, divide_tool],
                                                     llm=Settings.llm,
                                                     verbose=True,
                                                     allow_parallel_tool_calls=False)
agent = AgentRunner(agent_worker)

# response = agent.chat('what is 12 + (20 * 6) - 10 / 2?')

# Step-wise execution
# Note: AgentWorkers control the step-wise execution of a Task.
task = agent.create_task('what is 12 + (20 * 6) - 10 / 2?')

step_output = agent.run_step(task.task_id)
print(step_output.is_last)
# step_output has the following properties in a dictionary.
print(step_output.dict())
step_output = agent.run_step(task.task_id)
step_output = agent.run_step(task.task_id)
step_output = agent.run_step(task.task_id)
print(step_output.is_last)
# Stepwise execution with human feedback
step_output = agent.run_step(task.task_id, input='Multiple by 0')
print(step_output.is_last)



