# SHEDIFY 🗓️✨

**SHEDIFY** is an automated, high-performance class and resource scheduling system designed to provide conflict-free allocations of rooms and time slots. By leveraging advanced Design and Analysis of Algorithms (DAA) techniques like **Graph Coloring** and **Greedy Scheduling**, it effectively manages complex scheduling constraints, preventing double-bookings while optimizing room usage.

## 🚀 Key Features

*   **Conflict-Free Automation**: Utilizes Graph Coloring algorithms to ensure that multiple class requests do not overlap in the same room.
*   **Interactive Real-Time Booking**: Features a dynamic frontend that allows users to manually book rooms while validating against existing schedules to prevent double-booking.
*   **Intelligent Fallbacks**: Implements a Best-Fit greedy approach to place smaller classes in optimally sized rooms, preserving larger venues.
*   **Modern Web Interface**: Built with a sleek, responsive, and glassmorphic UI design to provide a premium user experience.

## 🛠️ Technology Stack

*   **Backend**: Python, [FastAPI](https://fastapi.tiangolo.com/), Uvicorn
*   **Frontend**: HTML5, Vanilla CSS (Glassmorphism), JavaScript
*   **Core Logic Algorithms**: Greedy Graph Coloring

## 🧠 Approach & Algorithm Design (DAA Techniques)

The core logic of SHEDIFY translates complex scheduling constraints into an algorithmic graph problem.

1.  **Conflict Graph Construction**: 
    The system interprets each class request as a "Node". If two requests overlap in time, an "Edge" is drawn between them, indicating a conflict.
2.  **Greedy Graph Coloring**: 
    Each room acts as a distinct "Color". The scheduling engine sorts requests by their degree of conflict (most constrained requests first). It then assigns an available classroom (color) to a request ensuring that no two adjacent nodes (conflicting time segments) share the same classroom.
3.  **Capacity Validation (Best-Fit)**: 
    When assigning classrooms, the system evaluates available rooms based on capacity vs. expected students, dynamically assigning the optimal room.

## 📂 Project Structure

```
d:\Projects\SHEDIFY\
├── backend/
│   ├── api.py           # FastAPI application and endpoints
│   ├── models.py        # Data classes (Classroom, ClassRequest, Schedule)
│   ├── scheduler.py     # Graph coloring and greedy scheduling algorithms
│   └── database.py      # Mock database / storage management
├── frontend/
│   ├── index.html       # Application entry point / layout
│   ├── style.css        # Glassmorphic and responsive styling
│   └── app.js           # Interactive UI logic & API integration
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

## 🚶 Walkthrough of Current Implementation

1.  **Initialization**: When the FastAPI backend is launched, it exposes REST endpoints and holds mock data of classrooms and class requests.
2.  **Schedule Generation**: Upon hitting the `/api/schedule` endpoint from the frontend, the backend runs the Greedy Graph Coloring algorithm dynamically on the existing class requests to map them cleanly across available rooms without time overlaps.
3.  **Interactive Interface**: The user opens the `index.html` frontend, which securely fetches the dynamically sorted schedules and classroom metadata, rendering everything nicely in an interactive grid.
4.  **Manual Bookings**: The user can use the "Book a Room" form to submit new, specific booking needs.
5.  **Conflict Validation**: The system intercepts manual bookings, simulates inserting them into the existing graph nodes, and runs strict runtime verifications. It throws HTTP 400/409 errors visually if the manual booking exceeds room capacity or clashes with established schedules.

## 🔮 Future Implementations & Roadmap

We plan to expand SHEDIFY with several massive improvements tailored for real-world scaling:

1.  **University-Specific Database Integration**: 
    Replacing the current mock objects with a robust SQL/NoSQL database mapping explicitly to our own university's actual infrastructure (specific building blueprints, rooms, physical capacities, and exact offered courses curriculum).
2.  **Advanced UI / Frontend Enhancements**: 
    - Full-scale calendar integrations (Daily/Weekly/Monthly views).
    - Drag-and-drop scheduling capabilities allowing admins to visually shift classes around.
    - Role-based authentication (Admin vs. Professor vs. Student views).
3.  **Enhanced Scheduling Constraints**:
    Incorporating additional complex heuristics such as professor availability, travel time between buildings, or specific equipment requirements (e.g., projectors, chemistry lab stations).
4.  **Export and Notifications**:
    Options to seamlessly export completed schedules to PDF or synchronize natively with Google Calendar / Outlook. 

## ⚙️ Setup and Installation

### Prerequisites
*   Python 3.8+
*   Any modern web browser

### Running the Backend Server

1.  Navigate to the project root directory:
    ```bash
    cd d:/Projects/SHEDIFY
    ```
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Start the FastAPI server via Uvicorn:
    ```bash
    uvicorn backend.api:app --reload
    ```
    The API should now be running on `http://127.0.0.1:8000`. You can view the automatically generated API docs at `http://127.0.0.1:8000/docs`.

### Running the Frontend

Since the frontend is built using standard web technologies, you don't need a heavy build process.

1.  Open the `frontend/index.html` file directly in your web browser.
    *   *Alternatively, you can use an extension like VS Code Live Server to serve the frontend directory.*
2.  The application will automatically connect to the locally running backend to fetch schedules and available rooms.

## 📝 API Endpoints

*   `GET /api/schedule`: Generates and retrieves the optimally computed class schedule.
*   `GET /api/rooms`: Retrieves a list of available classrooms.
*   `POST /api/book`: Submits a manual room booking request. Rejects the request if there is a time overlap conflict or capacity issue.

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request or open an issue to discuss proposed changes or feature additions.
