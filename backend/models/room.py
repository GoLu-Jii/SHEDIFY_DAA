"""Room model for scheduling."""

from dataclasses import dataclass, field
from typing import List, Optional
from backend.models.class_request import ClassRequest


@dataclass
class Room:
    """Represents a room in the institution."""
    
    room_id: str
    block: str
    room_type: str  # "regular", "lab", "seminar_hall"
    capacity: Optional[int] = None
    
    def __post_init__(self):
        """Initialize room state."""
        self.allocated_classes: List[ClassRequest] = []
        self.last_end_time: int = 0  # Minutes since midnight
    
    def is_available_at(self, start_time: int, end_time: int) -> bool:
        """Check if room is available for the given time slot."""
        # Check if the requested time slot overlaps with any allocated class
        for allocated_class in self.allocated_classes:
            if (start_time < allocated_class.end_minutes and 
                allocated_class.start_minutes < end_time):
                return False
        return True
    
    def can_accommodate(self, class_request: ClassRequest) -> bool:
        """Check if room can accommodate the class request."""
        # Check room type compatibility
        if class_request.room_type == "any":
            return True
        if class_request.room_type == "lab" and self.room_type != "lab":
            return False
        if class_request.room_type == "seminar_hall" and self.room_type != "seminar_hall":
            return False
        if class_request.room_type == "regular" and self.room_type not in ["regular", "seminar_hall"]:
            return False
        
        # Check time availability
        return self.is_available_at(class_request.start_minutes, class_request.end_minutes)
    
    def allocate_class(self, class_request: ClassRequest) -> bool:
        """Allocate a class to this room."""
        if not self.can_accommodate(class_request):
            return False
        
        self.allocated_classes.append(class_request)
        self.last_end_time = max(self.last_end_time, class_request.end_minutes)
        return True
    
    def get_schedule(self) -> List[ClassRequest]:
        """Get all classes allocated to this room, sorted by start time."""
        return sorted(self.allocated_classes, key=lambda c: c.start_minutes)
    
    def __repr__(self) -> str:
        return f"Room({self.room_id}, {self.block}, {self.room_type})"
