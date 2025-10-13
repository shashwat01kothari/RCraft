import os
from fastapi import APIRouter, Form, HTTPException, Depends
from fastapi.responses import FileResponse
from backend.core.services.resume_optimizer_service import ResumeOptimizerService
from backend.core.data_models import OptimizerWorkflowState, WorkflowRunResponse
from backend.core.tools.pdf_renderer import PdfRenderer
from backend.core.tools.workflow_state_manager import WorkflowStateManager

router = APIRouter()

def get_optimizer_service():
    """Dependency injector for the optimizer service."""
    # This now correctly instantiates our LangGraph-powered service.
    return ResumeOptimizerService()

def get_state_manager() -> WorkflowStateManager:
    """Provides a WorkflowStateManager instance to manage Redis connections."""
    return WorkflowStateManager()


# --- API ENDPOINT 1: RUN THE WORKFLOW ---

@router.post("/optimizer/run", response_model=WorkflowRunResponse)
async def run_optimizer_workflow(
    job_description: str = Form(..., description="The full text of the job description."),
    job_role: str = Form(..., description="The job role the user is targeting (e.g., 'Software Engineer')."),
    company_name: str = Form(..., description="The name of the target company."),
    service: ResumeOptimizerService = Depends(get_optimizer_service),
    state_manager: WorkflowStateManager = Depends(get_state_manager)
):
    """
    Kicks off the long-running, multi-agent LangGraph workflow to generate resume content.

    This endpoint is asynchronous from the user's perspective. It performs the
    heavy lifting and, upon completion, saves the result to a temporary state
    store (Redis) and returns a unique ID for that result.
    """
    print("--- API: Kicking off optimizer workflow run ---")
    try:
        # --- THE FIX IS HERE ---
        # 1. The service now directly returns the final report, not the entire state.
        #    We rename the variable for clarity.
        final_report = service.optimize_resume(jd=job_description, role=job_role, company=company_name)

        # 2. Accessing the resume data is now simpler and more direct.
        resume_data = final_report.final_resume
        
        # 3. Save the final data to Redis and get a unique ID.
        workflow_id = state_manager.save_state(resume_data)
        
        # 4. Return the successful response, including the ID and the data for preview.
        return WorkflowRunResponse(
            workflow_id=workflow_id,
            resume_data=resume_data
        )
        
    except ConnectionError as e:
        # Handle specific case where Redis is down
        print(f"ERROR: Could not connect to state manager (Redis): {e}")
        raise HTTPException(status_code=503, detail=f"State service unavailable: {e}")
    except ValueError as e:
        # Handle cases where the service raises a value error (e.g., workflow fails)
        print(f"ERROR: A validation error occurred during the workflow: {e}")
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        # Handle any other unexpected errors during the workflow
        print(f"An unexpected error occurred during workflow run: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred during the workflow.")


# --- API ENDPOINT 2: DOWNLOAD THE PDF ---

@router.get("/optimizer/download-pdf/{workflow_id}")
async def download_resume_pdf(
    workflow_id: str,
    state_manager: WorkflowStateManager = Depends(get_state_manager)
):
    """
    Retrieves the result of a completed workflow using its unique ID and returns
    the generated resume as a professionally typeset, downloadable PDF file.
    """
    print(f"--- API: Received request to download PDF for ID: {workflow_id} ---")
    
    renderer = PdfRenderer()
    file_path = None
    try:
        # 1. Load the resume data from Redis using the provided ID.
        resume_data = state_manager.load_state(workflow_id)
        
        # 2. Delegate the rendering task to the dedicated PdfRenderer tool.
        file_path = renderer.render_to_pdf(resume_data)
        
        # 3. Return the generated file as a downloadable response.
        return FileResponse(
            path=file_path,
            media_type='application/pdf',
            # Provide a user-friendly filename for the download.
            filename=f"Optimized_Resume_{workflow_id[:8]}.pdf"
        )
        
    except FileNotFoundError as e:
        # This error is raised by the state manager if the ID is invalid or expired.
        raise HTTPException(status_code=404, detail=str(e))
    except ConnectionError as e:
        # Handle specific case where Redis is down
        raise HTTPException(status_code=503, detail=f"State service unavailable: {e}")
    except Exception as e:
        # Handle errors during the PDF rendering process
        print(f"An unexpected error occurred during PDF generation: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred during PDF generation.")
    finally:
        if file_path and os.path.exists(file_path):
            os.remove(file_path)
            print(f"--- API: Cleaned up temporary PDF file: {file_path} ---")