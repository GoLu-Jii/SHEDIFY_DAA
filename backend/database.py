from datetime import time
from .models import Classroom, ClassRequest

CLASSROOMS = [
    Classroom(id="Room101", capacity=60, room_type="lecture"),
    Classroom(id="Room102", capacity=100, room_type="lecture"),
    Classroom(id="Room103", capacity=150, room_type="lecture"),
    Classroom(id="Room104", capacity=30, room_type="lab"),
    Classroom(id="Room105", capacity=40, room_type="lab"),
    Classroom(id="Room106", capacity=50, room_type="lab"),
]

REQUESTS = []

def get_mock_classrooms():
    return CLASSROOMS

def get_mock_requests():
    return REQUESTS

def add_request(req: ClassRequest):
    REQUESTS.append(req)
