
import os
import re
import json
import google.generativeai as genai

class LLMEvaluatorAgent:
    """The core AI agent using Gemini for semantic resume analysis."""

    def __init__(self, api_key: str):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-2.5-pro') # Using gemini-pro for speed/cost balance

    def _get_llm_response(self, prompt: str) -> str:
        """Sends a prompt to the LLM and returns the cleaned JSON response."""
        try:
            response = self.model.generate_content(prompt)
            # The API response may contain markdown backticks and 'json' specifier
            clean_response = re.sub(r'```json\n|\n```', '', response.text).strip()
            return clean_response
        except Exception as e:
            print(f"Error communicating with LLM: {e}")
            return f'{{"error": "Failed to get response from LLM: {str(e)}"}}'

    def generate_role_persona(self, target_job_role: str) -> str:
        """Creates a profile of an ideal candidate for a given role."""
        print(f"Generating ideal persona for: {target_job_role}...")
        prompt = f"""
            As an expert recruiter, create an "ideal candidate persona" for the job role: '{target_job_role}'.
            Your output MUST be a JSON object with three keys: "hard_skills" (a list of strings),
            "soft_skills" (a list of strings), and "key_responsibilities" (a list of strings).
        """
        return self._get_llm_response(prompt)

    def analyze_category(self, category: str, resume_text: str, role_persona_json: str = "") -> str:
        """Analyzes a specific resume category against the generated persona."""
        try:
            persona = json.loads(role_persona_json) if role_persona_json else {}
        except json.JSONDecodeError:
            persona = {}

        prompts = {
            "summary": f"""
                Analyze the 'Professional Summary' of this resume. The candidate is targeting a role like '{persona.get('role', 'the target role')}'.
                Rules: Must clearly state professional identity and align with the target role, highlighting 1-2 key skills. Avoid clichés.
                Resume Summary: "{resume_text}"
                Provide your analysis as a JSON object with an integer "score" (1-10) and a brief "feedback" string.
            """,
            "skills": f"""
                Analyze the 'Skills' section. The ideal hard skills for this role are: {persona.get('hard_skills', 'N/A')}.
                Rules: Score high if resume skills match the ideal skills. Score lower if key skills are missing. Check for skill stuffing.
                Resume Skills Section: "{resume_text}"
                Provide your analysis as a JSON object with an integer "score" (1-10) and a brief "feedback" string.
            """,
            "relevance": f"""
                Analyze the overall resume's relevance for a role with these responsibilities: {persona.get('key_responsibilities', 'N/A')}.
                Rules: Score how well the candidate's described experience proves they can perform these duties.
                Full Resume Text: "{resume_text}"
                Provide your analysis as a JSON object with an integer "score" (1-10) and a brief "feedback" justification.
            """,
            "experience": f"""
                Analyze the 'Experience & Impact' of this resume.
                Rules: Bullets should start with strong action verbs. Must include quantified results (numbers, percentages). Focus on impact, not just duties.
                Resume Text: "{resume_text}"
                Provide your analysis as a JSON object with an integer "score" (1-10) and "feedback" string with specific examples.
            """
        }

        prompt = prompts.get(category)
        if not prompt:
            return '{"score": 0, "feedback": "Category not found."}'
        return self._get_llm_response(prompt)