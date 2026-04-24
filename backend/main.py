from fastapi import FastAPI
from typing import List
from datetime import time
from pydantic import BaseModel
import uuid

from backend.scheduler import schedule_classes
from backend.models import ClassRequest
from backend.classrooms import delete_request, get_mock_requests, get_mock_classrooms


app = FastAPI(title="Smart Scheduling System")

class ClassRequestSchema(BaseModel):
    course_name: str
    start_time: str
    end_time: str
    class_type: str = "lecture"
    requested_room_type: str
    expected_students: int


@app.get("/")
def root():
    return {"message": "Scheduler API running"}


@app.get("/classrooms")
def get_classrooms():
    return get_mock_classrooms()


@app.post("/schedule")
def generate_schedule(requests: List[ClassRequestSchema]):
    
    # convert incoming JSON → ClassRequest objects
    parsed_requests = []
    
    for req in requests:
        parsed_requests.append(
            ClassRequest(
                id=f"REQ_{uuid.uuid4().hex[:6].upper()}",
                course_name=req.course_name,
                start_time=time.fromisoformat(req.start_time),
                end_time=time.fromisoformat(req.end_time),
                class_type=req.class_type,
                requested_room_type=req.requested_room_type,
                expected_students=req.expected_students
            )
        )

    classrooms = get_mock_classrooms()

    schedules, recommendations = schedule_classes(parsed_requests, classrooms)

    return {
        "schedules": [
            {
                "request_id": s.request_id,
                "classroom_id": s.classroom_id
            }
            for s in schedules
        ],
        "recommendations": recommendations
    }


@app.delete("/delete/{request_id}")
def delete_class(request_id: str):
    
    delete_request(request_id)

    # recompute updated schedule
    schedules, recommendations = schedule_classes(
        get_mock_requests(),
        get_mock_classrooms()
    )

    return {
        "status": "success",
        "message": f"Request {request_id} deleted",
        "schedules": [
            {
                "request_id": s.request_id,
                "classroom_id": s.classroom_id
            }
            for s in schedules
        ],
        "recommendations": recommendations
    }