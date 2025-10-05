# main.py

import os
import json
from dotenv import load_dotenv
from preprocessor_agent import PreprocessorAgent
from rule_checker_agent import RuleCheckerAgent
from llm_evaluator_agent import LLMEvaluatorAgent
from aggregator_agent import AggregatorAgent

class ResumeCoach:
    """Orchestrates the entire resume analysis workflow."""

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file. Please create one.")

        self.preprocessor = PreprocessorAgent()
        self.rule_checker = RuleCheckerAgent()
        self.llm_evaluator = LLMEvaluatorAgent(api_key)
        self.aggregator = AggregatorAgent()

    def analyze(self, resume_path: str, target_job_role: str):
        """Runs the full agentic pipeline for resume analysis."""
        print(f"--- Starting Analysis for role: {target_job_role} ---")

        # 1. Pre-processor Agent
        print("Step 1/5: Pre-processing resume file...")
        resume_text = self.preprocessor.extract_text(resume_path)
        page_count = self.preprocessor.get_page_count(resume_path)
        sections = self.preprocessor.identify_sections(resume_text)

        # 2. Rule Checker Agent
        print("Step 2/5: Running deterministic rule checks...")
        rule_feedback = self.rule_checker.check_rules(resume_text, page_count)

        # 3. LLM Evaluator Agent (Persona Generation)
        print("Step 3/5: Generating ideal candidate persona...")
        role_persona_json = self.llm_evaluator.generate_role_persona(target_job_role)

        # 4. LLM Evaluator Agent (Category Analysis)
        print("Step 4/5: Evaluating resume categories with AI...")
        llm_evaluations = {}
        categories_to_analyze = ["summary", "experience", "skills", "relevance"]
        for category in categories_to_analyze:
            print(f"  - Analyzing {category}...")
            section_text = sections.get(category, resume_text if category in ['relevance'] else '')
            llm_evaluations[category] = self.llm_evaluator.analyze_category(
                category, section_text, role_persona_json
            )

        # 5. Aggregator Agent
        print("Step 5/5: Aggregating scores and generating report...")
        final_report = self.aggregator.aggregate_scores(llm_evaluations, rule_feedback)
        
        print("\n--- Analysis Complete! ---")
        return final_report

# --- Example Usage ---
if __name__ == '__main__':
    # Create a dummy resume file for testing
    with open("sample_resume.txt", "w") as f:
        f.write("""
        Jane Smith
        jane.smith@email.com | (555) 123-4567

        Professional Summary
        Data professional with 3 years of experience in turning raw data into actionable insights.

        Experience
        Data Analyst | DataCorp | June 2022 - Present
        - Worked with large datasets to identify trends.
        - Created weekly reports for management.
        - Helped clean and prepare data for analysis.

        Skills
        - SQL, Python, R
        - Microsoft Excel, Tableau
        - Communication
        """)

    # --- INPUTS ---
    RESUME_FILE_PATH = "sample_resume.txt"
    TARGET_JOB_ROLE = "Junior Data Analyst"

    try:
        coach = ResumeCoach()
        report = coach.analyze(RESUME_FILE_PATH, TARGET_JOB_ROLE)
        print("\n--- FINAL AI RESUME REPORT ---")
        
        print(report)
    except Exception as e:
        print(f"An error occurred: {e}")