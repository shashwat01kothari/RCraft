# backend/core/services/resume_analysis_service.py

import os
import tempfile
import logging
import json
from dotenv import load_dotenv

from core.agents.analyzer.preprocessor_agent import PreprocessorAgent
from core.agents.analyzer.rule_checker_agent import RuleCheckerAgent
from core.agents.analyzer.llm_analyzer_agent import LLMAnalyzerAgent
from core.agents.analyzer.aggregator_agent import AggregatorAgent

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class ResumeAnalysisService:
    """
    A production-grade service to orchestrate the resume analysis workflow.
    """

    def __init__(self):
        load_dotenv()
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            logging.error("CRITICAL: GOOGLE_API_KEY not found in .env file.")
            raise ValueError("Configuration Error: GOOGLE_API_KEY is not set.")

        self.preprocessor = PreprocessorAgent()
        self.rule_checker = RuleCheckerAgent()
        self.llm_analyzer = LLMAnalyzerAgent(api_key)
        self.aggregator = AggregatorAgent()
        logging.info("ResumeAnalysisService initialized successfully.")

    def analyze_resume(self, resume_content: bytes, filename: str, target_job_role: str) -> dict:
        """
        Analyzes a resume provided as byte content. This is the primary entry point.
        """
        logging.info(f"Starting analysis for role: '{target_job_role}' on file: '{filename}'")
        
        # --- KEY CHANGE: Robust and platform-safe temporary file handling ---
        file_extension = os.path.splitext(filename)[1]
        # 1. Create the temporary file but instruct it NOT to delete on close.
        #    We will handle deletion manually in a `finally` block for robustness.
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=file_extension)
        resume_path = temp_file.name

        try:
            # 2. Write content and IMMEDIATELY close the file to release the lock.
            temp_file.write(resume_content)
            temp_file.close() # This is the crucial step that releases the lock.

            # --- Agentic Workflow (Now operates on the closed, accessible file) ---
            logging.info("Step 1/4: Pre-processing and running local checks...")
            resume_text = self.preprocessor.extract_text(resume_path)
            page_count = self.preprocessor.get_page_count(resume_path)
            rule_feedback = self.rule_checker.check_rules(resume_text, page_count)
            logging.info("  - Local processing complete.")

            logging.info("Step 2/4: Generating ideal candidate persona...")
            role_persona_json = self.llm_analyzer.generate_role_persona(target_job_role)
            logging.info("  - Persona generation complete.")

            logging.info("Step 3/4: Performing holistic resume analysis with AI...")
            holistic_eval_json = self.llm_analyzer.analyze_resume_holistically(
                resume_text, role_persona_json
            )
            logging.info("  - Holistic AI analysis complete.")

            logging.info("Step 4/4: Aggregating scores and generating final report...")
            final_report_str = self.aggregator.aggregate_scores(holistic_eval_json, rule_feedback)
            logging.info("Analysis finished successfully.")
            
            return json.loads(final_report_str)

        except Exception as e:
            logging.error(f"An unexpected error occurred during the analysis pipeline: {e}", exc_info=True)
            return {
                "error": "An internal error occurred during the analysis pipeline.",
                "details": str(e)
            }
        finally:
            # 3. GUARANTEE DELETION: This block runs no matter what, ensuring we
            #    don't leave temporary files on the disk if an error occurs.
            if os.path.exists(resume_path):
                os.remove(resume_path)
                logging.info(f"Cleaned up temporary file: {resume_path}")