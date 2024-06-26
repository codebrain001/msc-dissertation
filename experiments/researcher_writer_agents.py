# Create Agents to Research and write an article
# Warning control
import warnings
import os
warnings.filterwarnings('ignore')
from crewai import Agent, Task, Crew
openai_api_key = os.getenv("OPENAI_API_KEY")
os.environ['OPENAI_API_KEY'] = openai_api_key
openai_model = 'gpt-3.5-turbo'
os.environ["OPENAI_MODEL_NAME"] = openai_model

# Creating the agents, to create agents with crewai, you define the agent role, goal and backstrory
# I has been seen that LLMs performs better when they are role playing
planner  = Agent(
    role="Content Planner",
    goal="Plan engaging and factually accurate content for a given {topic}",
    backstory="You're working on planning a blog article "
                "about the topic: {topic}."
                "You collect information that helps the audience learn something "
                "and make informed decisions. "
                "Your work is the basis for "
                "the content writer to write an article on this topic.",
            allow_delegation=False,
            verbose=True,
)

writer = Agent(
    role="Content Writer",
    goal="Write insightful and factually accurate "
         "opinion piece about the topic: {topic}",
    backstory="You're working on a writing "
              "a new opinion piece about the topic: {topic}. "
              "You base your writing on the work of the content planner,"
              "who provides an outline and relevant context about the topic. "
              "You follow the main objectives and directions of the outline, "
              "as provide by the content planner. "
              "You also provide objective and impartial insights "
              "and back them up with information "
              "provide by the Content Planner. "
              "You acknowledge in your opinion piece "
              "when your statements are opinions "
              "as opposed to objective statements.",
    allow_delegation=False,
    verbose=True
)

editor = Agent(
    role="Editor",
    goal="Edit a given blog post to align with "
         "the writing style of the organization. ",
    backstory="You are an editor who receives a blog post "
              "from the Content Writer. "
              "Your goal is to review the blog post "
              "to ensure that it follows journalistic best practices,"
              "provides balanced viewpoints "
              "when providing opinions or assertions, "
              "and also avoids major controversial topics "
              "or opinions when possible.",
    allow_delegation=False,
    verbose=True
)

# Define the tasks
plan = Task(
    description=(
        "1. Prioritize the latest trends, key players, "
            "and noteworthy news on {topic}.\n"
        "2. Identify the target audience, considering "
            "their interests and pain points.\n"
        "3. Develop a detailed content outline including "
            "an introduction, key points, and a call to action.\n"
        "4. Include SEO keywords and relevant data or sources."
    ),
    expected_output="A comprehensive content plan document "
        "with an outline, audience analysis, "
        "SEO keywords, and resources.",
    agent=planner,
)

write = Task(
    description=(
        "1. Use the content plan to craft a compelling "
            "blog post on {topic}.\n"
        "2. Incorporate SEO keywords naturally.\n"
		"3. Sections/Subtitles are properly named "
            "in an engaging manner.\n"
        "4. Ensure the post is structured with an "
            "engaging introduction, insightful body, "
            "and a summarizing conclusion.\n"
        "5. Proofread for grammatical errors and "
            "alignment with the brand's voice.\n"
    ),
    expected_output="A well-written blog post "
        "in markdown format, ready for publication, "
        "each section should have 2 or 3 paragraphs.",
    agent=writer,
)

edit = Task(
    description=("Proofread the given blog post for "
                 "grammatical errors and "
                 "alignment with the brand's voice."),
    expected_output="A well-written blog post in markdown format, "
                    "ready for publication, "
                    "each section should have 2 or 3 paragraphs.",
    agent=editor
)

# The crew merges the agents and tasks together
# Note for this  projects, the tasks are performed sequentially by default
crew = Crew(
    agents=[planner, writer, editor],
    tasks=[plan, write, edit],
    verbose=2 # It can be set to 1 and 2, defining the level of granuality you want to see in the logs, the higher the number the more granuality
)

result = crew.kickoff(inputs={'topic': 'Requirement engineering'})