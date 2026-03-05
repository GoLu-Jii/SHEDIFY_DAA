"""FastAPI server for Shedify scheduling system."""

import sys
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional
from backend.main import schedule_classes

app = FastAPI(
    title="Shedify API",
    description="Automated Class Scheduling System API",
    version="1.0.0"
)

# Enable CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify actual origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response Models
class ClassRequestModel(BaseModel):
    """Class request model for API."""
    class_id: str = Field(..., description="Unique class identifier")
    class_name: str = Field(..., description="Name of the class")
    start_time: str = Field(..., description="Start time in HH:MM format (24-hour)")
    end_time: str = Field(..., description="End time in HH:MM format (24-hour)")
    room_type: str = Field(..., description="Room type: regular, lab, seminar_hall, or any")
    day: str = Field(..., description="Day of the week")
    instructor: Optional[str] = Field(None, description="Instructor name")
    course_code: Optional[str] = Field(None, description="Course code")

    class Config:
        json_schema_extra = {
            "example": {
                "class_id": "CS101-1",
                "class_name": "Data Structures",
                "start_time": "09:00",
                "end_time": "10:30",
                "room_type": "regular",
                "day": "Monday",
                "instructor": "Dr. Smith",
                "course_code": "CS101"
            }
        }


class ScheduleRequest(BaseModel):
    """Request model for scheduling endpoint."""
    class_requests: List[ClassRequestModel] = Field(..., description="List of class requests to schedule")


@app.post("/api/schedule", response_model=dict)
async def schedule_endpoint(request: ScheduleRequest):
    """
    Schedule classes using the greedy algorithm.
    
    Returns:
        Dictionary containing:
        - schedule: List of scheduled classes with room assignments
        - unscheduled: List of classes that couldn't be scheduled
        - conflicts: List of detected conflicts
        - statistics: Scheduling statistics
    """
    try:
        # Convert Pydantic models to dictionaries
        # Compatible with both Pydantic v1 and v2
        try:
            class_requests_data = [req.model_dump() for req in request.class_requests]
        except AttributeError:
            # Fallback for Pydantic v1
            class_requests_data = [req.dict() for req in request.class_requests]
        
        # Schedule classes
        result = schedule_classes(class_requests_data)
        
        return result
        
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")


@app.get("/api/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "Shedify Scheduling System",
        "version": "1.0.0"
    }


@app.get("/")
async def root():
    """Root endpoint with API information."""
    return {
        "message": "Welcome to Shedify API",
        "docs": "/docs",
        "health": "/api/health",
        "schedule": "/api/schedule"
    }


if __name__ == "__main__":
    import uvicorn
    print("Starting Shedify API server on http://localhost:8000")
    print("API Documentation available at http://localhost:8000/docs")
    print("API endpoints:")
    print("  POST /api/schedule - Schedule classes")
    print("  GET  /api/health   - Health check")
    print("  GET  /docs         - Interactive API documentation")
    uvicorn.run("backend.api_server:app", host="0.0.0.0", port=8000, reload=True)
