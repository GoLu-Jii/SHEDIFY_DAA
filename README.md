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


## 🏗️ Backend Architecture and Setup

*   **Backend folder**: `backend/` contains the FastAPI app, scheduling logic, and data models.
*   **Main app**: `backend/main.py` starts the FastAPI server with Uvicorn.
*   **Scheduler**: `backend/scheduler.py` implements the core conflict-checking and greedy graph coloring.
*   **Models**: `backend/models.py` defines the data structures for classrooms, requests, and schedules.

*   **Set up a virtual environment**:
    ```bash
    python -m venv .venv
    .venv\Scripts\activate.Ps1
    pip install -r requirements.txt
    ```
*   **Run locally**: start the server with:
    ```bash
    uvicorn backend.main:app --reload
    ```