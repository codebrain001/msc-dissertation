from crewai import Agent
from tools.input_extraction_tools import InputExtractionTools
from tools.search_and_scrape_tools import SearchAndScrapeTools
import re
import streamlit as st


class Agents():
    def __init__(self, input_extraction_tools, search_and_scrape_tools, compliance_tools):
        self.input_extraction_tools = input_extraction_tools
        self.summary_tool, self.semantic_search_tool = self.input_extraction_tools.create_query_engine_tools()
        self.search_and_scrape_tools = search_and_scrape_tools
        self.search_tool = self.search_and_scrape_tools.create_search_tool()
        self.scrape_tool = self.search_and_scrape_tools.create_scrape_tool()
        self.youtube_video_search_tool = self.search_and_scrape_tools.create_youtube_video_search_tool()
        self.market_data_extraction_search_tool = self.search_and_scrape_tools.create_market_data_extraction_search_tool()
        self.compliance_tools = compliance_tools
        self.gdpr_summary_tool = self.compliance_tools.create_GDPR_summary_tool()
        self.gdpr_quick_access_reference_tool = self.compliance_tools.create_GDPR_quick_access_reference_tool()
        self.gdpr_semantic_search_tool = self.compliance_tools.create_GDPR_semantic_search_tool()




    def preliminary_requirement_profiling_agent(self):
        return Agent(
            role='Senior Business Analyst',
            goal='Identify and outline initial project requirements.',
            backstory=(
                'You are a Senior Business Analyst with extensive experience in analyzing business needs and translating them into actionable project plans. '
                'You have worked in various industries, including finance, healthcare, and technology, providing you with a broad perspective on different business models. '
                'You are tasked with dissecting preliminary meeting notes to identify key project requirements and objectives, ensuring that all stakeholder needs are captured from the outset.'
            ),
            tools=[self.summary_tool, self.semantic_search_tool],
            verbose=True,
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
            tools=[self.search_tool,
                   self.scrape_tool,
                   self.youtube_video_search_tool,
                   self.market_data_extraction_search_tool],
            verbose=True,
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
                self.gdpr_quick_access_reference_tool,
                self.gdpr_semantic_search_tool
            ],
            verbose=True,
        )

    def requirement_development_agent(self):
        return Agent(
            role='Senior Requirements Engineer',
            goal='Develop detailed functional and non-functional requirements as well as Develop detailed functional requirements based on initial profiling and research based on initial profiling and research. ',
            backstory=(
                'You have extensive experience in requirements analysis, and specification as well as software engineering. '
                'You have strong technical knowledge, excellent communication skills, and the ability to translate business needs into technical specifications.'
                'With prowness of bridging the gap between business and technology'
            ),
            tools=[self.search_tool,
                   self.scrape_tool,
            ],
            verbose=True,
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
            tools=[self.search_tool,
                   self.scrape_tool,
            ],
            verbose=True,
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
            tools=[self.search_tool,
                   self.scrape_tool,
            ],
            verbose=True,
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
            tools=[self.search_tool,
                   self.scrape_tool,
            ],
            verbose=True,
        )

# This portion of the code is adapted from @AbubakrChan; thank you!                       #
# https://github.com/AbubakrChan/crewai-UI-business-product-launch/blob/main/main.py
class StreamToExpander:
    def __init__(self, expander):
        self.expander = expander
        self.buffer = []
        self.colors = ['red', 'green', 'blue', 'orange']  # Define a list of colors
        self.color_index = 0  # Initialize color index

    def write(self, data):
        # Filter out ANSI escape codes using a regular expression
        cleaned_data = re.sub(r'\x1B\[[0-9;]*[mK]', '', data)

        # Check if the data contains 'task' information
        task_match_object = re.search(r'\"task\"\s*:\s*\"(.*?)\"', cleaned_data, re.IGNORECASE)
        task_match_input = re.search(r'task\s*:\s*([^\n]*)', cleaned_data, re.IGNORECASE)
        task_value = None
        if task_match_object:
            task_value = task_match_object.group(1)
        elif task_match_input:
            task_value = task_match_input.group(1).strip()

        if task_value:
            st.toast(":robot_face: " + task_value)

        # Check if the text contains the specified phrase and apply color
        if "Entering new CrewAgentExecutor chain" in cleaned_data:
            # Apply different color and switch color index
            self.color_index = (self.color_index + 1) % len(self.colors)  # Increment color index and wrap around if necessary

            cleaned_data = cleaned_data.replace("Entering new CrewAgentExecutor chain", f":{self.colors[self.color_index]}[Entering new CrewAgentExecutor chain]")

        if "City Selection Expert" in cleaned_data:
            # Apply different color 
            cleaned_data = cleaned_data.replace("City Selection Expert", f":{self.colors[self.color_index]}[City Selection Expert]")
        if "Local Expert at this city" in cleaned_data:
            cleaned_data = cleaned_data.replace("Local Expert at this city", f":{self.colors[self.color_index]}[Local Expert at this city]")
        if "Amazing Travel Concierge" in cleaned_data:
            cleaned_data = cleaned_data.replace("Amazing Travel Concierge", f":{self.colors[self.color_index]}[Amazing Travel Concierge]")
        if "Finished chain." in cleaned_data:
            cleaned_data = cleaned_data.replace("Finished chain.", f":{self.colors[self.color_index]}[Finished chain.]")

        self.buffer.append(cleaned_data)
        if "\n" in data:
            self.expander.markdown(''.join(self.buffer), unsafe_allow_html=True)
            self.buffer = []
