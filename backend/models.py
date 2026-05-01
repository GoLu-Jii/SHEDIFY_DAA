from dataclasses import dataclass
from datetime import time

@dataclass
class Classroom:
    id: str
    capacity: int
    room_type: str  # e.g., 'lecture', 'lab', 'general'

@dataclass
class ClassRequest:
    id: str
    course_name: str
    start_time: time
    end_time: time
    requested_room_type: str
    expected_students: int

@dataclass
class Schedule:
    request_id: str
    classroom_id: str


# welcome to shedify