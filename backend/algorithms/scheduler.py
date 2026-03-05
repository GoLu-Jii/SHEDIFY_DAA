"""Greedy scheduling algorithm with min heap optimization."""

import heapq
from typing import List, Tuple, Dict
from backend.models.class_request import ClassRequest
from backend.models.room import Room
from backend.services.room_service import RoomService


class Scheduler:
    """Main scheduler using greedy algorithm with priority queue optimization."""
    
    def __init__(self, room_service: RoomService):
        """Initialize scheduler with room service."""
        self.room_service = room_service
    
    def schedule_classes(self, class_requests: List[ClassRequest]) -> Dict[str, any]:
        """
        Schedule classes using greedy algorithm with min heap.
        
        Algorithm:
        1. Sort classes by start time
        2. Use min heap to track rooms by their end times
        3. For each class, check if any room is free
        4. If yes, reuse room; else allocate new room
        5. Push updated room end time back to heap
        
        Returns:
            Dictionary containing:
            - schedule: List of scheduled classes with room assignments
            - conflicts: List of conflicts if any
            - statistics: Scheduling statistics
        """
        if not class_requests:
            return {
                "schedule": [],
                "conflicts": [],
                "statistics": {
                    "total_classes": 0,
                    "scheduled_classes": 0,
                    "unscheduled_classes": 0,
                    "rooms_used": 0
                }
            }
        
        # Sort classes by start time (greedy approach)
        sorted_classes = sorted(class_requests, key=lambda c: c.start_minutes)
        
        # Min heap: (last_end_time, room_id)
        # Room that becomes free earliest is at the top
        heap: List[Tuple[int, str]] = []
        
        # Track room usage
        room_usage: Dict[str, Room] = {}
        scheduled_classes = []
        unscheduled_classes = []
        
        # Process each class
        for class_request in sorted_classes:
            allocated = False
            
            # Check if any room in heap is available
            # (room's last end time <= current class start time)
            while heap and heap[0][0] <= class_request.start_minutes:
                end_time, room_id = heapq.heappop(heap)
                room = room_usage[room_id]
                
                # Check if room can accommodate this class
                if room.can_accommodate(class_request):
                    room.allocate_class(class_request)
                    scheduled_classes.append({
                        "class": class_request,
                        "room": room,
                        "room_id": room.room_id,
                        "block": room.block
                    })
                    # Push updated end time back to heap
                    heapq.heappush(heap, (room.last_end_time, room_id))
                    allocated = True
                    break
            
            # If no room was available, try to allocate a new room
            if not allocated:
                available_room = self.room_service.find_available_room(
                    class_request, 
                    list(room_usage.values())
                )
                
                if available_room:
                    available_room.allocate_class(class_request)
                    room_id = available_room.room_id
                    room_usage[room_id] = available_room
                    scheduled_classes.append({
                        "class": class_request,
                        "room": available_room,
                        "room_id": available_room.room_id,
                        "block": available_room.block
                    })
                    # Push to heap
                    heapq.heappush(heap, (available_room.last_end_time, room_id))
                    allocated = True
                else:
                    unscheduled_classes.append(class_request)
        
        # Detect conflicts
        conflicts = self._detect_conflicts(scheduled_classes)
        
        # Calculate statistics
        rooms_used = len(set(item["room_id"] for item in scheduled_classes))
        
        statistics = {
            "total_classes": len(class_requests),
            "scheduled_classes": len(scheduled_classes),
            "unscheduled_classes": len(unscheduled_classes),
            "rooms_used": rooms_used,
            "utilization_rate": round(rooms_used / len(self.room_service.get_all_rooms()) * 100, 2) if self.room_service.get_all_rooms() else 0
        }
        
        return {
            "schedule": scheduled_classes,
            "conflicts": conflicts,
            "unscheduled": unscheduled_classes,
            "statistics": statistics
        }
    
    def _detect_conflicts(self, scheduled_classes: List[Dict]) -> List[Dict]:
        """
        Detect conflicts in the schedule.
        
        A conflict occurs when two classes in the same room overlap.
        """
        conflicts = []
        
        # Group by room
        room_schedules: Dict[str, List[ClassRequest]] = {}
        for item in scheduled_classes:
            room_id = item["room_id"]
            if room_id not in room_schedules:
                room_schedules[room_id] = []
            room_schedules[room_id].append(item["class"])
        
        # Check for overlaps within each room
        for room_id, classes in room_schedules.items():
            for i, class1 in enumerate(classes):
                for class2 in classes[i + 1:]:
                    if class1.overlaps_with(class2):
                        conflicts.append({
                            "room_id": room_id,
                            "class1": class1,
                            "class2": class2,
                            "type": "room_overlap"
                        })
        
        return conflicts
