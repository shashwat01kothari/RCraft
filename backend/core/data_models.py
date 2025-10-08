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
