from backend.database import get_mock_classrooms, get_mock_requests
from backend.scheduler import schedule_classes

def main():
    print("Initializing SHEDIFY Schedule Generation...")
    
    classrooms = get_mock_classrooms()
    requests = get_mock_requests()
    
    print(f"Loaded {len(classrooms)} Classrooms and {len(requests)} Class Requests.\n")
    
    schedules = schedule_classes(requests, classrooms)
    
    print("----- FINAL ALLOCATED SCHEDULE -----")
    if not schedules:
        print("No classes could be scheduled.")
        
    schedules_by_room = {}
    for s in schedules:
        schedules_by_room.setdefault(s.classroom_id, []).append(s)
        
    for room_id, allocated_schedules in schedules_by_room.items():
        print(f"\n[Room: {room_id}]")
        for sched in allocated_schedules:
            req = next(r for r in requests if r.id == sched.request_id)
            print(f"  -> {req.start_time.strftime('%H:%M')} - {req.end_time.strftime('%H:%M')} | {req.course_name} ({req.class_type}, {req.expected_students} students)")

if __name__ == "__main__":
    main()
