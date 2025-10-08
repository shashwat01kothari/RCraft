# main.py
from fastapi import FastAPI
import uvicorn

from backend.core.apis.analysis_router import router as  analysis_router

app = FastAPI(
    title="Career Co-Pilot API",
    description="An AI-powered service to generate a holistic analysis of resumes.",
    version="2.0.0"
)

# Include the router that contains our /analyze endpoint
app.include_router(analysis_router, prefix="/api", tags=["Analysis"])

@app.get("/", tags=["Root"])
async def read_root():
    """A simple health check endpoint."""
    return {"message": "Career Co-Pilot API is running."}

# This allows running the server directly using `python main.py`
if __name__ == "__main__":
     uvicorn.run(
        "backend.main:app", 
        host="127.0.0.0", 
        port=8000, 
        reload=True,
        reload_dirs=["backend"] 
    )