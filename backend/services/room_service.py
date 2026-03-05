"""Room service for managing rooms and finding available rooms."""

from typing import List, Optional
from backend.models.room import Room
from backend.models.class_request import ClassRequest
from backend.config.rooms import get_all_rooms


class RoomService:
    """Service for managing rooms and room allocation."""
    
    def __init__(self):
        """Initialize room service with all available rooms."""
        self.rooms = get_all_rooms()
        self._room_dict = {room.room_id: room for room in self.rooms}
    
    def get_all_rooms(self) -> List[Room]:
        """Get all available rooms."""
        return self.rooms.copy()
    
    def get_room_by_id(self, room_id: str) -> Optional[Room]:
        """Get room by ID."""
        return self._room_dict.get(room_id)
    
    def get_rooms_by_type(self, room_type: str) -> List[Room]:
        """Get all rooms of a specific type."""
        return [room for room in self.rooms if room.room_type == room_type]
    
    def get_rooms_by_block(self, block: str) -> List[Room]:
        """Get all rooms in a specific block."""
        return [room for room in self.rooms if room.block.upper() == block.upper()]
    
    def find_available_room(self, class_request: ClassRequest, 
                           exclude_rooms: Optional[List[Room]] = None) -> Optional[Room]:
        """
        Find an available room for a class request.
        
        Priority:
        1. Rooms that match the required room type
        2. Rooms that are not in the exclude list
        3. First available room
        
        Args:
            class_request: The class request to find a room for
            exclude_rooms: List of rooms to exclude from search
            
        Returns:
            Available room or None if no room is available
        """
        exclude_room_ids = {room.room_id for room in exclude_rooms} if exclude_rooms else set()
        
        # Filter available rooms
        available_rooms = [
            room for room in self.rooms 
            if room.room_id not in exclude_room_ids and room.can_accommodate(class_request)
        ]
        
        if not available_rooms:
            return None
        
        # Prioritize rooms by type match
        if class_request.room_type != "any":
            type_matched = [r for r in available_rooms if r.room_type == class_request.room_type]
            if type_matched:
                available_rooms = type_matched
        
        # Return first available (could be enhanced with more sophisticated selection)
        return available_rooms[0]
    
    def reset_all_rooms(self):
        """Reset all rooms (clear allocations). Useful for testing or re-scheduling."""
        for room in self.rooms:
            room.allocated_classes = []
            room.last_end_time = 0
