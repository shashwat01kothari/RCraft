import os
import google.generativeai as genai
import json
from dotenv import load_dotenv
import pprint

from ..data_models import ResumeData


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

class LLMStructuringAgent:
    """An agent dedicated to converting raw text into a structured ResumeData object."""

    def __init__(self):
        self.model = genai.GenerativeModel('gemini-2.5-pro')

    def structure_resume_text(self, raw_text: str) -> ResumeData:
        """Uses an LLM to parse raw text and return a ResumeData object."""
        prompt = f"""
        You are an expert resume parsing system. Your task is to analyze the following resume text and extract the key information into a structured JSON format. The JSON object must conform to the specified schema.

        Schema:
        {{
          "education": [{{ "degree": "string", "institution": "string", "graduation_year": "string" }}],
          "work_experience": [{{ "title": "string", "company": "string", "duration": "string", "description": "list[string]" }}],
          "projects": [{{ "title": "string", "description": "list[string]" }}],
          "technical_skills": "list[string]",
          "certifications": "list[string]"
        }}
        
        Rules:
        - If a section is not found, return an empty list for it.
        - `description` fields should be a list of strings, where each string is a bullet point.
        
        Resume Text:
        ---
        {raw_text}
        ---
        
        Now, provide the structured JSON output.
        """
        
        try:
            response = self.model.generate_content(prompt)
            cleaned_response = response.text.strip().replace("```json", "").replace("```", "")
            structured_json = json.loads(cleaned_response)
            return ResumeData(**structured_json)
        except (json.JSONDecodeError, Exception) as e:
            print(f"Error structuring text with LLM: {e}")
            raise ValueError("Failed to get a valid structured response from the LLM for parsing.")
        


### self testing / simulation component
if __name__ == "__main__":
    
    # 1. Define a sample raw text, as if it were extracted from a resume
    SAMPLE_RESUME_TEXT = """
    **John Doe**
    john.doe@email.com | (123) 456-7890 | linkedin.com/in/johndoe | github.com/johndoe

    Highly motivated Software Engineer with a proven track record of developing scalable web applications. My expertise lies in Python and cloud infrastructure, particularly AWS. Seeking a challenging role to apply my skills in a collaborative environment.

    *** Core Competencies ***
    - Languages & Databases: Proficient in Python, JavaScript, and SQL (PostgreSQL, MongoDB).
    - Development Tools: Docker, Git
    - Frameworks: Experienced with Flask and React.

    *** Projects ***
    My main project is an AI Resume Analyzer. I built the entire backend service to parse and score documents using Google's Gemini API. The frontend was built with Streamlit for rapid prototyping. This project showcases my skills in both backend development and API integration.

    *** Professional History ***
    Software Engineer at Tech Solutions Inc. (June 2020 - Present)
    In my current role, I was instrumental in developing and maintaining several REST APIs, primarily using Python and Flask. This work led to a significant improvement in our application's performance. I also regularly collaborated in an agile team of 5 engineers on our main customer-facing web application.

    *** Academic Record ***
    I graduated from the University of Technology, located in Major City, with a Bachelor of Science in Computer Science in May 2020.

    *** Certs ***
    I am an AWS Certified Cloud Practitioner, certification obtained in 2021.
    
    """

    print("--- Testing LLMStructuringAgent ---")
    
    # 2. Instantiate the agent
    structuring_agent = LLMStructuringAgent()
    
    print("\nSample Raw Text to be Processed:")
    print("---------------------------------")
    print(SAMPLE_RESUME_TEXT)
    print("---------------------------------\n")

    try:
        # 3. Call the method with the sample text
        print("Calling the structuring agent... (This may take a moment)")
        structured_data = structuring_agent.structure_resume_text(SAMPLE_RESUME_TEXT)
        
        print("--- SUCCESS: LLM Structuring Complete ---")
        print("Type of result:", type(structured_data))
        print("\nStructured Data Output:")
        # Use pprint to nicely format the Pydantic model's dictionary representation
        pprint.pprint(structured_data.model_dump())

    except ValueError as e:
        print(f"\n--- ERROR ---")
        print(e)
    except Exception as e:
        print(f"\n--- AN UNEXPECTED ERROR OCCURRED ---")
        print(e)