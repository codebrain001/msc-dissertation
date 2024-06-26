# Create customer support agents automation
# Warning control
import warnings
import os
warnings.filterwarnings('ignore')
from crewai import Agent, Task, Crew
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = openai_api_key
openai_model = 'gpt-3.5-turbo'
os.environ["OPENAI_MODEL_NAME"] = openai_model

# Role playing, focus and cooperation
support_agent = Agent(
    role="Senior Support Representative",
    goal="Be the most friendly and helpful "
        "support representative in your team",
    backstory=(
		"You work at crewAI (https://crewai.com) and "
        " are now working on providing "
		"support to {customer}, a super important customer "
        " for your company."
		"You need to make sure that you provide the best support!"
		"Make sure to provide full complete answers, "
        " and make no assumptions."
	),
    allow_delegation=False,
    verbose=True,
)

support_quality_assurance_agent = Agent(
	role="Support Quality Assurance Specialist",
	goal="Get recognition for providing the "
    "best support quality assurance in your team",
	backstory=(
		"You work at crewAI (https://crewai.com) and "
        "are now working with your team "
		"on a request from {customer} ensuring that "
        "the support representative is "
		"providing the best support possible.\n"
		"You need to make sure that the support representative "
        "is providing full"
		"complete answers, and make no assumptions."
	),
	verbose=True
)
# Role Playing: Both agents have been given a role, goal and backstory.
# Focus: Both agents have been prompted to get into the character of the roles they are playing.
# Cooperation: Support Quality Assurance Agent can delegate work back to the Support Agent, allowing for these agents to work together.

# Tools, guardrails and memory
from crewai_tools import SerperDevTool, ScrapeWebsiteTool, WebsiteSearchTool
search_tool = SerperDevTool()
# specific scraping tool
docs_scrape_tool = ScrapeWebsiteTool(
    website_url="https://docs.crewai.com/how-to/Creating-a-Crew-and-kick-it-off/"
)
# Different Ways to Give Agents Tools
# Agent Level: The Agent can use the Tool(s) on any Task it performs.
# Task Level: The Agent will only use the Tool(s) when performing that specific Task.
# Note: Task Tools override the Agent Tools.
inquiry_resolution = Task(
    description=(
        "{customer} just reached out with a super important ask:\n"
	    "{inquiry}\n\n"
        "{person} from {customer} is the one that reached out. "
		"Make sure to use everything you know "
        "to provide the best support possible."
		"You must strive to provide a complete "
        "and accurate response to the customer's inquiry."),
    expected_output=(
	    "A detailed, informative response to the "
        "customer's inquiry that addresses "
        "all aspects of their question.\n"
        "The response should include references "
        "to everything you used to find the answer, "
        "including external data or solutions. "
        "Ensure the answer is complete, "
		"leaving no questions unanswered, and maintain a helpful and friendly "
		"tone throughout."
    ),
    tools=[search_tool, docs_scrape_tool],
    agent=support_agent,
)


quality_assurance_review = Task(
    description=(
        "Review the response drafted by the Senior Support Representative for {customer}'s inquiry. "
        "Ensure that the answer is comprehensive, accurate, and adheres to the "
		"high-quality standards expected for customer support.\n"
        "Verify that all parts of the customer's inquiry "
        "have been addressed "
		"thoroughly, with a helpful and friendly tone.\n"
        "Check for references and sources used to "
        " find the information, "
		"ensuring the response is well-supported and "
        "leaves no questions unanswered."
    ),
    expected_output=(
        "A final, detailed, and informative response "
        "ready to be sent to the customer.\n"
        "This response should fully address the "
        "customer's inquiry, incorporating all "
		"relevant feedback and improvements.\n"
		"Don't be too formal, we are a chill and cool company "
	    "but maintain a professional and friendly tone throughout."
    ),
    agent=support_quality_assurance_agent,
)

# Create Crew
crew = Crew(
    agents=[support_agent, support_quality_assurance_agent],
    tasks=[inquiry_resolution, quality_assurance_review],
    verbose=2,
    memory=True, # This sets all three types of memory easily - short, long and entity memory.
)

inputs = {
    "customer": "University of Sunderland",
    "person": "Ashley W.",
    "inquiry": "I need help with setting up a Crew "
               "and kicking it off, specifically "
               "how can I add memory to my crew? "
               "Can you provide guidance?"
}
result = crew.kickoff(inputs=inputs)
from IPython.display import Markdown
Markdown(result)