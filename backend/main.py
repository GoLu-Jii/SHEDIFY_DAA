"""Main entry point for Shedify scheduling system."""

import json
from typing import List, Dict
from backend.models.class_request import ClassRequest
from backend.services.room_service import RoomService
from backend.algorithms.scheduler import Scheduler


def create_class_request(data: Dict) -> ClassRequest:
    """Create a ClassRequest from dictionary data."""
    return ClassRequest(
        class_id=data.get("class_id", ""),
        class_name=data.get("class_name", ""),
        start_time=data.get("start_time", ""),
        end_time=data.get("end_time", ""),
        room_type=data.get("room_type", "any"),
        day=data.get("day", ""),
        instructor=data.get("instructor"),
        course_code=data.get("course_code")
    )


def schedule_classes(class_requests_data: List[Dict]) -> Dict:
    """
    Main function to schedule classes.
    
    Args:
        class_requests_data: List of dictionaries containing class request data
        
    Returns:
        Dictionary with schedule, conflicts, and statistics
    """
    # Initialize services
    room_service = RoomService()
    scheduler = Scheduler(room_service)
    
    # Reset rooms for fresh scheduling
    room_service.reset_all_rooms()
    
    # Create class requests
    class_requests = []
    for data in class_requests_data:
        try:
            class_request = create_class_request(data)
            class_requests.append(class_request)
        except Exception as e:
            print(f"Error creating class request: {e}")
            continue
    
    # Schedule classes
    result = scheduler.schedule_classes(class_requests)
    
    # Format result for output
    formatted_result = {
        "schedule": [
            {
                "class_id": item["class"].class_id,
                "class_name": item["class"].class_name,
                "start_time": item["class"].start_time,
                "end_time": item["class"].end_time,
                "day": item["class"].day,
                "room_id": item["room_id"],
                "block": item["block"],
                "room_type": item["room"].room_type,
                "instructor": item["class"].instructor,
                "course_code": item["class"].course_code
            }
            for item in result["schedule"]
        ],
        "unscheduled": [
            {
                "class_id": req.class_id,
                "class_name": req.class_name,
                "start_time": req.start_time,
                "end_time": req.end_time,
                "day": req.day,
                "reason": "No available room"
            }
            for req in result["unscheduled"]
        ],
        "conflicts": [
            {
                "room_id": conflict["room_id"],
                "class1_id": conflict["class1"].class_id,
                "class2_id": conflict["class2"].class_id,
                "type": conflict["type"]
            }
            for conflict in result["conflicts"]
        ],
        "statistics": result["statistics"]
    }
    
    return formatted_result


if __name__ == "__main__":
    # Example usage
    example_requests = [
        {
            "class_id": "CS101-1",
            "class_name": "Data Structures",
            "start_time": "09:00",
            "end_time": "10:30",
            "room_type": "regular",
            "day": "Monday",
            "instructor": "Dr. Smith",
            "course_code": "CS101"
        },
        {
            "class_id": "CS101-2",
            "class_name": "Data Structures Lab",
            "start_time": "10:30",
            "end_time": "12:00",
            "room_type": "lab",
            "day": "Monday",
            "instructor": "Dr. Smith",
            "course_code": "CS101"
        },
        {
            "class_id": "CS102-1",
            "class_name": "Algorithms",
            "start_time": "09:00",
            "end_time": "10:30",
            "room_type": "regular",
            "day": "Monday",
            "instructor": "Dr. Jones",
            "course_code": "CS102"
        }
    ]
    
    result = schedule_classes(example_requests)
    print(json.dumps(result, indent=2))
