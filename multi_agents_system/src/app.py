import os
import sys
from dotenv import load_dotenv
import time
import csv
import logging
import nest_asyncio

from utils import StreamToExpander
from agents import Agents
from tools.input_extraction_tools import InputExtractionTools
from tools.search_and_scrape_tools import SearchAndScrapeTools
from tools.compliance_tools import ComplianceTools
from tasks import AgentTasks

from crewai import Crew, Process
from langchain_openai import ChatOpenAI
from langchain_anthropic import ChatAnthropic
from langchain_google_genai import ChatGoogleGenerativeAI
import streamlit as st

# Load environment variables
env_file_path = './multi_agents_system/src/.env'
load_dotenv(dotenv_path=env_file_path)
# Setup directories
input_dir = "multi_agents_system/src/tools/data/inputs"
gdpr_dir = 'multi_agents_system/src/tools/data/documents'

# Apply nest_asyncio to allow nested event loops
nest_asyncio.apply()

# Configure logging
logging.basicConfig(stream=sys.stdout, level=logging.WARNING)
logging.getLogger().addHandler(logging.StreamHandler(stream=sys.stdout))

def setup_page():
    st.set_page_config(
        page_title="Multi-Agent Requirement Analysis and Specification",
        page_icon="🏠",
        layout="wide",
        menu_items={
            'Report a bug': "https://github.com/codebrain001/msc-dissertation/issues/",
            'About': "## This tool helps in automating and enhancing software requirement analysis and specification process."
        }
    )

def sidebar_configuration(disabled):
    st.sidebar.title("Configuration")
    st.sidebar.markdown("### Select LLM")
    llm_options = ["GPT-4o",  'cCaude-3-5-Sonnet-20240620', 'Gemini-1.5-Pro']
    selected_llm = st.sidebar.selectbox("Choose LLM", llm_options, index=0, disabled=disabled, key="llm_selectbox")
    selected_llm = selected_llm.lower()
    st.session_state.model_name = selected_llm
    st.sidebar.markdown("### API Key")
    api_key = st.sidebar.text_input("Enter your API key", type="password", disabled=disabled, key="api_key_input")

    create_agents_disabled = disabled or not selected_llm or not api_key
    create_agents_button = st.sidebar.button("Create Agentic", disabled=create_agents_disabled, key="create_agent_button")
    return selected_llm, api_key, create_agents_button

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

def initialize_manager_llm(model_name, api_key):
    try:
        if model_name == "gpt-4o":
            return ChatOpenAI(model=model_name, api_key=api_key, temperature=0)
        elif model_name == 'claude-3-5-sonnet-20240620':
            return ChatAnthropic(model=model_name, api_key=api_key, temperature=0)
        elif model_name == 'gemini-1.5-pro':
            return ChatGoogleGenerativeAI(model=f'models/{model_name}', api_key=api_key, temperature=0)
        else:
            st.error(f'Unsupported model name: {model_name}')
            return None
    except Exception as e:
        st.error(f"Error initializing manager LLM: {e}")
        return None

