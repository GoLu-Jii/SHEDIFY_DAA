from fastapi import FastAPI
from typing import List
from datetime import time
from pydantic import BaseModel
import uuid
from fastapi.middleware.cors import CORSMiddleware

from backend.scheduler import schedule_classes
from backend.models import ClassRequest
from backend.classrooms import delete_request, get_mock_requests, get_mock_classrooms, add_request, ACTIVE_SCHEDULES


app = FastAPI(title="Smart Scheduling System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ClassRequestSchema(BaseModel):
    course_name: str
    start_time: str
    end_time: str
    requested_room_type: str
    expected_students: int


@app.get("/classrooms")
def get_classrooms():
    return get_mock_classrooms()


@app.get("/schedules")
def get_schedules():
    return {
        "schedules": list(ACTIVE_SCHEDULES.values())
    }


@app.post("/schedule")
def generate_schedule(requests: List[ClassRequestSchema]):
    
    
    parsed_requests = []
    
    for req in requests:
        new_req = ClassRequest(
            id=f"REQ_{uuid.uuid4().hex[:6].upper()}",
            course_name=req.course_name,
            start_time=time.fromisoformat(req.start_time),
            end_time=time.fromisoformat(req.end_time),
            requested_room_type=req.requested_room_type,
            expected_students=req.expected_students
        )

        add_request(new_req)
        parsed_requests.append(new_req)

    classrooms = get_mock_classrooms()
    schedules = schedule_classes(get_mock_requests(), classrooms)

    for s in schedules:
        ACTIVE_SCHEDULES[s.request_id] = {
            "request_id": s.request_id,
            "classroom_id": s.classroom_id
        }
    
    return {
        "schedules": list(ACTIVE_SCHEDULES.values())
    }
        


@app.delete("/delete/{request_id}")
def delete_class(request_id: str):
    
    delete_request(request_id)

    schedule_list = []


    return {
        "status": "success",
        "message": f"Request {request_id} deleted",
        "schedules": list(ACTIVE_SCHEDULES.values())
    }
