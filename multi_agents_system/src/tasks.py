from crewai import Task
from pydantic import BaseModel
from typing import List, Optional

class DataDictionary(BaseModel):
   attribute_name: str
   description: str
   data_type: str
   maximum_length: int
   minimum_length: int
   allowed_values: str
   nullable: bool
   default_value: Optional[str]
   constrainst: Optional[str]
   related_to: Optional[List[str]]

class AgentTasks:
    def __init__(self, preliminary_requirement_profiling_agent, research_agent, compliance_agent,
                 requirement_development_agent, data_dictionary_agent, project_management_agent,
                 quality_assurance_agent):
        self.preliminary_requirement_profiling_agent = preliminary_requirement_profiling_agent
        self.research_agent = research_agent
        self.compliance_agent = compliance_agent
        self.requirement_development_agent = requirement_development_agent
        self.data_dictionary_agent = data_dictionary_agent
        self.project_management_agent = project_management_agent
        self.quality_assurance_agent = quality_assurance_agent

    def create_preliminary_profiling_task(self):
        return Task(
            description=(
                "Thoroughly analyze the preliminary meeting notes to identify and extract key project requirements, objectives, and stakeholder needs. "
                "Summarize the essential points to provide a foundational understanding of the project scope, "
                "ensuring all critical aspects are captured for subsequent phases."
            ),
            expected_output=(
                "A well structured analysis document detailing the initial project requirements, objective and stakeholder needs. "
                "This document should clearly outline the foundational elements necessary for the project's development."
            ),
            agent=self.preliminary_requirement_profiling_agent,
            output_file='multi_agents_system/src/tools/data/outputs/preliminary_requirement_profiling_document.md',
        )

    def create_research_task(self, preliminary_profiling_task):
        return Task(
            description=(
                "Conduct an in-depth market and competitive research based on the preliminary requirement profiling task. "
                "Gather and analyze relevant market data, examine competition, and identify current and emerging technological trends. "
                "This research will help inform strategic decisions and highlight potential opportunities and threats."
            ),
            expected_output=(
                "A comprehensive report written that covers the following sub sections: "
                "1. Market Analysis: Detailed insights into market size, growth potential, and key market segments. Analysis of consumer behavior and preferences relevant to the project."
                "2. Competitor Analysis: In-depth evaluation of direct and indirect competitors, including their strengths, weaknesses, market positioning, and strategies. "
                "Identification of competitors' key products or services and their market share. "
                "3. Technological Trends: Overview of current and emerging technologies that could impact the project. "
                "Analysis of technology adoption trends, innovation drivers, and potential technological disruptions. "
                "4. Opportunities and Threats: Identification of market opportunities and potential threats."
            ),
            agent=self.research_agent,
            context=[preliminary_profiling_task],
            output_file='multi_agents_system/src/tools/data/outputs/market_research_document.md',
            async_execution=True
        )

    def create_compliance_task(self, preliminary_profiling_task, research_task):
        return Task(
            description=(
                "Perform a comprehensive compliance analysis on the preliminary requirement profiling task and market research task to ensure all findings comply with GDPR regulations. "
                "Conduct a Data Protection Impact Assessment (DPIA) and develop a robust compliance strategy. "
                "Document all necessary compliance measures to safeguard data privacy and security."
            ),
            expected_output=(
                "A detailed compliance report that includes the following: "
                "1. Compliance Analysis: Assessment of the preliminary requirement profiling and market research findings to ensure alignment with GDPR regulations. "
                "2. DPIA Report: Comprehensive Data Protection Impact Assessment detailing potential data privacy risks and mitigation strategies. "
                "3. Compliance Strategy: A well-defined compliance strategy outlining the measures and procedures to ensure ongoing GDPR compliance. "
                "4. Documentation: Thorough documentation of all compliance measures, including policies, procedures, and any necessary records to demonstrate GDPR adherence. "
                "This report should ensure the project meets all GDPR standards and maintains robust data privacy and security protocols."
            ),
            context=[preliminary_profiling_task, research_task],
            agent=self.compliance_agent,
            async_execution=True
        )

    def create_requirement_development_task(self, preliminary_profiling_task, research_task, compliance_task):
        return Task(
            description=(
                "Develop detailed functional and non-functional requirements based on insights gained from the preliminary profiling and market research. "
                "Create comprehensive user stories and acceptance criteria for each requirement, ensuring they align with stakeholder needs and project objectives."
            ),
            expected_output=(
                "A detailed business requirement document draft containing the project's functional and non-functional requirements, "
                "along with well-defined user stories and acceptance criteria. "
                "This document should ensure all project requirements are clearly articulated and actionable."
            ),
            context=[preliminary_profiling_task, research_task, compliance_task],
            agent=self.requirement_development_agent,
            output_file='multi_agents_system/src/tools/data/outputs/BRD_draft.md',
            async_execution=True
        )


    def create_data_dictionary_task(self, preliminary_profiling_task, research_task, compliance_task):
        return Task(
            description=(
                "Identify and define key data elements required for the project. "
                "Specify data types, formats, and validation rules, and establish relationships between data elements. "
                "Document detailed metadata to support effective data management and ensure consistency throughout the project."
            ),
            expected_output=(
                "A comprehensive data dictionary that includes detailed metadata, data types, formats, validation rules, and relationships between data elements. "
                "This dictionary should facilitate effective data management and governance."
            ),
             context=[preliminary_profiling_task, research_task, compliance_task],
            agent=self.data_dictionary_agent,
            async_execution=True,
            output_json=DataDictionary,
            output_file="multi_agents_system/src/tools/data/outputs/data_dictionary.json",
        )

    def create_project_management_task(self, requirement_development_task):
        return Task(
            description=(
                "Develop a detailed project plan and timeline, including estimated timelines for each project phase. "
                "Allocate resources effectively and develop a risk management plan to anticipate and mitigate potential challenges, "
                "ensuring the project stays on track and within budget."
            ),
            expected_output=(
                "A comprehensive project plan document outlining project milestones, deliverables, estimated timelines, resource allocation, and risk management strategies. "
                "This plan should provide a clear roadmap for successful project execution. "
            ),
            context=[requirement_development_task],
            agent=self.project_management_agent,
            output_file="multi_agents_system/src/tools/data/outputs/project_plan.md",
            async_execution=True
        )

    def create_quality_assurance_task(self, requirement_development_task):
        return Task(
            description=(
                "Review the Business Requirement Document (BRD) draft from the requirement development task to ensure its completeness and accuracy. "
                "Enhance and finalize the document, ensuring it includes comprehensive functional and non-functional requirements as well as detailed user stories. "
                "Follow best practices in business analysis and software engineering throughout the process. "
                "Additionally, include a thorough project summary that encapsulates the key elements and findings of the project. "
            ),
            expected_output=(
                "A rewritten draft of the Business Requirement Document (BRD) that includes: "
                "Comprehensive Functional Requirements: Detailed descriptions of all functional requirements, "
                "ensuring they are clear, complete, and aligned with project objectives. "
                "1. Comprehensive Non-Functional Requirements: Detailed descriptions of all non-functional requirements, "
                "including performance, usability, reliability, and security criteria. "
                "2. Detailed User Stories: Thoroughly defined user stories that capture the end-users' needs and expected outcomes. "
                "3. Project Summary: A comprehensive summary of the project, "
                "including key findings, objectives, and any critical insights derived during the quality assurance process. "
                "This rewritten draft should ensure the BRD is of the highest quality and fully prepared for the next stages of the project."
            ),
            context=[requirement_development_task],
            agent=self.quality_assurance_agent,
            output_file="multi_agents_system/src/tools/data/outputs/final_BRD.md",
        )
