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
            raise ValueError("GOOGLE_API_KEY not found in .env file. Please create one.")

        self.preprocessor = PreprocessorAgent()
        self.rule_checker = RuleCheckerAgent()
        self.llm_evaluator = LLMAnalyzerAgent(api_key)
        self.aggregator = AggregatorAgent()

    def analyze(self, resume_path: str, target_job_role: str):
        """Runs the full agentic pipeline for resume analysis."""
        print(f"--- Starting Full Analysis for role: {target_job_role} ---")

        # 1. Pre-processor Agent
        print("Step 1/5: Pre-processing resume file...")
        resume_text = self.preprocessor.extract_text(resume_path)
        page_count = self.preprocessor.get_page_count(resume_path)
        sections = self.preprocessor.identify_sections(resume_text)
        print("  - Resume text extracted and sections identified.")

        # 2. Rule Checker Agent
        print("Step 2/5: Running deterministic rule checks...")
        rule_feedback = self.rule_checker.check_rules(resume_text, page_count)
        print("  - Rule checks complete.")

        # 3. LLM Evaluator Agent (Persona Generation)
        print("Step 3/5: Generating ideal candidate persona...")
        role_persona_json = self.llm_evaluator.generate_role_persona(target_job_role)
        print("  - Persona generation complete.")

        # 4. LLM Evaluator Agent (Comprehensive Category Analysis)
        print("Step 4/5: Evaluating all resume categories with AI...")
        llm_evaluations = {}
        
        # --- ALL CATEGORIES ARE NOW INCLUDED ---
        categories_to_analyze = [
            "structure", "language", "ats", "summary", 
            "experience", "skills", "relevance"
        ]
        
        for category in categories_to_analyze:
            print(f"  - Analyzing '{category}'...")
            # Use specific sections for context-aware analysis, or full text for general analysis
            section_text = sections.get(category, resume_text)
            llm_evaluations[category] = self.llm_evaluator.analyze_category(
                category, section_text, role_persona_json
            )

        # 5. Aggregator Agent
        print("Step 5/5: Aggregating scores and generating final report...")
        final_report = self.aggregator.aggregate_scores(llm_evaluations, rule_feedback)
        
        print("\n--- Analysis Complete! ---")
        return final_report

# --- Example Usage ---
if __name__ == '__main__':
    # Using the same dummy resume file for consistency
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

        Project Coordinator | Web Innovators | June 2015 - Dec 2017
        - Assisted senior project managers.
        - Was tasked with organizing meetings.

        Skills
        - Project Management
        - Microsoft Project
        - Communication
        - Agile
        - Teamwork
        """)

    RESUME_FILE_PATH = "sample_resume.txt"
    TARGET_JOB_ROLE = "Senior IT Project Manager"

    try:
        coach = ResumeCoach()
        report = coach.analyze(RESUME_FILE_PATH, TARGET_JOB_ROLE)
        print("\n--- FULL AI RESUME REPORT ---")
        print(report)
    except Exception as e:
        print(f"An unexpected error occurred during the analysis: {e}")