import streamlit as st
import os

def setup_page():
    # Add page title, page icon, and wide layout
    st.set_page_config(
        page_title="Multi-Agent Requirement Analysis",
        page_icon=":memo:",
        layout="wide",
        menu_items={
            'Report a bug': "https://github.com/your-repo/issues",
            'About': "## This tool helps in automating and enhancing software requirement analysis and specification process."
        }
    )

def sidebar_configuration():
    # Sidebar configuration for navigating different LLMs and inputting API keys
    st.sidebar.title("Configuration")
    st.sidebar.markdown("### Select LLM")
    llm_options = ["GPT-3.5", "GPT-4", "Mistral", "LLama3"]
    selected_llm = st.sidebar.selectbox("Choose LLM", llm_options, index=0)
    st.sidebar.markdown("### API Key")
    api_key = st.sidebar.text_input("Enter your API key", type="password")
    return selected_llm, api_key

def upload_preliminary_documents():
    st.title("Requirement Analysis and Specification with LLM Agents")
    st.info("Upload Preliminary Meeting Documents",  icon="ℹ️")
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

def main():
    setup_page()
    selected_llm, api_key = sidebar_configuration()
    uploaded_files = upload_preliminary_documents()

    if uploaded_files:
        st.write("Files uploaded successfully. Proceed with processing...")

if __name__ == "__main__":
    main()
