
import os
import re
import json
import google.generativeai as genai

class LLMAnalyzerAgent:
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
        """Analyzes a specific resume category. All prompts expect a JSON response."""
        try:
            persona = json.loads(role_persona_json) if role_persona_json else {}
        except json.JSONDecodeError:
            persona = {}
        
        target_role = persona.get('role_title', 'the target role')
        ideal_skills = persona.get('hard_skills', 'N/A')
        ideal_responsibilities = persona.get('key_responsibilities', 'N/A')

        # Comprehensive prompts for all categories
        prompts = {
            "structure": f"""
                Analyze the 'Structure & Readability' of this resume.
                Rules:
                - Resume should ideally fit on 1 page, 2 pages maximum.
                - No dense text blocks (more than 4-5 lines per paragraph).
                - Consistent spacing and clean alignment.
                - Clear section headings are used (Experience, Education, Skills, etc.).
                - Check for major spelling or grammatical errors.
                
                Full Resume Text: "{resume_text}"
                
                Provide your analysis as a JSON object with an integer "score" (1-10) and a brief "feedback" string.
            """,
            "language": f"""
                Analyze the 'Language & Tone' of this resume.
                Rules:
                - No first-person language ("I," "my").
                - Bullets should start with strong, impactful action verbs (e.g., "Orchestrated," "Engineered," "Maximized").
                - Avoid weak/passive verbs ("Worked on," "Helped with," "Responsible for").
                - Consistent verb tense (past tense for past roles, present for current).
                
                Full Resume Text: "{resume_text}"
                
                Provide your analysis as a JSON object with an integer "score" (1-10) and "feedback" string with specific examples.
            """,
            "ats": f"""
                Analyze the 'ATS Compatibility' of this resume's text content.
                Rules:
                - Uses standard, recognizable section headings (e.g., "Experience," not "My Journey").
                - Avoids special characters or symbols that might confuse a parser.
                - Contact info (email, phone) should be present in plain text.
                - The text flow does not suggest the use of complex tables, columns, or graphics that would be hard to parse.
                
                Full Resume Text: "{resume_text}"
                
                Provide your analysis as a JSON object with an integer "score" (1-10) and a brief "feedback" string explaining potential issues.
            """,
            "summary": f"""
                Analyze the 'Professional Summary'. The candidate targets a '{target_role}' role.
                Rules: Must align with the target role, highlighting 1-2 key skills. Avoid clichés.
                Resume Summary: "{resume_text}"
                Provide your analysis as a JSON object with an integer "score" (1-10) and a brief "feedback" string.
            """,
            "experience": f"""
                Analyze the 'Experience & Impact' of this resume.
                Rules: Bullets must start with action verbs. Score higher for quantified results (%, $, #). Focus on impact, not duties.
                Resume Experience Section: "{resume_text}"
                Provide your analysis as a JSON object with an integer "score" (1-10) and "feedback" with specific examples.
            """,
            "skills": f"""
                Analyze the 'Skills' section against the ideal skills for the role: {ideal_skills}.
                Rules: Score high if resume skills match ideal skills. Score lower if key skills are missing. Check for skill stuffing.
                Resume Skills Section: "{resume_text}"
                Provide your analysis as a JSON object with an integer "score" (1-10) and a brief "feedback" string.
            """,
            "relevance": f"""
                Analyze the resume's overall relevance for a role with these responsibilities: {ideal_responsibilities}.
                Rules: Score how well the candidate's experience proves they can perform these duties.
                Full Resume Text: "{resume_text}"
                Provide your analysis as a JSON object with an integer "score" (1-10) and a brief "feedback" justification.
            """
        }

        prompt = prompts.get(category)
        if not prompt:
            return '{"score": 0, "feedback": "Category not found."}'
        return self._get_llm_response(prompt)