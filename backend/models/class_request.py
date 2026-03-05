"""Class request model for scheduling."""

from dataclasses import dataclass
from typing import Optional


@dataclass
class ClassRequest:
    """Represents a class scheduling request."""
    
    class_id: str
    class_name: str
    start_time: str  # Format: "HH:MM" (24-hour format)
    end_time: str    # Format: "HH:MM" (24-hour format)
    room_type: str   # "regular", "lab", "seminar_hall", or "any"
    day: str         # Day of the week (e.g., "Monday", "Tuesday")
    instructor: Optional[str] = None
    course_code: Optional[str] = None
    
    def __post_init__(self):
        """Validate and convert time strings to minutes for easier comparison."""
        self.start_minutes = self._time_to_minutes(self.start_time)
        self.end_minutes = self._time_to_minutes(self.end_time)
        
        if self.start_minutes >= self.end_minutes:
            raise ValueError(f"Start time {self.start_time} must be before end time {self.end_time}")
    
    @staticmethod
    def _time_to_minutes(time_str: str) -> int:
        """Convert time string (HH:MM) to minutes since midnight."""
        try:
            hours, minutes = map(int, time_str.split(':'))
            if not (0 <= hours < 24 and 0 <= minutes < 60):
                raise ValueError(f"Invalid time format: {time_str}")
            return hours * 60 + minutes
        except (ValueError, AttributeError) as e:
            raise ValueError(f"Time must be in HH:MM format. Got: {time_str}") from e
    
    def overlaps_with(self, other: 'ClassRequest') -> bool:
        """Check if this class overlaps with another class."""
        return (self.start_minutes < other.end_minutes and 
                other.start_minutes < self.end_minutes)
    
    def __lt__(self, other: 'ClassRequest') -> bool:
        """Compare by start time for sorting."""
        return self.start_minutes < other.start_minutes
    
    def __repr__(self) -> str:
        return f"ClassRequest({self.class_id}, {self.class_name}, {self.start_time}-{self.end_time})"
