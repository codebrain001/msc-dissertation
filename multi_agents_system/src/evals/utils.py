import os
from PyPDF2 import PdfReader

def read_pdf(file_path):
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return ""

    with open(file_path, "rb") as file:
        reader = PdfReader(file)
        content = ""
        for page in reader.pages:
            content += page.extract_text() or ""
    return content


def aggregate_model_outputs(folder_path):
    file_order = [
        'preliminary_requirement_profiling_document.md',
        'market_research_document.md',
        'BRD_draft.md',
        'compliance_report.md',
        'data_dictionary.md',
        'final_BRD.md',
        'project_plan.md'
    ]
    model_outputs = ""

    for file_name in file_order:
        file_path = os.path.join(folder_path, file_name)
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as file:
                content = file.read()
                model_outputs += content + "\n\n"
        else:
            print(f"File {file_name} not found in the specified folder.")

    return model_outputs

