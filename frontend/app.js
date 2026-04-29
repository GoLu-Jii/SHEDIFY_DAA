const API_URL = "http://localhost:8000";

// 1. Initial Load: Get the rooms from the backend as soon as the page opens
window.addEventListener('DOMContentLoaded', () => {
    updateCampusGrid();
});

// Function to fetch and display classrooms
async function updateCampusGrid() {
    const grid = document.getElementById('timetable-layout');
    
    try {
        const response = await fetch(`${API_URL}/classrooms`);
        const rooms = await response.json();
        
        grid.innerHTML = ""; // Clear any placeholder text
        rooms.forEach(room => {
            const roomCard = document.createElement('div');
            roomCard.className = 'card';
            roomCard.innerHTML = `
                <h3>${room.id}</h3>
                <p style="color:var(--grey-text)">${room.room_type.toUpperCase()} | Cap: ${room.capacity}</p>
            `;
            grid.appendChild(roomCard);
        });
    } catch (err) {
        grid.innerHTML = "<p>Error: Could not connect to the backend.</p>";
    }
}

// 2. Form Logic: Sending the booking request
const entryForm = document.getElementById('main-input-form');

if (entryForm) {
    entryForm.addEventListener('submit', async (e) => {
        e.preventDefault();

        // Collecting data from our 'humanized' IDs
        const newEntry = {
            course_name: document.getElementById('subject-name').value,
            start_time: document.getElementById('time-from').value,
            end_time: document.getElementById('time-to').value,
            class_type: "lecture", // Default for the schema
            requested_room_type: document.getElementById('room_type').value,
            expected_students: parseInt(document.getElementById('headcount').value)
        };

        // Important: Backend expects a LIST [newEntry]
        try {
            const response = await fetch(`${API_URL}/schedule`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify([newEntry]) 
            });

            const result = await response.json();
            showOutput(result);
        } catch (err) {
            alert("Connection error. Is FastAPI running?");
        }
    });
}

// 3. Displaying the recommendations from the Conflict Graph
function showOutput(data) {
    const outputDiv = document.getElementById('room-suggestions');
    outputDiv.innerHTML = "<h3 style='margin-top:20px;'>Recommended Rooms:</h3>";
    
    // We loop through the 'recommendations' dictionary from Python
    for (const reqId in data.recommendations) {
        const roomsList = data.recommendations[reqId];
        
        if (roomsList.length === 0) {
            outputDiv.innerHTML += `<p style="color:red">No rooms available for this slot.</p>`;
        }

        roomsList.forEach(roomId => {
            const suggestion = document.createElement('div');
            suggestion.className = 'card';
            suggestion.style.marginTop = "10px";
            suggestion.style.padding = "10px";
            suggestion.innerHTML = `<strong>${roomId}</strong>`;
            outputDiv.appendChild(suggestion);
        });
    }
}
