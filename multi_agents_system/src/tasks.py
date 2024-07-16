import os
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
    def __init__(self, model_name, preliminary_requirement_profiling_agent, research_agent, compliance_agent,
                 requirement_development_agent, data_dictionary_agent, project_management_agent,
                 quality_assurance_agent):
        self.model_name = model_name
        self.preliminary_requirement_profiling_agent = preliminary_requirement_profiling_agent
        self.research_agent = research_agent
        self.compliance_agent = compliance_agent
        self.requirement_development_agent = requirement_development_agent
        self.data_dictionary_agent = data_dictionary_agent
        self.project_management_agent = project_management_agent
        self.quality_assurance_agent = quality_assurance_agent
        self.base_output_path = f'multi_agents_system/src/tools/data/outputs/{model_name}'
        os.makedirs(self.base_output_path, exist_ok=True)

    def create_preliminary_profiling_task(self):
        return Task(
            description=(
                "Thoroughly analyze the preliminary meeting notes provided to key identify and extract key project requirements, objectives, and stakeholder needs. "
                "Summarize the essential points to provide a foundational understanding of the project scope, "
                "ensuring all critical aspects are captured for subsequent phases. "
                "Document the analysis in a clear and structured format."
            ),
            expected_output=(
                "A document titled 'Preliminary Meeting Notes Analysis' that should contain content covering the following areas: "
                "1. A detailed analysis of the initial project requirements. "
                "2. Clearly defined project objectives. "
                "3. Identified stakeholder needs and expectations. "
                "4. Any other relevant information extracted from the meeting notes. "
                "This document will serve as the foundation for subsequent project phases, ensuring that all critical aspects are captured."
            ),
            agent=self.preliminary_requirement_profiling_agent,
            output_file=f'{self.base_output_path}/preliminary_requirement_profiling_document.md',
        )

    def create_research_task(self, preliminary_profiling_task):
        return Task(
            description=(
                "Conduct an in-depth market and competitive research based on the preliminary requirement profiling task. "
                "Gather and analyze relevant market data, examine competition, and identify current and emerging technological trends. "
                "This research will help inform strategic decisions and highlight potential opportunities and threats."
            ),
            expected_output=(
                "A comprehensive document covering the following sub sections: "
                "1. Market Analysis: Detailed insights into market size, growth potential, and key market segments. Analysis of consumer behavior and preferences relevant to the project."
                "2. Competitor Analysis: In-depth evaluation of direct and indirect competitors, including their strengths, weaknesses, market positioning, and strategies. "
                "Identification of competitors' key products or services and their market share. "
                "3. Technological Trends: Overview of current and emerging technologies that could impact the project. "
                "Analysis of technology adoption trends, innovation drivers, and potential technological disruptions. "
                "4. Opportunities and Threats: Identification of market opportunities and potential threats."
            ),
            agent=self.research_agent,
            context=[preliminary_profiling_task],
            output_file=f'{self.base_output_path}/market_research_document.md',
        )

    def create_requirement_development_task(self, preliminary_profiling_task, research_task):
        return Task(
            description=(
                "Develop detailed functional and non-functional requirements based on insights gained from the preliminary profiling and market research. "
                "Create comprehensive user stories and acceptance criteria for each requirement, ensuring they align with stakeholder needs and project objectives. "
                "Document these requirements in a clear and structured format."
            ),
            expected_output=(
                "A document titled 'Business Requirements Document (BRD) Draft' that should contain content covering the following areas: "
                "1. Detailed functional requirements: Specific features and functionalities required for the project. "
                "2. Detailed non-functional requirements: Performance, security, usability, and other quality attributes. "
                "3. Comprehensive user stories: Clearly defined user stories that capture end-user needs and expected outcomes. "
                "4. Acceptance criteria: Specific conditions under which each requirement is met. "
                "This document should ensure all project requirements are clearly articulated and actionable, providing a solid foundation for the project's development."
            ),
            context=[preliminary_profiling_task, research_task],
            agent=self.requirement_development_agent,
            output_file=f'{self.base_output_path}/BRD_draft.md',
        )


    def create_compliance_task(self, requirement_development_task):
        return Task(
            description=(
                "Perform a comprehensive compliance analysis on the Business Requirements Document (BRD) draft obtained from the requirement development task to ensure all findings comply with GDPR regulations. "
                "Conduct a Data Protection Impact Assessment (DPIA) specifically for the requirements outlined in the BRD draft and develop a robust compliance strategy. "
                "Document all necessary compliance measures to safeguard data privacy and security, ensuring the project's adherence to GDPR standards."
            ),
            expected_output=(
               "A document titled 'Compliance Report for BRD Draft' that that should contain content covering the following areas: "
                "1. Compliance Analysis: Assessment of the BRD draft to ensure alignment with GDPR regulations. "
                "2. DPIA Report: Comprehensive Data Protection Impact Assessment detailing potential data privacy risks and mitigation strategies for the requirements specified in the BRD draft. "
                "3. Compliance Strategy: A well-defined compliance strategy outlining the measures and procedures to ensure ongoing GDPR compliance for the project. "
                "4. Documentation: Thorough documentation of all compliance measures, including policies, procedures, and any necessary records to demonstrate GDPR adherence. "
                "This report should ensure the project meets all GDPR standards and maintains robust data privacy and security protocols."
            ),
            context=[requirement_development_task],
            agent=self.compliance_agent,
            output_file=f'{self.base_output_path}/compliance_report.md',
        )

    def create_data_dictionary_task(self, requirement_development_task, compliance_task):
        return Task(
            description=(
                "Identify and define multiple key data attributes required for the project based on the Business Requirements Document (BRD) draft and the compliance strategy. "
                "Follow the Pydantic model for each data attribute, specify data types, formats, validation rules, and establish relationships between data elements. "
                "Document detailed metadata to support effective data management and ensure consistency throughout the project. "
                "Ensure that the data dictionary aligns with both the project requirements and compliance measures, encompassing all necessary data attributes."
            ),
            expected_output=(
                "A JSON file that contains the following structured data attributes using the Pydantic model: "
                "1. Metadata: Detailed metadata for each data attribute, including attribute name, description, source, and any relevant notes. "
                "2. Data Types and Formats: Clearly defined data types and formats for each attribute, ensuring alignment with the project's data schema. "
                "3. Validation Rules: Specific validation rules for each attribute, such as allowed ranges, patterns, or constraints. "
                "4. Relationships: Defined relationships between data elements, indicating how attributes are interconnected. "
                "5. Compliance Attributes: Any compliance-related data attributes as specified in the compliance strategy, with details on regulatory requirements and standards. "
                "This JSON file should be comprehensive to facilitate effective data management, governance, and ensure consistency across the project."
            ),
            context=[requirement_development_task, compliance_task],
            agent=self.data_dictionary_agent,
            async_execution=True,
            output_pydantic=DataDictionary, # Use the Pydantic model for structured output
            output_file=f"{self.base_output_path}/data_dictionary.json",
        )

    def create_project_management_task(self, requirement_development_task, compliance_task):
        return Task(
            description=(
                "Develop a detailed project plan and timeline based on the Business Requirements Document (BRD) draft and the compliance strategy. "
                "Include estimated timelines for each project phase, allocate resources effectively, and develop a risk management plan to anticipate and mitigate potential challenges. "
                "Ensure the project plan aligns with the project's requirements and compliance measures, ensuring the project stays on track and within budget."
            ),
            expected_output=(
                "A document titled 'Project Plan' that includes: "
                "1. Project milestones and deliverables. "
                "2. Estimated timelines for each project phase. "
                "3. Resource allocation details. "
                "4. Risk management strategies to anticipate and mitigate potential challenges. "
                "This plan should provide a clear roadmap for successful project execution, aligning with both project requirements and compliance measures."
            ),
            context=[requirement_development_task, compliance_task],
            agent=self.project_management_agent,
            output_file=f"{self.base_output_path}/project_plan.md",
            async_execution=True
        )

    def create_quality_assurance_task(self, requirement_development_task, compliance_task, project_management_task):
        return Task(
            description=(
                "Conduct a thorough review of the Business Requirements Document (BRD) draft from the requirement development task to ensure its completeness, accuracy, and alignment with the compliance strategy. "
                "Enhance and finalize the document by incorporating comprehensive functional and non-functional requirements, detailed user stories, and adhering to best practices in business analysis and software engineering. "
                "Additionally, include a thorough project summary that encapsulates the key elements and findings of the project, ensuring the BRD meets the highest quality standards."
            ),
            expected_output=(
                "A document titled 'Final Business Requirements Document (BRD)' that includes: "
                "1. Comprehensive Functional and Non-Functional Requirements: Detailed descriptions of all functional and non-functional requirements, "
                "presented in tabular form, ensuring they are clear, complete, and aligned with project objectives. "
                "2. Detailed User Stories: Thoroughly defined user stories that capture the end-users' needs and expected outcomes. "
                "3. Project Summary: A comprehensive summary of the project, including key findings, objectives, and any critical insights derived during the quality assurance process. "
                "This finalized BRD should ensure the project is fully prepared for the next stages and adheres to both project and compliance requirements."
            ),
            context=[requirement_development_task, compliance_task, project_management_task],
            agent=self.quality_assurance_agent,
            output_file=f"{self.base_output_path}/final_BRD.md",
        )
