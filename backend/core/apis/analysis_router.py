# api/analysis_router.py
from fastapi import APIRouter, UploadFile, File, Form, HTTPException , Depends
from backend.core.services.resume_analysis_service import ResumeAnalysisService
from backend.core.data_models import FinalHolisticReport
import tempfile
import os


router = APIRouter()

# --- NEW: Dependency Injection Factory ---
# This function is a "provider". FastAPI will call this for us.
# It creates a new instance of our service for each request that needs it.
# This is a clean, stateless approach.
def get_resume_service():
    """Provides a ResumeProcessingService instance."""
    return ResumeAnalysisService()

@router.post("/analyze", response_model=FinalHolisticReport)
async def analyze_resume(
    # The file and form data remain the same
    file: UploadFile = File(..., description="The user's resume file (PDF or DOCX)."),
    job_role: str = Form(..., description="The job role the user is targeting."),
    
    # --- UPDATED: FastAPI will now inject the service instance for us ---
    # It calls get_resume_service() and the result is passed to this parameter.
    service: ResumeAnalysisService = Depends(get_resume_service)
):
    """
    Accepts a resume file and a target job role, processes them,
    and returns the final_holistic_report for the frontend.
    """
    tmp_path = None
    try:
        # with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
        #     tmp.write(await file.read())
        #     tmp_path = tmp.name
        
        # # We now use the 'service' instance that FastAPI provided.
        # final_report = service.analyze_resume(tmp_path, target_job_role=job_role)
        resume_bytes = await file.read()
        filename = file.filename

        # Call the class method
        final_report = service.analyze_resume(
            resume_content=resume_bytes,
            filename=filename,
            target_job_role=job_role
        )

        # If your method returns a dict compatible with FinalHolisticReport
        
        return final_report

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"An unexpected error occurred in the API: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred.")
    finally:
        if tmp_path and os.path.exists(tmp_path):
            os.unlink(tmp_path)