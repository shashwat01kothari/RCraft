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

class OptimizerWorkflowState(BaseModel):
    """
    The central, evolving state object that will be passed through the LangGraph workflow.
    Each agent will read from and write to this single object.
    """
    # --- Initial Inputs ---
    job_description: str
    job_role: str
    company_name: str