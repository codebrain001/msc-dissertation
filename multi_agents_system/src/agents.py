from crewai import Agent
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI

import sys
import logging
import nest_asyncio
# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

class Agents:
    def __init__(self, model_name, api_key,  input_extraction_tools, search_and_scrape_tools, compliance_tools):
        self.model_name = model_name
        self.api_key = api_key
        self.input_extraction_tools = input_extraction_tools
        self.search_and_scrape_tools = search_and_scrape_tools
        self.compliance_tools = compliance_tools
        # Instatiate individual tools
        self.input_summary_tool, self.input_semantic_search_tool = self.input_extraction_tools.create_query_engine_tools()
        self.search_tool = self.search_and_scrape_tools.create_search_tool()
        self.scrape_tool = self.search_and_scrape_tools.create_scrape_tool()
        self.gdpr_summary_tool, self.gdpr_semantic_search_tool = compliance_tools.create_compliance_query_engine_tools()

      # Define the llm model to run agent with
        if self.model_name in ["gpt-4o"]:
            self.llm = ChatOpenAI(model=self.model_name, api_key=self.api_key, temperature=0)
        elif self.model_name in ['claude-3-5-sonnet-20240620']:
            self.llm = ChatAnthropic(model_name=self.model_name, api_key=self.api_key, temperature=0)
        elif self.model_name in ['gemini-1.5-pro']:
            self.llm = ChatGoogleGenerativeAI(model=f'models/{self.model_name}', api_key=self.api_key, temperature=0)
        else:
            logging.error(f'Unsupported model name: {self.model_name}')

    # Define the agents
    def preliminary_requirement_profiling_agent(self):
        return Agent(
            role='Senior Business Analyst',
            goal='Identify and outline initial project requirements.',
            backstory=(
                'You are a Senior Business Analyst with extensive experience in analyzing business needs and translating them into actionable project plans. '
                'You have worked in various industries, including finance, healthcare, and technology, providing you with a broad perspective on different business models. '
                'You are tasked with dissecting preliminary meeting notes to identify key project requirements and objectives, ensuring that all stakeholder needs are captured from the outset.'
            ),
            tools=[
                self.input_summary_tool,
                self.input_semantic_search_tool
            ],
            verbose=True,
            llm=self.llm,
            max_rpm=None,
        )

    def research_agent(self):
        return Agent(
            role='Senior Market Researcher',
            goal='Conduct comprehensive market and competitive research.',
            backstory=(
                'You are a Senior Market Researcher with a keen eye for detail and a passion for uncovering the latest market trends.'
                'Your prowness includes navigating and extracting critical information with background in technology, business, economics, finance and marketing.'
                'Your skills helps product owners understand thier competitive landscapes and feasibility study'
                'You are tasked with gathering detailed market data, analyzing competitors, and identifying technological trends and gaps that could influence the success of a new business initiative.'
            ),
            tools=[
                self.search_tool,
                self.scrape_tool,
                ],
            verbose=True,
            llm=self.llm,
            max_rpm=None,
        )

    def requirement_development_agent(self):
        return Agent(
            role='Senior Requirements Engineer',
            goal=(
            'Develop comprehensive and detailed functional and non-functional requirements based on insights from initial profiling and market research tasks. '
            'Create well-defined user stories and acceptance criteria for each requirement, ensuring all requirements are clearly articulated, actionable, and aligned with stakeholder needs and project objectives.'
            ),
            backstory=(
                'You have extensive experience in requirements analysis, and specification as well as software engineering. '
                'You have strong technical knowledge, excellent communication skills, and the ability to translate business needs into technical specifications.'
                'With prowness of bridging the gap between business and technology'
            ),
            verbose=True,
            llm=self.llm,
            max_rpm=None,
        )

    def compliance_agent(self):
        return Agent(
            role='GDPR Compliance Specialist',
            goal='Ensure project compliance with GDPR.',
            backstory=(
                'You are a GDPR Compliance Specialist with extensive experience in data protection and privacy laws. '
                'You have a deep understanding of the legal requirements and best practices. '
                'You are responsible for conducting Data Protection Impact Assessments (DPIA), developing compliance strategies, and ensuring that all aspects of the project adhere to GDPR regulations.'
            ),
            tools=[
                self.gdpr_summary_tool,
                self.gdpr_semantic_search_tool
            ],
            verbose=True,
            llm=self.llm,
            max_rpm=None,
        )

    def data_dictionary_agent(self):
        return Agent(
            role='Senior Data Architect',
            goal='Develop and maintain a comprehensive data dictionary. ',
            backstory=(
                'You are a Senior Data Architect with a deep understanding of data management and database design. '
                'With over a decade of experience, you have worked on numerous projects to design and implement robust data architectures. '
                'Your role involves identifying key data elements, defining data types and formats, establishing relationships between data elements, and documenting metadata. '
                'Your current project focuses on creating a comprehensive data dictionary for a new application, ensuring data integrity and consistency.'
            ),
            verbose=True,
            llm=self.llm,
            max_rpm=None,
        )

    def quality_assurance_agent(self):
        return Agent(
            role='Senior Quality Assurance Analyst',
            goal="Ensure the BRD's completeness, correctness, and adherence to best practices.",
            backstory=(
                'With extensive experience in software testing and quality assurance. '
                'You have worked on ensuring the quality and reliability of software projects by implementing rigorous testing processes and quality control measures. '
                'Your role involves reviewing the Business Requirement Document (BRD) for completeness and correctness, ensuring adherence to best practices in business analysis and software engineering, and generating a comprehensive project summary. '
                'Your current project requires you to oversee the final production of the BRD, guaranteeing that it meets the highest standards of quality and accuracy.'
            ),
            tools=[
                self.search_tool,
                self.scrape_tool,
            ],
            verbose=True,
            llm=self.llm,
            max_rpm=None,
        )

    def project_management_agent(self):
        return Agent(
            role='Senior Project Manager',
            goal='Develop a detailed project plan and timeline. ',
            backstory=(
                'You are a Senior Project Manager with a proven track record of successfully leading projects from inception to completion. '
                'With a background in project management and a certification in PMP, you have managed projects across various domains, including IT, construction, and healthcare. '
                'Your role involves developing detailed project plans, estimating timelines, allocating resources, and managing risks. '
                'Your current assignment is to ensure that a new project is planned and executed efficiently, meeting all deadlines and objectives'
            ),
            verbose=True,
            llm=self.llm,
            max_rpm=None,
        )