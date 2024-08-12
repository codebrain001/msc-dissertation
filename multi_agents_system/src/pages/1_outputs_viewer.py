import streamlit as st
import os
import json

def setup_page():
    # Add page title, page icon, and wide layout
    st.set_page_config(
        page_title="Outputs Viewer",
        page_icon="📝",
        layout="wide",
        menu_items={
            'Report a bug': "https://github.com/codebrain001/msc-dissertation/issues/",
            'About': "## This tool helps in automating and enhancing software requirement analysis and specification process."
        }
    )

def load_file_to_display(file_path):
    if file_path.endswith('.md'):
        with open(file_path, 'r') as file:
            return file.read()
    elif file_path.endswith('.json'):
        with open(file_path, 'r') as file:
            return json.dumps(json.load(file), indent=4)
    else:
        return "Unsupported file format."

def main(model_name):
    setup_page()
    st.write(st.session_state['model_name'])
    st.header('Business Requirements Analysis and Specification Results')
    st.subheader(f'Derived from AI Agents 🤖 Powered by Model: {model_name}')
    base_path = f'multi_agents_system/src/tools/data/outputs/{model_name}'
    files = [
        "preliminary_requirement_profiling_document.md",
        "market_research_document.md",
        "BRD_draft.md",
        "compliance_report.md",
        "data_dictionary.md",
        "project_plan.md",
        "final_BRD.md",
    ]
    for file_name in files:
        file_path = os.path.join(base_path, file_name)
        if os.path.exists(file_path):
            with st.expander(file_name):
                content = load_file_to_display(file_path)
                if file_name.endswith('.md'):
                    st.markdown(content)
                else:
                    st.write(content)
        else:
            st.warning(f"{file_name} does not exist in the specified path.")

if __name__ == "__main__":
    if 'model_name' in st.session_state:
        model_name = st.session_state.model_name
        main(model_name)
    else:
        st.error("Model name not found in session state.")
        st.info('Initiate the agentic workflow and please wait for its completion. Once the workflow is finished, you can then access the output page to view the results.', icon="ℹ️")