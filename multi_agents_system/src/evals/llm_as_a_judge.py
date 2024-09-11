from utils import read_pdf, aggregate_model_outputs
import os
import pandas as pd
from prometheus_eval.litellm import LiteLLM
from prometheus_eval import PrometheusEval
from prometheus_eval.prompts import SCORE_RUBRIC_TEMPLATE


input_file_path = "../tools/data/test_document/Meeting_Notes_001.pdf"
expected_output_file_path = "../tools/data/Expected_Outputs.pdf"
input = read_pdf(input_file_path)
reference_output = read_pdf(expected_output_file_path)
claude_sonnet_output_set = aggregate_model_outputs('../tools/data/outputs/claude-3-5-sonnet-20240620')
gpt4o_output_set = aggregate_model_outputs('../tools/data/outputs/gpt-4o')
gemini_pro_output_set = aggregate_model_outputs('../tools/data/outputs/gemini-1.5-pro')

hf_token = os.getenv("HUGGINGFACE_API_KEY")
os.environ["HUGGINGFACE_API_KEY"] = hf_token
model = LiteLLM('huggingface/prometheus-eval/prometheus-7b-v2.0')
judge = PrometheusEval(model=model)

input_file_path = "../tools/data/test_document/Meeting_Notes_001.pdf"
expected_output_file_path = "../tools/data/Expected_Outputs.pdf"
input = read_pdf(input_file_path)
reference_output = read_pdf(expected_output_file_path)
claude_sonnet_output_set = aggregate_model_outputs('../tools/data/outputs/claude-3-5-sonnet-20240620')
gpt4o_output_set = aggregate_model_outputs('../tools/data/outputs/gpt-4o')
gemini_pro_output_set = aggregate_model_outputs('../tools/data/outputs/gemini-1.5-pro')


instruction = f"You are to evaluate the content quality using the accuarcy (The information in the document is correct and factual) based on the input: {input}"
response = claude_sonnet_output_set
reference_answer = reference_output

# Rubric data for accuracy evaluation
rubric_data = {
  "criteria": "Is the information in the document correct and factual?",
  "score1_description": "The information is mostly incorrect or misleading, with many factual errors and inaccuracies.",
  "score2_description": "The information contains several factual errors or inaccuracies, and the overall reliability is low.",
  "score3_description": "The information is somewhat accurate, but there are notable errors or omissions that affect its reliability.",
  "score4_description": "The information is mostly accurate, with only minor errors or inaccuracies that do not significantly impact its reliability.",
  "score5_description": "The information is highly accurate and factual, with no significant errors or inaccuracies."
}

score_rubric = SCORE_RUBRIC_TEMPLATE.format(**rubric_data)

feedback, score = judge.single_absolute_grade(
    instruction=instruction,
    response=response,
    rubric=score_rubric,
    reference_answer=reference_answer
)

print("Feedback:", feedback)
print("Score:", score)
