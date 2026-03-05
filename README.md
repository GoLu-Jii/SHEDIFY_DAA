# Shedify - Automated Class Scheduling System

Shedify is an automated class scheduling system designed for educational institutions. It efficiently schedules multiple class requests across limited resources (classrooms, labs, seminar halls) while preventing conflicts and optimizing resource utilization.

## Features

- **Automated Scheduling**: Uses greedy algorithm with min heap optimization for efficient room allocation
- **Conflict Prevention**: Ensures no overlapping classes use the same room
- **Resource Optimization**: Maximizes utilization of available classrooms, labs, and seminar halls
- **Room Type Support**: Handles regular classrooms, laboratories, and seminar halls
- **Real-time Output**: Provides immediate scheduling results with statistics

## DAA Techniques Applied

1. **Greedy Scheduling Algorithm**: Assigns classes to available rooms by selecting non-conflicting time slots efficiently
2. **Graph Coloring Technique**: Represents classes as nodes and overlapping classes as edges, where each color represents a classroom
3. **Priority Queue (Min Heap)**: Tracks classrooms based on their current end times to quickly find available rooms

## Project Structure

```
SHEDIFY/
├── backend/
│   ├── algorithms/
│   │   ├── __init__.py
│   │   ├── scheduler.py          # Main greedy scheduling algorithm
│   │   └── conflict_detector.py  # Conflict detection utilities
│   ├── models/
│   │   ├── __init__.py
│   │   ├── class_request.py      # Class request data model
│   │   └── room.py               # Room data model
│   ├── services/
│   │   ├── __init__.py
│   │   └── room_service.py      # Room management service
│   ├── config/
│   │   ├── __init__.py
│   │   └── rooms.py              # Room configuration (all blocks)
│   └── main.py                   # Main entry point
├── frontend/
│   ├── index.html                # Main UI
│   ├── style.css                 # Styling
│   └── app.js                    # Frontend logic
├── requirements.txt
└── README.md
```

## Algorithm Design

### Greedy Room Allocation Algorithm

```
1. Sort classes by start_time
2. Initialize empty min heap (priority queue)
3. For each class:
   a. If heap is not empty and heap.top.end_time <= class.start_time:
      - Pop room from heap
      - Assign class to room
   b. Else:
      - Allocate new room
      - Assign class to new room
   c. Push (room_id, class.end_time) into heap
4. Output final schedule
```

### Complexity Analysis

- **Sorting classes**: O(N log N)
- **Conflict checking**: O(N²) worst case
- **Greedy room assignment**: O(N)
- **Overall Complexity**: O(N log N) average case, O(N²) for dense conflicts

## Room Configuration

The system supports multiple blocks with various room types:

- **Block A**: Regular classrooms (A001-A005, A101-A104), Computer labs, Electronics lab, Physics lab
- **Block B**: Thermodynamics lab, Advance civil lab, Computer lab-4
- **Block C**: Regular classrooms (C001-C005, C101-C104, C201-C205, C301-C306), Labs, Old seminar hall
- **Block D**: Regular classrooms (D001-D007, D101-D109, D201-D209, D301-D309), Seminar halls
- **Block E**: Similar to Block C with additional computer labs

## Usage

### Backend (Python)

```python
from backend.main import schedule_classes

# Example class requests
class_requests = [
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
    # ... more requests
]

result = schedule_classes(class_requests)
print(result)
```

### Frontend

1. Open `frontend/index.html` in a web browser
2. Add class requests using the form
3. Click "Generate Schedule" to see the optimized schedule

### Running the Backend

#### Option 1: Direct Python Script

```bash
# Navigate to project directory
cd SHEDIFY

# Run the main script
python backend/main.py
```

#### Option 2: API Server (for frontend integration)

```bash
# Install dependencies
pip install -r requirements.txt

# Run the API server (from project root)
python backend/api_server.py

# Or run as a module
python -m backend.api_server
```

The API server will start on `http://localhost:8000` and the frontend can connect to it automatically.

**FastAPI Features:**
- Interactive API documentation at `http://localhost:8000/docs`
- Automatic request/response validation
- Built-in CORS support
- Type hints and Pydantic models

## Class Request Format

Each class request should include:

- `class_id`: Unique identifier (e.g., "CS101-1")
- `class_name`: Name of the class
- `start_time`: Start time in "HH:MM" format (24-hour)
- `end_time`: End time in "HH:MM" format (24-hour)
- `room_type`: "regular", "lab", "seminar_hall", or "any"
- `day`: Day of the week
- `instructor`: (Optional) Instructor name
- `course_code`: (Optional) Course code

## Output Format

The scheduler returns:

- **schedule**: List of scheduled classes with room assignments
- **unscheduled**: List of classes that couldn't be scheduled
- **conflicts**: List of detected conflicts (should be empty in optimal scheduling)
- **statistics**: Scheduling statistics including:
  - Total classes
  - Scheduled classes
  - Unscheduled classes
  - Rooms used
  - Utilization rate

## Future Enhancements

- API endpoint for frontend integration
- Database integration for persistent storage
- Multi-day scheduling support
- Capacity-based room allocation
- Instructor preference handling
- Export schedule to calendar formats

## License

This project is developed for educational purposes as part of Design and Analysis of Algorithms coursework.
