"""Simple test script to verify the scheduling system works."""

from backend.main import schedule_classes
import json

# Test data
test_requests = [
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
    },
    {
        "class_id": "CS103-1",
        "class_name": "Database Systems",
        "start_time": "11:00",
        "end_time": "12:30",
        "room_type": "regular",
        "day": "Monday",
        "instructor": "Dr. Brown",
        "course_code": "CS103"
    },
    {
        "class_id": "CS104-1",
        "class_name": "Software Engineering Seminar",
        "start_time": "14:00",
        "end_time": "16:00",
        "room_type": "seminar_hall",
        "day": "Monday",
        "instructor": "Dr. Wilson",
        "course_code": "CS104"
    }
]

if __name__ == "__main__":
    print("=" * 60)
    print("Shedify Scheduling System - Test Run")
    print("=" * 60)
    print(f"\nInput: {len(test_requests)} class requests\n")
    
    result = schedule_classes(test_requests)
    
    print("\n" + "=" * 60)
    print("SCHEDULING RESULTS")
    print("=" * 60)
    
    print("\nStatistics:")
    stats = result["statistics"]
    print(f"  Total Classes: {stats['total_classes']}")
    print(f"  Scheduled: {stats['scheduled_classes']}")
    print(f"  Unscheduled: {stats['unscheduled_classes']}")
    print(f"  Rooms Used: {stats['rooms_used']}")
    print(f"  Utilization Rate: {stats['utilization_rate']}%")
    
    print("\nSchedule:")
    for item in result["schedule"]:
        print(f"  • {item['class_name']} ({item['class_id']})")
        print(f"    Room: {item['room_id']} (Block {item['block']})")
        print(f"    Time: {item['start_time']} - {item['end_time']}")
        print(f"    Day: {item['day']}")
        print()
    
    if result["unscheduled"]:
        print("\n[WARNING] Unscheduled Classes:")
        for item in result["unscheduled"]:
            print(f"  • {item['class_name']} ({item['class_id']}) - {item.get('reason', 'No reason')}")
    
    if result["conflicts"]:
        print("\n[ERROR] Conflicts Detected:")
        for conflict in result["conflicts"]:
            print(f"  • Room {conflict['room_id']}: {conflict['class1_id']} vs {conflict['class2_id']}")
    else:
        print("\n[SUCCESS] No conflicts detected!")
    
    print("\n" + "=" * 60)
    print("Test completed successfully!")
    print("=" * 60)
