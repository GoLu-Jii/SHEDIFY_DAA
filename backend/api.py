from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from backend.database import get_mock_classrooms, get_mock_requests, add_request
from backend.scheduler import schedule_classes, is_overlapping
from backend.models import ClassRequest
from pydantic import BaseModel
from datetime import datetime
import uuid

app = FastAPI(title="SHEDIFY API")

# Add CORS to allow frontend to fetch data from different origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BookingRequest(BaseModel):
    room_id: str
    course_name: str
    start_time: str
    end_time: str
    expected_students: int

@app.get("/api/schedule")
def get_schedule():
    classrooms = get_mock_classrooms()
    requests = get_mock_requests()
    
    schedules = schedule_classes(requests, classrooms)
    
    result = []
    schedules_by_room = {}
    for s in schedules:
        schedules_by_room.setdefault(s.classroom_id, []).append(s)
        
    for room in classrooms:
        room_data = {
            "id": room.id,
            "type": room.room_type,
            "capacity": room.capacity,
            "classes": []
        }
        
        if room.id in schedules_by_room:
            for sched in schedules_by_room[room.id]:
                req = next(r for r in requests if r.id == sched.request_id)
                room_data["classes"].append({
                    "id": req.id,
                    "course_name": req.course_name,
                    "class_type": req.class_type,
                    "expected_students": req.expected_students,
                    "start_time": req.start_time.strftime('%H:%M'),
                    "end_time": req.end_time.strftime('%H:%M')
                })
        
        # Sort classes chronologically
        room_data["classes"].sort(key=lambda x: x["start_time"])
        result.append(room_data)
        
    return {"status": "success", "data": result}

@app.get("/api/rooms")
def get_rooms():
    return {"status": "success", "data": get_mock_classrooms()}

@app.post("/api/book")
def book_room(booking: BookingRequest):
    try:
        t_start = datetime.strptime(booking.start_time, "%H:%M").time()
        t_end = datetime.strptime(booking.end_time, "%H:%M").time()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid time format. Use HH:MM")
        
    if t_start >= t_end:
        raise HTTPException(status_code=400, detail="Start time must be before end time")
        
    classrooms = get_mock_classrooms()
    room = next((r for r in classrooms if r.id == booking.room_id), None)
    if not room:
        raise HTTPException(status_code=404, detail="Room not found")
        
    if booking.expected_students > room.capacity:
        raise HTTPException(status_code=400, detail=f"Room capacity ({room.capacity}) exceeded")

    requests = get_mock_requests()
    # Find requests that are mapped to this room after a schedule run
    # Wait, schedule run happens dynamically. If we hardcode the new request to this room,
    # what happens to the other dynamic schedules?
    # To fix a request to a room, we can just ensure its requested_room_type is the target room ID,
    # and in scheduler, if requested_room_type matches room.id exactly, we greedily assign it.
    # Currently scheduler groups by room_type (e.g. 'lecture'). If requested_room_type == ID, it might fail.
    # Let's adjust scheduler logic or just add a manual check here:
    
    # We will simulate a schedule run including this new hypothetical request.
    new_req = ClassRequest(
        id=f"BOOK_{uuid.uuid4().hex[:6].upper()}",
        course_name=booking.course_name,
        start_time=t_start,
        end_time=t_end,
        class_type="manual",
        requested_room_type=room.id, # Hijacking this field for specific room requirement
        expected_students=booking.expected_students
    )
    
    # Verify explicitly that the new request does not overlap with ANY currently assigned class in this room
    current_schedules = schedule_classes(requests, classrooms)
    for sched in current_schedules:
        if sched.classroom_id == room.id:
            existing_req = next((r for r in requests if r.id == sched.request_id), None)
            if existing_req and is_overlapping(existing_req, new_req):
                raise HTTPException(status_code=409, detail="Time overlap conflict: Room is already booked for this time.")
        
    # If successful, permanently add it
    add_request(new_req)
    
    return {"status": "success", "message": "Room booked successfully!", "booking_id": new_req.id}
