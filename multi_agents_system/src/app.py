import os
import sys
import shutil
from dotenv import set_key, load_dotenv
import time

from utils import StreamToExpander
from agents import Agents
from tools.input_extraction_tools import InputExtractionTools
from tools.search_and_scrape_tools import SearchAndScrapeTools
from tools.compliance_tools import ComplianceTools
from tasks import AgentTasks

from crewai import Crew, Process
import streamlit as st
from st_pages import hide_pages, show_pages, Page

# Setup directories
env_file_path = './multi_agents_system/src/.env'
input_dir = "multi_agents_system/src/tools/data/inputs"
gdpr_dir = 'multi_agents_system/src/tools/data/documents'

def setup_page():
    st.set_page_config(
        page_title="Multi-Agent Requirement Analysis and Specification",
        page_icon="📝",
        layout="wide",
        menu_items={
            'Report a bug': "https://github.com/codebrain001/msc-dissertation/issues/",
            'About': "## This tool helps in automating and enhancing software requirement analysis and specification process."
        }
    )
    show_pages([Page("multi_agents_system/src/app.py")])
    hide_pages([Page("multi_agents_system/src/pages/ 1_🔍_outputs_viewer.py")])

def write_to_env_file(filepath, key, value):
    if os.path.exists(filepath):
        load_dotenv(filepath)
    set_key(filepath, key, value)

def sidebar_configuration(disabled):
    st.sidebar.title("Configuration")
    st.sidebar.markdown("### Select LLM")
    llm_options = ["GPT-3.5-turbo", "GPT-4o", "Open-mixtral-8x22b", "Mistral-medium"]
    selected_llm = st.sidebar.selectbox("Choose LLM", llm_options, index=0, disabled=disabled, key="llm_selectbox")
    selected_llm = selected_llm.lower()
    st.sidebar.markdown("### API Key")
    api_key = st.sidebar.text_input("Enter your API key", type="password", disabled=disabled, key="api_key_input")

    create_agents_disabled = disabled or not selected_llm or not api_key
    create_agents_button = st.sidebar.button("Create Agentic", disabled=create_agents_disabled, key="create_agent_button")

    if create_agents_button:
        env_file_path = './multi_agents_system/src/.env'

        if 'gpt' in selected_llm:
            env_key = 'OPENAI_API_KEY'
        elif 'mistral' in selected_llm:
            env_key = 'MISTRAL_API_KEY'
        else:
            env_key = None
        if env_key:
            write_to_env_file(env_file_path, env_key, api_key)
            st.toast(f"{env_key} has been updated in app environment")

    return selected_llm, create_agents_button

def upload_preliminary_documents():
    st.title("Requirement Analysis and Specification with LLM Agents")
    st.info("Upload Preliminary Meeting Documents", icon="ℹ️")
    uploaded_files = st.file_uploader(
        "Choose documents",
        type=["doc", "docx", "txt", "pdf", "mp4", "mp3"],
        accept_multiple_files=True
    )
    if uploaded_files:
        save_uploaded_files_path = "./multi_agents_system/src/tools/data/inputs/"
        os.makedirs(save_uploaded_files_path, exist_ok=True)

        for uploaded_file in uploaded_files:
            file_path = os.path.join(save_uploaded_files_path, uploaded_file.name)
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.toast(f"Uploaded and saved: {uploaded_file.name}")
    return uploaded_files

def get_agentic_crew(model_name):
    input_extraction_tools = InputExtractionTools(input_dir=input_dir, model_name=model_name, load_collection_status=False)
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
    research_task = agent_tasks.create_research_task(preliminary_profiling_task)
    requirement_development_task = agent_tasks.create_requirement_development_task(preliminary_profiling_task, research_task)
    compliance_task = agent_tasks.create_compliance_task(requirement_development_task)
    data_dictionary_task = agent_tasks.create_data_dictionary_task(requirement_development_task, compliance_task)
    project_management_task = agent_tasks.create_project_management_task(requirement_development_task, compliance_task)
    quality_assurance_task = agent_tasks.create_quality_assurance_task(requirement_development_task, compliance_task, project_management_task)
     # Creating the crew
    requirement_analysis_and_specification_crew = Crew(
        agents=[preliminary_requirement_profiling_agent,
                research_agent,
                requirement_development_agent,
                compliance_agent,
                data_dictionary_agent,
                project_management_agent,
                quality_assurance_agent
            ],
        tasks=[
            preliminary_profiling_task,
            research_task,
            requirement_development_task,
            compliance_task,
            data_dictionary_task,
            project_management_task,
            quality_assurance_task
        ],
        verbose=1,
        memory=True
    )
    return requirement_analysis_and_specification_crew

def main():
    setup_page()
    st.sidebar.info("Sidebar configuration will be enabled after files are uploaded.")
    uploaded_files = upload_preliminary_documents()

    if uploaded_files:
        model_name, create_agents_button = sidebar_configuration(disabled=False)
        if create_agents_button and model_name:
            st.session_state.model_name = model_name
            with st.spinner('Agentic Workflow Execution started...'):
                time.sleep(3)
            requirement_analysis_and_specification_crew = get_agentic_crew(model_name)
            with st.spinner('Indexing Uploaded document...'):
                time.sleep(30)
            with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
                with st.container(height=500, border=False):
                    sys.stdout = StreamToExpander(st)
                    result = requirement_analysis_and_specification_crew.kickoff()
                status.update(label="✅ Requirement Analysis and Specification Successful!",
                      state="complete", expanded=False)
            st.subheader('View Agentic Workflow Outputs', anchor=False, divider="rainbow")
            st.info("This section allows you to view the outputs of the agentic workflow. Click the link below to access the Output Viewer Page.")
            st.page_link("pages/1_🔍_outputs_viewer.py", label="Output Viewer", icon="1️⃣")

            # Remove uploaded document(s)
            for file_name in os.listdir(input_dir):
                file_path = os.path.join(input_dir, file_name)
                try:
                    shutil.rmtree(file_path)
                except Exception as e:
                    st.error(f'Failed to delete {file_path}. Reason: {e}')
                    st.toast("Uploaded document(s) removed from App.")

if __name__ == "__main__":
    main()