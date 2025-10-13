# llm_analyzer_agent.py

import os
import re
import json
import time
import google.generativeai as genai
from google.api_core import exceptions

class LLMAnalyzerAgent:
    """The core AI agent using Gemini for holistic, multi-category resume analysis."""

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    def _get_llm_response(self, prompt: str) -> str:
        """Sends a prompt to the LLM with robust error handling and retries."""
        max_retries = 3
        delay = 5
        for attempt in range(max_retries):
            try:
                generation_config = genai.types.GenerationConfig(response_mime_type="application/json")
                response = self.model.generate_content(prompt, generation_config=generation_config)
                return response.text
            except exceptions.ResourceExhausted as e:
                print(f"    - Rate limit exceeded. Waiting for {delay}s. (Attempt {attempt + 1}/{max_retries})")
                time.sleep(delay)
                delay *= 2
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                return f'{{"error": "An unexpected API error occurred: {str(e)}"}}'
        print("All retries failed. Could not get a response from the LLM.")
        return f'{{"error": "API rate limit was exceeded and all retries failed."}}'

    def generate_role_persona(self, target_job_role: str) -> str:
        """Creates a profile of an ideal candidate. This remains a separate, initial call."""
        print(f"  - Generating ideal candidate persona for: {target_job_role}...")
        prompt = f"""
            You are an expert recruiter. Create an "ideal candidate persona" for the job role: '{target_job_role}'.
            Your output MUST be a valid JSON object with three keys: "hard_skills" (list of strings),
            "soft_skills" (list of strings), and "key_responsibilities" (list of strings).
        """
        return self._get_llm_response(prompt)

    def analyze_resume_holistically(self, resume_text: str, role_persona_json: str) -> str:
        """Performs all 7 analyses in a single API call."""
        try:
            persona = json.loads(role_persona_json)
        except json.JSONDecodeError:
            persona = {} # Handle case where persona generation fails

        prompt = f"""
            You are an expert AI Resume Coach. Your task is to analyze a resume against the ideal persona for a target role.
            Perform a comprehensive analysis covering all 7 categories below.

            **Resume Text:**
            ---
            {resume_text}
            ---

            **Ideal Candidate Persona:**
            ---
            {json.dumps(persona, indent=2)}
            ---

            Your final output MUST be a single, valid JSON object with a key for each of the 7 categories. Assume that the current year is 2025 .
            Each category key must contain a nested JSON object with an integer "score" (from 1 to 10) and a brief "feedback" string.

            Follow these rules for each category:

            1.  **"structure"**: Analyze layout, page count, headings, and grammar.
            2.  **"language"**: Analyze use of strong action verbs, consistent tense, and avoidance of first-person pronouns.
            3.  **"ats"**: Analyze for standard headings, parsable format, and plain text contact info.
            4.  **"summary"**: Analyze alignment with the target role and key skills mentioned in the persona.
            5.  **"experience"**: Analyze for quantified impact (%, $, #) and action-oriented descriptions.
            6.  **"skills"**: Analyze how well the resume's skills match the persona's "hard_skills".
            7.  **"relevance"**: Analyze how well the overall experience aligns with the persona's "key_responsibilities".

            Provide specific, actionable feedback for each category.
        """
        return self._get_llm_response(prompt)



