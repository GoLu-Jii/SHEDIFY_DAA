from datetime import time
from .models import Classroom, ClassRequest

CLASSROOMS = [
    # Block A
    Classroom(id="A101", capacity=60, room_type="lecture"),
    Classroom(id="A102", capacity=80, room_type="lecture"),
    Classroom(id="A103", capacity=100, room_type="lecture"),
    Classroom(id="A201", capacity=60, room_type="lecture"),
    Classroom(id="A202", capacity=80, room_type="lecture"),
    Classroom(id="A203", capacity=100, room_type="lecture"),
    Classroom(id="A_CS_LAB-01", capacity=30, room_type="lab"),
    Classroom(id="A_CS_LAB-02", capacity=40, room_type="lab"),
    Classroom(id="A_CS_LAB-03", capacity=50, room_type="lab"),
    
    # Block B
    Classroom(id="B101", capacity=60, room_type="lecture"),
    Classroom(id="B102", capacity=80, room_type="lecture"),
    Classroom(id="B103", capacity=100, room_type="lecture"),
    Classroom(id="B201", capacity=60, room_type="lecture"),
    Classroom(id="B202", capacity=80, room_type="lecture"),
    Classroom(id="B203", capacity=100, room_type="lecture"),
    Classroom(id="B_CS_LAB-01", capacity=30, room_type="lab"),
    Classroom(id="B_CS_LAB-02", capacity=40, room_type="lab"),
    Classroom(id="B_CS_LAB-03", capacity=50, room_type="lab"),
    
    # Block C
    Classroom(id="C101", capacity=60, room_type="lecture"),
    Classroom(id="C102", capacity=80, room_type="lecture"),
    Classroom(id="C103", capacity=100, room_type="lecture"),
    Classroom(id="C201", capacity=60, room_type="lecture"),
    Classroom(id="C202", capacity=80, room_type="lecture"),
    Classroom(id="C203", capacity=100, room_type="lecture"),
    Classroom(id="C_CS_LAB-01", capacity=30, room_type="lab"),
    Classroom(id="C_CS_LAB-02", capacity=40, room_type="lab"),
    Classroom(id="C_CS_LAB-03", capacity=50, room_type="lab"),
    
    # Block D
    Classroom(id="D101", capacity=60, room_type="lecture"),
    Classroom(id="D102", capacity=80, room_type="lecture"),
    Classroom(id="D103", capacity=100, room_type="lecture"),
    Classroom(id="D201", capacity=60, room_type="lecture"),
    Classroom(id="D202", capacity=80, room_type="lecture"),
    Classroom(id="D203", capacity=100, room_type="lecture"),
    Classroom(id="D_CS_LAB-01", capacity=30, room_type="lab"),
    Classroom(id="D_CS_LAB-02", capacity=40, room_type="lab"),
    Classroom(id="D_CS_LAB-03", capacity=50, room_type="lab"),
    
    # Block E
    Classroom(id="E101", capacity=60, room_type="lecture"),
    Classroom(id="E102", capacity=80, room_type="lecture"),
    Classroom(id="E103", capacity=100, room_type="lecture"),
    Classroom(id="E201", capacity=60, room_type="lecture"),
    Classroom(id="E202", capacity=80, room_type="lecture"),
    Classroom(id="E203", capacity=100, room_type="lecture"),
    Classroom(id="E_CS_LAB-01", capacity=30, room_type="lab"),
    Classroom(id="E_CS_LAB-02", capacity=40, room_type="lab"),
    Classroom(id="E_CS_LAB-03", capacity=50, room_type="lab"),
]

REQUESTS = {}
ACTIVE_SCHEDULES = {} 

def get_mock_classrooms():
    return CLASSROOMS

def get_mock_requests():
    return list(REQUESTS.values())

def add_request(req: ClassRequest):
    REQUESTS[req.id] = req
    
def delete_request(request_id: str):

    REQUESTS.pop(request_id, None)
    ACTIVE_SCHEDULES.pop(request_id, None)
