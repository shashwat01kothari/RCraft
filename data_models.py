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

class AnalysisResult(BaseModel):
    ats_score: int = Field(..., ge=0, le=100)
    summary: str
    improvement_suggestions: List[ImprovementSuggestion]