import streamlit as st
import os
import time

def setup_page():
    # Add page title, page icon, and wide layout
    st.set_page_config(
        page_title="Multi-Agent Requirement Analysis and Specification",
        page_icon="📝",
        layout="wide",
        menu_items={
            'Report a bug': "https://github.com/codebrain001/msc-dissertation/issues/",
            'About': "## This tool helps in automating and enhancing software requirement analysis and specification process."
        }
    )

def sidebar_configuration(disabled):
    # Sidebar configuration for navigating different LLMs and inputting API keys
    st.sidebar.title("Configuration")
    st.sidebar.markdown("### Select LLM")
    llm_options = ["GPT-3.5", "GPT-4", "Mistral", "LLama3"]
    selected_llm = st.sidebar.selectbox("Choose LLM", llm_options, index=0, disabled=disabled, key="llm_selectbox")
    st.sidebar.markdown("### API Key")
    api_key = st.sidebar.text_input("Enter your API key", type="password", disabled=disabled, key="api_key_input")

    create_agent_disabled = disabled or not selected_llm or not api_key
    create_agent_button = st.sidebar.button("Create Agentic", disabled=create_agent_disabled, key="create_agent_button")

    if create_agent_button:
        st.sidebar.success("Agentic workflow creation in progress...")

    return selected_llm, api_key

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
            st.write(f"Uploaded and saved: {uploaded_file.name}")

    return uploaded_files

def main():
    setup_page()
    st.sidebar.info("Sidebar configuration will be enabled after files are uploaded.")
    uploaded_files = upload_preliminary_documents()

    if uploaded_files:
        selected_llm, api_key = sidebar_configuration(disabled=False)
        st.success("Files processed successfully. Proceed with selecting the respective LLM and input API keys to create respective agents...")
    else:
        sidebar_configuration(disabled=True)

if __name__ == "__main__":
    main()
