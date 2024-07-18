# Meeting Log

## Date: 2024-07-04
**Time:** 13:30 - 14:30

**Called By:** Ashley Williamson (Staff)
**Attendees:** Ashley Williamson (Staff), Aboze Brain John (Student)

**Hours spent on project since first meeting:** 112

**Brief description of work since last meeting:**
- Use of Git issues to track project progress, showcasing improved skill development from previous meetings.
- Completed 1st and 2nd iterations of the RAG system including a summary index and semantic search index
- Utilizing crew.ai for building multi agents system, with  asynchronous task definition as well as agent roles and tools accessible to agents.
- Utilized GPT-3.5 Turbo via OpenAI API primarily to power the LLM agents with definitions and placeholder made to enable GPT4o and Mistral models for future work.
- Attempted to modify the code to avoid re-indexing/re-ingesting source documents to reduce costs.
- Previous attempts to run models locally via Ollama were mentioned, but the current code does not support this yet.

**Issues identified:**
- Quality of output documents, especially JSON and Business Requirement Document(BRD) formats.
- Cost of re-indexing/re-ingesting source documents.
- VRAM limitations for local computation and talked about the possibility of using the Games Lab for local computatio
- Discussed implementing a lock mechanism to ensure ingestion happens only once, involving modifications to the SimpleDirectoryReader logic.

**Agreed tasks for next meeting:**
- Look up potential UK conferences for publishing work related to the project.
- Continue with the agentic approach in the project.
- Implement a lock mechanism to ensure ingestion happens only once, involving modifications to the SimpleDirectoryReader logic.
- Keep scientific documentation in mind, especially formalizing and documenting comparisons for the methodology section of the thesis.
- Experiment with prompting changes to improve JSON output, by considering one-shot or multi-shot prompting instead of the current zero-shot approach.
- Start some parts of the thesis write-up, focusing on literature and methodology sections.
- Explore the use of LaTeX and Overleaf for academic write-ups.
- Draft an evaluative methodology and plan involving human participants, including a literature review, questionnaire design, analysis methodology, recruitment methodology, and formal documentation (participant info sheet, etc.).
- Prepare and submit an ethics application with all required information clearly outlined. No studies involving human participants should commence until the ethics application is approved.

**Next meeting**
- Date: 2024-07-18
- Time: 11:30-12:00