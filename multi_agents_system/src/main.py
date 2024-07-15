from agents import Agents
from tools.input_extraction_tools import InputExtractionTools
from tools.search_and_scrape_tools import SearchAndScrapeTools
from tools.compliance_tools import ComplianceTools
from tasks import AgentTasks
from crewai import  Crew

if __name__ == "__main__":
    model_name = "gpt-3.5-turbo"
    input_dir = "multi_agents_system/src/tools/data/inputs"
    gdpr_dir = 'multi_agents_system/src/tools/data/documents'
    input_extraction_tools = InputExtractionTools(input_dir=input_dir, model_name=model_name, load_collection_status=True)
    search_and_scrape_tools = SearchAndScrapeTools()
    compliance_tools = ComplianceTools(input_dir=gdpr_dir, model_name=model_name,  load_collection_status=True)


    # Initialize Agents with the input extraction tools
    agents = Agents(input_extraction_tools, search_and_scrape_tools, compliance_tools)
    preliminary_requirement_profiling_agent = agents.preliminary_requirement_profiling_agent()
    research_agent = agents.research_agent()
    compliance_agent = agents.compliance_agent()
    requirement_development_agent = agents.requirement_development_agent()
    data_dictionary_agent = agents.data_dictionary_agent()
    project_management_agent = agents.project_management_agent()
    quality_assurance_agent = agents.quality_assurance_agent()

    # Instantiate AgentTasks with the initialized agents
    agent_tasks = AgentTasks(
        model_name,
        preliminary_requirement_profiling_agent,
        research_agent,
        compliance_agent,
        requirement_development_agent,
        data_dictionary_agent,
        project_management_agent,
        quality_assurance_agent
    )

    # Create tasks
    preliminary_profiling_task = agent_tasks.create_preliminary_profiling_task()
    print(preliminary_requirement_profiling_agent.execute_task(preliminary_profiling_task))

    # # Create tasks
    # preliminary_profiling_task = agent_tasks.create_preliminary_profiling_task()
    # research_task = agent_tasks.create_research_task(preliminary_profiling_task)
    # requirement_development_task = agent_tasks.create_requirement_development_task(preliminary_profiling_task, research_task)
    # compliance_task = agent_tasks.create_compliance_task(requirement_development_task)
    # data_dictionary_task = agent_tasks.create_data_dictionary_task(requirement_development_task, compliance_task)
    # project_management_task = agent_tasks.create_project_management_task(requirement_development_task, compliance_task)
    # quality_assurance_task = agent_tasks.create_quality_assurance_task(requirement_development_task, compliance_task, project_management_task)

    # # Creating the crew
    # requirement_analysis_and_specification_crew = Crew(
    #     agents=[preliminary_requirement_profiling_agent,
    #             research_agent,
    #             requirement_development_agent,
    #             compliance_agent,
    #             data_dictionary_agent,
    #             project_management_agent,
    #             quality_assurance_agent
    #         ],
    #     tasks=[
    #         preliminary_profiling_task,
    #         research_task,
    #         requirement_development_task,
    #         compliance_task,
    #         data_dictionary_task,
    #         project_management_task,
    #         quality_assurance_task
    #     ],
    #     verbose=2,
    #     memory=True
    # )

    # # Run the crew
    # result = requirement_analysis_and_specification_crew.kickoff()

