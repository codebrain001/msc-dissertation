# Controlling agent reasoning loop with return direct tools
# This can be useful for speeding up the agent's response time, when you know the tool output is good enough,
# to avoid the agent rewriting the response and for ending the reasoning loop.
#This feature plays a crucial role in streamlining the agent's decision-making process,
#particularly when immediate output from a single tool is sufficient for the task at hand rather than sending the output of tool to LLM for final response.
# Setting return_direct to True impacts the agent's reasoning loop. When activated and the corresponding tool is called independently, the loop concludes, 
# and the output from the tool is directly returned.

from llama_index.core.bridge.pydantic import BaseModel # Using Pydantic class for data validation, type enforcement, data parsing, proper error handling as it will definitely be used to store data
from llama_index.core.agent import AgentRunner
from llama_index.core.agent import FunctionCallingAgentWorker
from llama_index.llms.openai import OpenAI
from llama_index.embeddings.mistralai import MistralAIEmbedding
from llama_index.core.tools import BaseTool, FunctionTool
from llama_index.core.llms import ChatMessage
from llama_index.core import Settings
from typing import Optional
import os

mistral_api_key = os.getenv("MISTRAL_API_KEY")
# Settings.llm = MistralAI(model="mistral-small", api_key=mistral_api_key)
# e mistral-small does not support function calling API. hence I will utilize OpenAI
open_api_key = os.getenv("OPENAI_API_KEY")
Settings.llm = OpenAI(model="gpt-4", api_key=open_api_key)
Settings.embed_model = MistralAIEmbedding(model_name='mistral-embed', api_key=mistral_api_key)


# Defining a system to manage restaurant bookings using various functions and integrating them into a tool-based architecture
bookings = {} # A dictionary to store bookings using unique user IDs as keys.

# The RestaurantBooking class is a Pydantic model used to track and represent the state of a booking. It includes optional fields like name, email, phone, date, and time, allowing for flexible data entry.
class RestaurantBooking(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    date: Optional[str] = None
    time: Optional[str] = None

def get_booking_state(user_id: str) -> str:
    """Get the current state of a booking for a given booking ID."""
    try:
        return str(bookings[user_id].dict())
    except:
        return f"Booking ID {user_id} not found"

def update_booking(user_id: str, property: str, value: str) -> str:
    """Update a property of a booking for a given booking ID. Only enter details that are explicitly provided."""
    booking = bookings[user_id]
    setattr(booking, property, value)
    return f"Booking ID {user_id} updated with {property}={value}"

def create_booking(user_id: str) -> str:
    """Create a new booking for a given booking ID."""
    bookings[user_id] = RestaurantBooking()
    return "Booking created, but not yet confirmed. Please provide your name, email, phone, date, and time."


def confirm_booking(user_id: str) -> str:
    """Confirm a booking for a given booking ID."""
    booking = bookings[user_id]

    if booking.name is None:
        raise ValueError("Please provide your name.")

    if booking.email is None:
        raise ValueError("Please provide your email.")

    if booking.phone is None:
        raise ValueError("Please provide your phone number.")

    if booking.date is None:
        raise ValueError("Please provide a date of your booking.")

    if booking.time is None:
        raise ValueError("Please provide a time of your booking.")

    return f"Booking ID {user_id} confirmed."

# Experimnent 1: return_direct is not enabled in get_booking_state_tool
# Create tools
get_booking_state_tool = FunctionTool.from_defaults(fn=get_booking_state, name="get_booking_state")
update_booking_tool = FunctionTool.from_defaults(fn=update_booking, name="update_booking")
create_booking_tool = FunctionTool.from_defaults(fn=create_booking, name="create_booking", return_direct=True)
confirm_booking_tool = FunctionTool.from_defaults(fn=confirm_booking, name="confirm_booking", return_direct=True)

user_id = "user123"
prefix_messages = [
    ChatMessage(
        role="system",
        content=(
            f"You are now connected to the booking system and helping {user_id} with making a booking. "
            "Only enter details that the user has explicitly provided. "
            "Do not make up any details."
        ),
    )
]

# Create agent
agent_worker = FunctionCallingAgentWorker(
    tools=[get_booking_state_tool, update_booking_tool, create_booking_tool, confirm_booking_tool],
    llm=Settings.llm,
    prefix_messages=prefix_messages,
    allow_parallel_tool_calls=False,
    verbose=True
)

agent = AgentRunner(agent_worker, verbose=True)

# Creating booking
response = agent.chat('Hi, I would love to make a restaurant booking.')
response = agent.chat('My name is Brain and my email is brain@gmail.com and phone number 1234567890.')
response = agent.chat('I would love to book June 17th 2024 by 11:00 AM')
response = agent.chat("provide booking details of user user123")

# Experiment 2 return_direct is enabled in `get_booking_state_tool`
print('Experiment 2', '#'*10)
# Create tools
get_booking_state_tool = FunctionTool.from_defaults(fn=get_booking_state, name="get_booking_state", return_direct=True)
update_booking_tool = FunctionTool.from_defaults(fn=update_booking, name="update_booking")
create_booking_tool = FunctionTool.from_defaults(fn=create_booking, name="create_booking", return_direct=True)
confirm_booking_tool = FunctionTool.from_defaults(fn=confirm_booking, name="confirm_booking", return_direct=True)

user_id = "user124"
prefix_messages = [
    ChatMessage(
        role="system",
        content=(
            f"You are now connected to the booking system and helping {user_id} with making a booking. "
            "Only enter details that the user has explicitly provided. "
            "Do not make up any details."
        ),
    )
]

# Create agent
agent_worker = FunctionCallingAgentWorker(
    tools=[get_booking_state_tool, update_booking_tool, create_booking_tool, confirm_booking_tool],
    llm=Settings.llm,
    prefix_messages=prefix_messages,
    allow_parallel_tool_calls=False,
    verbose=True
)

agent = AgentRunner(agent_worker, verbose=True)

# Creating booking
response = agent.chat('Hi, I would love to make a restaurant booking.')
response = agent.chat('My name is John and my email is john@gmail.com and phone number 1234567890.')
response = agent.chat('I would love to book June 19th 2024 by 12:00 AM')
response = agent.chat("provide booking details of user user124")

