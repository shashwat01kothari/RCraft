from typing import Dict, Any
from ..parsers import get_parser
from ..agents.llm_structuring_agent import LLMStructuringAgent
from ..agents.llm_analyser_agent import LLMAnalyserAgent

class ResumeProcessingService:
    """Orchestrates the resume parsing and analysis workflow."""

    def __init__(self):
        # The service now holds instances of the agents it depends on.
        self.structuring_agent = LLMStructuringAgent()
        self.analyser_agent = LLMAnalyserAgent()

    def process_resume(self, file_path: str, job_description: str) -> Dict[str, Any]:
        """The main public method to process a resume file against a job description."""
        try:
            # Step 1: Select the correct parser and extract raw text
            Parser_class = get_parser(file_path)
            parser = Parser_class()
            with open(file_path, "rb") as f:
                print(f"Parsing {file_path} for raw text...")
                raw_text = parser.parse_to_text(f)
                if not raw_text or raw_text.isspace():
                    raise ValueError("Could not extract any text from the provided file.")
                print("Raw text extracted successfully.")

            # Step 2: Use the structuring agent to get structured data
            print("Structuring raw text with LLM...")
            resume_data = self.structuring_agent.structure_resume_text(raw_text)
            print("Structuring complete.")

            # Step 3: Use the analyser agent to get the analysis
            print("Analyzing resume against job description...")
            analysis_result = self.analyser_agent.analyze(resume_data, job_description)
            print("Analysis complete.")

            # Step 4: Return the combined results
            return {
                "parsed_resume": resume_data.model_dump(),
                "analysis": analysis_result.model_dump()
            }
        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": f"An unexpected error occurred: {e}"}