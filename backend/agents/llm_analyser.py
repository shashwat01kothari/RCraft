# core/llm_analyser.py
import os
import google.generativeai as genai
import json
from dotenv import load_dotenv

from ...data_models import ResumeData, AnalysisResult

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class LLMAnalyserAgent:
    """An agent that uses an LLM to score and suggest improvements for a resume."""

    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')

    def analyze(self, resume_data: ResumeData, job_description: str) -> AnalysisResult:
        """
        Scores the resume and provides improvement suggestions.
        """
        resume_json = resume_data.model_dump_json(indent=2)
        
        prompt = f"""
        You are a world-class, brutally honest Applicant Tracking System (ATS) and a senior tech recruiter.
        Your task is to score a candidate's resume against a job description and provide strict, non-overlapping improvement suggestions.

        **Resume Data (JSON):**
        ```json
        {resume_json}
        ```

        **Job Description:**
        ---
        {job_description}
        ---

        **Instructions:**
        1.  **ATS Score:** Act as a strict ATS. Score the resume out of 100 based on keyword matching, skills alignment, and experience relevance. Be brutal; a perfect score should be nearly impossible.
        2.  **Summary:** Briefly summarize the candidate's strengths and weaknesses for this role.
        3.  **Improvement Suggestions:** Provide a list of the top 5 most critical, non-overlapping, and actionable suggestions. For each suggestion, specify the area of the resume it applies to.

        **Output Format (Strict JSON):**
        You MUST respond with a single, valid JSON object that conforms to this schema:
        {{
          "ats_score": integer,
          "summary": "string",
          "improvement_suggestions": [
            {{ "area": "string (e.g., Work Experience, Projects, Skills)", "suggestion": "string" }}
          ]
        }}
        """
        
        try:
            response = self.model.generate_content(prompt)
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
            analysis_json = json.loads(cleaned_response)
            return AnalysisResult(**analysis_json)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error during LLM analysis: {e}")
            raise ValueError("Failed to get a valid analysis from the LLM.")