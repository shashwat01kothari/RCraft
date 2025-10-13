# core/data_models.py
from pydantic import BaseModel, Field
from typing import List, Optional

class Education(BaseModel):
    degree: str
    institution: str
    graduation_year: Optional[str] = None

class WorkExperience(BaseModel):
    title: str
    company: str
    duration: Optional[str] = None
    description: List[str] = Field(default_factory=list)

class Project(BaseModel):
    title: str
    description: List[str] = Field(default_factory=list)

class ResumeData(BaseModel):
    education: List[Education] = Field(default_factory=list)
    work_experience: List[WorkExperience] = Field(default_factory=list)
    projects: List[Project] = Field(default_factory=list)
    technical_skills: List[str] = Field(default_factory=list)
    certifications: List[str] = Field(default_factory=list)

class ImprovementSuggestion(BaseModel):
    area: str  # e.g., "Work Experience", "Skills"
    suggestion: str


#api validation 

class CategoryScores(BaseModel):
    """A dedicated model for the breakdown of scores by category."""
    structure: float = Field(...,  description="Score for layout and formatting.", example=8.5)
    language: float = Field(...,  description="Score for use of action verbs and professional tone.", example=7.0)
    ats: float = Field(...,  description="Score for Applicant Tracking System compatibility.", example=9.0)
    summary: float = Field(...,  description="Score for the power and relevance of the professional summary.", example=8.0)
    experience: float = Field(...,  description="Score for impact, metrics, and STAR method usage.", example=7.5)
    skills: float = Field(..., description="Score for relevance and presentation of skills.", example=8.0)
    relevance: float = Field(...,  description="Score for overall alignment with the target job role.", example=9.0)



class FeedbackDetail(BaseModel):
    """A model to hold the detailed feedback for each category."""
    structure: str = Field(..., description="Feedback related to layout and formatting.", example="Improve section spacing and consistency.")
    language: str = Field(..., description="Feedback on professional tone and use of action verbs.", example="Use more active verbs and concise phrasing.")
    ats: str = Field(..., description="Feedback regarding ATS compatibility.", example="Add relevant keywords from job description.")
    summary: str = Field(..., description="Feedback for the professional summary.", example="Make the summary more impactful and concise.")
    experience: str = Field(..., description="Feedback on experience section.", example="Include measurable outcomes using STAR method.")
    skills: str = Field(..., description="Feedback on skills presentation.", example="List skills relevant to the target job prominently.")
    relevance: str = Field(..., description="Feedback on overall job relevance.", example="Tailor content more towards the target role.")

class FinalHolisticReport(BaseModel):
    """
    This Pydantic model validates the entire JSON structure before sending it to the frontend.
    It now uses dedicated classes for nested objects.
    """
    overall_score: float = Field(..., ge=0, le=100, description="Overall holistic score for the resume.", example=85.5)
    category_scores: CategoryScores = Field(..., description="Detailed breakdown of scores by category.")
    feedback: FeedbackDetail = Field(..., description="Detailed textual feedback for each category.")
    recommendations: List[str] = Field(..., description="List of general recommendations for improving the resume.", example=["Focus on ATS keywords", "Improve summary section"])



# --- NEW MODELS FOR THE OPTIMIZER VERTICAL ---


class ContextOutput(BaseModel):
    """
    The structured output from the Context Extraction Agent. This serves as the
    foundational understanding of the job description for all subsequent agents.
    """
    role: str = Field(description="The specific role being targeted, as extracted from the JD.")
    company: str = Field(description="The name of the target company.")
    skills: List[str] = Field(description="A list of key technical and soft skills extracted from the JD.")
    responsibilities: List[str] = Field(description="A list of core responsibilities mentioned in the JD.")
    tone: str = Field(description="The inferred tone of the company/role (e.g., 'technical and innovative', 'formal and corporate').")
    experience_level: str = Field(description="The inferred seniority level (e.g., 'mid-senior', 'entry-level', 'lead').")
    boolean_search_string: str = Field(description="A recruiter-style boolean search string to find candidates for this role.")


class ResearchOutput(BaseModel):
    """
    Structured output from the Research & Insight Agent. This captures the
    company's cultural DNA and communication style from external sources.
    """
    company_style: str = Field(description="The company's communication style (e.g., 'formal yet visionary', 'playful and direct').")
    mission_focus: List[str] = Field(description="A list of key themes from the company's mission or values (e.g., 'AI ethics', 'democratizing data').")
    key_phrases: List[str] = Field(description="A list of specific, recurring phrases or keywords found in the research to potentially include in the resume.")

class StrategyOutput(BaseModel):
    """
    Structured output from the Resume Strategist Agent. This serves as the
    architectural blueprint for the resume, guiding the Builder agent.
    """
    sections: List[str] = Field(description="The list of section titles to be included in the final resume.")
    priority_order: List[str] = Field(description="The recommended order of the top 3-4 most impactful sections.")
    guidelines: List[str] = Field(description="A list of high-level, strategic instructions for the writer agent to follow.")
    tone_of_voice: str = Field(description="A concise directive on the tone and style the resume should adopt.")



class FinalResumeSections(BaseModel):
    """A structured representation of the final resume's content, ready for rendering."""
    summary: str = Field(description="The professional summary section.")
    experience: str = Field(description="The work experience section, formatted as a single string.")
    projects: str = Field(description="The projects section, formatted as a single string.")
    skills: str = Field(description="The skills section, formatted as a single string.")
    education: Optional[str] = Field(None, description="The education section, if present.")

class ReviewerOutput(BaseModel):
    """The structured output from the Final Reviewer Agent."""
    final_resume: FinalResumeSections
    format: str = Field(default="docx", description="The desired output file format.")
    readability_score: float = Field(..., ge=0.0, le=1.0, description="A score from 0.0 to 1.0 indicating ease of reading.")



class OptimizerWorkflowState(BaseModel):
    """
    The central, evolving state object that will be passed through the LangGraph workflow.
    Each agent will read from and write to this single object.
    """
    # --- Initial Inputs ---
    job_description: str
    job_role: str
    company_name: str

    # --- Agent Outputs (populated sequentially) ---
    context: Optional[ContextOutput] = None
    research: Optional[ResearchOutput] = None
    strategy: Optional[StrategyOutput] = None
    draft_resume_text: Optional[str] = Field(None, description="The first full draft of the resume, formatted as a single Markdown string.")
    optimized_resume_text: Optional[str] = Field(None, description="The refined resume draft, optimized for ATS keyword and semantic alignment.")
    final_report: Optional[ReviewerOutput] = None



class WorkflowRunResponse(BaseModel):
    """
    The response sent after the initial workflow is complete. It provides a unique
    ID for the results and the data needed for a frontend preview.
    """
    workflow_id: str = Field(description="The unique ID for this workflow run, used to download the final asset.")
    resume_data: FinalResumeSections = Field(description="The structured resume content for preview.")