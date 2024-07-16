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
    base_path = f'multi_agents_system/src/tools/data/outputs/{model_name}'
    files = [
        "BRD_draft.md",
        "compliance_report.md",
        "data_dictionary.json",
        "final_BRD.md",
        "market_research_document.md",
        "preliminary_requirement_profiling_document.md",
        "project_plan.md"
    ]
    for file_name in files:
        file_path = os.path.join(base_path, file_name)
        if os.path.exists(file_path):
            with st.expander(file_name):
                content = load_file_to_display(file_path)
                if file_name.endswith('.md'):
                    st.markdown(content)
                elif file_name.endswith('.json'):
                    st.json(json.loads(content))
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