def create_agentic_crew(model_name, api_key, manager_llm):
    search_and_scrape_tools = SearchAndScrapeTools()
    compliance_tools = ComplianceTools(input_dir=gdpr_dir, model_name=model_name, api_key=api_key, load_collection_status=True)
    input_extraction_tools = InputExtractionTools(input_dir=input_dir, model_name=model_name, api_key=api_key, load_collection_status=True)

    agents = Agents(model_name, api_key, input_extraction_tools, search_and_scrape_tools, compliance_tools)
    preliminary_requirement_profiling_agent = agents.preliminary_requirement_profiling_agent()
    research_agent = agents.research_agent()
    requirement_development_agent = agents.requirement_development_agent()
    compliance_agent = agents.compliance_agent()
    data_dictionary_agent = agents.data_dictionary_agent()
    quality_assurance_agent = agents.quality_assurance_agent()
    project_management_agent = agents.project_management_agent()

    agent_tasks = AgentTasks(
        model_name,
        preliminary_requirement_profiling_agent,
        research_agent,
        requirement_development_agent,
        compliance_agent,
        data_dictionary_agent,
        quality_assurance_agent,
        project_management_agent
    )

    # Create tasks
    preliminary_profiling_task = agent_tasks.create_preliminary_profiling_task()
    research_task = agent_tasks.create_research_task(preliminary_profiling_task)
    requirement_development_task = agent_tasks.create_requirement_development_task(preliminary_profiling_task, research_task)
    compliance_task = agent_tasks.create_compliance_task(requirement_development_task)
    data_dictionary_task = agent_tasks.create_data_dictionary_task(requirement_development_task, compliance_task)
    quality_assurance_task = agent_tasks.create_quality_assurance_task(requirement_development_task, compliance_task)
    project_management_task = agent_tasks.create_project_management_task(quality_assurance_task)

    # Creating the crew
    requirement_analysis_and_specification_crew = Crew(
        agents=[
            preliminary_requirement_profiling_agent,
            research_agent,
            requirement_development_agent,
            compliance_agent,
            data_dictionary_agent,
            quality_assurance_agent,
            project_management_agent
        ],
        tasks=[
            preliminary_profiling_task,
            research_task,
            requirement_development_task,
            compliance_task,
            data_dictionary_task,
            quality_assurance_task,
            project_management_task,
        ],
        process=Process.hierarchical,
        verbose=True,
        memory=True,
        manager_llm=manager_llm,
    )
    return requirement_analysis_and_specification_crew

def main():
    setup_page()
    st.sidebar.info("Sidebar configuration will be enabled after files are uploaded.")
    uploaded_files = upload_preliminary_documents()

    if uploaded_files:
        model_name, api_key, create_agents_button = sidebar_configuration(disabled=False)
        if create_agents_button:
            start_time = time.time()
            st.toast('Agentic Workflow Execution started...')
            st.info('The agentic workflow will start after the uploaded document is indexed in the vector store.',  icon="1️⃣")

            manager_llm = initialize_manager_llm(model_name, api_key)
            requirement_analysis_and_specification_crew = create_agentic_crew(model_name, api_key, manager_llm)

            with st.spinner('Indexing Uploaded document...'):
                time.sleep(15)
            with st.status("🤖 **Agents at work...**", state="running", expanded=True) as status:
                with st.container(height=500, border=False):
                    sys.stdout = StreamToExpander(st)
                    result = requirement_analysis_and_specification_crew.kickoff()
                status.update(label="✅ Requirement Analysis and Specification Successful!",
                      state="complete", expanded=False)
            st.subheader('View Agentic Workflow Outputs', anchor=False, divider="rainbow")
            st.info("This section allows you to view the outputs of the agentic workflow. Click the link below to access the Output Viewer Page.")
            st.page_link("pages/1_outputs_viewer.py", label="Output Viewer", icon="1️⃣")

            end_time = time.time()
            elapsed_time = end_time - start_time
            # Remove uploaded input document(s)
            for file_name in os.listdir(input_dir):
                file_path = os.path.join(input_dir, file_name)
                try:
                    os.remove(file_path)
                except Exception as e:
                    st.error(f'Failed to delete {file_path}. Reason: {e}')
                    st.toast("Uploaded document(s) removed from App.")

            st.info(f"Time executed: {elapsed_time:.2f} seconds")

            # Save model name and execution time to CSV
            csv_file_path = 'multi_agents_system/src/tools/data/outputs/execution_times.csv'
            file_exists = os.path.isfile(csv_file_path)

            with open(csv_file_path, mode='a', newline='') as file:
                writer = csv.writer(file)
                if not file_exists:
                    writer.writerow(['Model Name', 'Execution Time (seconds)'])
                writer.writerow([model_name, f"{elapsed_time:.2f}"])

            st.toast(f"Execution details saved")

if __name__ == "__main__":
    main()


