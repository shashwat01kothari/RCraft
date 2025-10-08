# main.py

import os
import json
from dotenv import load_dotenv
from preprocessor_agent import PreprocessorAgent
from rule_checker_agent import RuleCheckerAgent
from llm_analyzer_agent import LLMAnalyzerAgent
from aggregator_agent import AggregatorAgent

class ResumeCoach:
    """Orchestrates the entire resume analysis workflow."""

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            raise ValueError("GOOGLE_API_KEY not found in .env file.")

        self.preprocessor = PreprocessorAgent()
        self.rule_checker = RuleCheckerAgent()
        self.llm_analyzer = LLMAnalyzerAgent(api_key)
        self.aggregator = AggregatorAgent()

    def analyze(self, resume_path: str, target_job_role: str):
        """Runs the full agentic pipeline using a holistic analysis approach."""
        print(f"--- Starting Holistic Analysis for role: {target_job_role} ---")

        # Step 1: Pre-processing and Rule Checking (Local)
        print("Step 1/4: Pre-processing and running local checks...")
        resume_text = self.preprocessor.extract_text(resume_path)
        page_count = self.preprocessor.get_page_count(resume_path)
        rule_feedback = self.rule_checker.check_rules(resume_text, page_count)
        print("  - Local processing complete.")

        # Step 2: Persona Generation (First API Call)
        print("Step 2/4: Generating ideal candidate persona...")
        role_persona_json = self.llm_analyzer.generate_role_persona(target_job_role)
        print("  - Persona generation complete.")

        # Step 3: Holistic Analysis (Second API Call)
        print("Step 3/4: Performing holistic resume analysis with AI...")
        holistic_eval_json = self.llm_analyzer.analyze_resume_holistically(
            resume_text, role_persona_json
        )
        print("  - Holistic AI analysis complete.")

        # Step 4: Aggregation (Local)
        print("Step 4/4: Aggregating scores and generating final report...")
        final_report = self.aggregator.aggregate_scores(holistic_eval_json, rule_feedback)
        
        print("\n--- Analysis Complete! ---")
        return final_report

# --- Main execution block ---
if __name__ == '__main__':
    with open("sample_resume.txt", "w") as f:
        f.write("""
        Jane Smith, PMP
        jane.s.smith@email.com | (555) 123-4567 | linkedin.com/in/janesmith

        Professional Summary
        I am a project manager with over 8 years of experience in the tech industry. I have worked on many successful projects and am a hardworking team player looking for a new challenge. Responsible for managing timelines and stakeholders.

        Work Experience
        Project Manager | Tech Solutions Inc. | Jan 2018 - Present
        - Helped the team to deliver a new software product.
        - Worked on creating project plans and status reports.
        - Responsible for a team of 5 developers.

        Skills
        - Project Management, Microsoft Project, Communication, Agile, Teamwork
        """)

    RESUME_FILE_PATH = "sample_resume.txt"
    TARGET_JOB_ROLE = "Senior IT Project Manager"

    try:
        coach = ResumeCoach()
        report = coach.analyze(RESUME_FILE_PATH, TARGET_JOB_ROLE)
        print("\n--- FINAL HOLISTIC AI REPORT ---")
        print(report)
    except Exception as e:
        print(f"\n--- An Error Occurred ---")
        print(f"An unexpected error stopped the analysis: {e}")