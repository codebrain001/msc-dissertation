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
                "Analyze the preliminary meeting notes provided"
                "to identify key project requirements, objectives, and stakeholder needs. "
                "Extract and summarize the essential points."
            ),
            expected_output=(
                "A structured document outlining the initial project requirements, objectives, "
                "and stakeholder needs."
            ),
            agent=self.preliminary_requirement_profiling_agent,
        )

    def create_research_task(self):
        return Task(
            description=(
                "Conduct comprehensive market and competitive research based on the project's "
                "initial requirements. Gather relevant market data, analyze competitors, and "
                "identify technological trends that could influence the success of the project."
            ),
            expected_output=(
                "A detailed report with market data, competitor analysis, and technological trends "
                "relevant to the project."
            ),
            agent=self.research_agent,
            async_execution=True
        )

    def create_compliance_task(self):
        return Task(
            description=(
                "Ensure that the project complies with GDPR regulations. Conduct a Data Protection "
                "Impact Assessment (DPIA) and develop a compliance strategy. Document all necessary "
                "compliance measures."
            ),
            expected_output=(
                "A comprehensive compliance report including the DPIA, compliance strategy, and "
                "detailed documentation of GDPR compliance measures."
            ),
            agent=self.compliance_agent,
            async_execution=True
        )

    def create_requirement_development_task(self, preliminary_profiling_task, research_task, compliance_task):
        return Task(
            description=(
                "Develop detailed functional and non-functional requirements based on the initial "
                "profiling and research. Create user stories and acceptance criteria for each requirement."
            ),
            expected_output=(
                "A document containing detailed functional and non-functional requirements, user stories, "
                "and acceptance criteria."
            ),
            context=[preliminary_profiling_task, research_task, compliance_task],
            agent=self.requirement_development_agent,
            async_execution=True
        )


    def create_data_dictionary_task(self, preliminary_profiling_task, research_task, compliance_task):
        return Task(
            description=(
                "Identify key data elements required for the project. Define data types, formats, and "
                "validation rules. Establish relationships between data elements and document metadata."
            ),
            expected_output=(
                "A comprehensive data dictionary with detailed metadata, data types, formats, validation rules, "
                "and relationships between data elements."
            ),
             context=[preliminary_profiling_task, research_task, compliance_task],
            agent=self.data_dictionary_agent,
            async_execution=True,
            output_json=DataDictionary,
            output_file="data_dictionary.json",
        )

    def create_project_management_task(self, requirement_development_task):
        return Task(
            description=(
                "Develop a detailed project plan and timeline. Estimate timelines for each phase of the project, "
                "allocate resources, and develop a risk management plan."
            ),
            expected_output=(
                "A project plan document including milestones, deliverables, estimated timelines, resource allocation, "
                "and risk management strategies."
            ),
            context=[requirement_development_task],
            agent=self.project_management_agent,
            output_file="project_plan.md",
            async_execution=True
        )

    def create_quality_assurance_task(self, requirement_development_task, project_management_task):
        return Task(
            description=(
                "Review the Business Requirement Document (BRD) for completeness and correctness. Ensure adherence to "
                "best practices in business analysis and software engineering. Generate a comprehensive project summary."
            ),
            expected_output=(
                "A final BRD document meeting the highest standards of quality and accuracy, along with a comprehensive "
                "project summary."
            ),
             context=[requirement_development_task, project_management_task],
            agent=self.quality_assurance_agent,
            output_file="final_BRD.md",
        )
