const API_URL = "http://localhost:8000";

// 1. Initial Load: Get allocated rooms from the backend
window.addEventListener('DOMContentLoaded', () => {
    loadAllocatedRooms();
});

// Function to fetch and display allocated rooms
async function loadAllocatedRooms() {
    const grid = document.getElementById('allocated-rooms');
    
    try {
        // Fetch rooms and existing schedules
        const [roomsRes, scheduleRes] = await Promise.all([
            fetch(`${API_URL}/classrooms`),
            fetch(`${API_URL}/schedules`)
        ]);
        
        const rooms = await roomsRes.json();
        const scheduleData = await scheduleRes.json();
        const schedules = scheduleData.schedules || [];
        // Create room lookup
        const roomMap = {};
        rooms.forEach(r => roomMap[r.id] = r);
        
        grid.innerHTML = "";
        
        if (schedules.length === 0) {
            grid.innerHTML = '<p style="color:var(--grey-text)">No rooms allocated yet.</p>';
            return;
        }
        
        schedules.forEach(schedule => {
            const room = roomMap[schedule.classroom_id];
            const roomCard = document.createElement('div');
            roomCard.className = 'card';
            roomCard.innerHTML = `
                <h3>${schedule.classroom_id}</h3>
                <p style="color:var(--grey-text)">${room?.room_type.toUpperCase() || 'UNKNOWN'} | Cap: ${room?.capacity || '-'}</p>
                <p><strong>Request:</strong> ${schedule.request_id}</p>
                <button class="button delete-btn" data-id="${schedule.request_id}" style="background:#dc2626;margin-top:10px;">Delete</button>
            `;
            grid.appendChild(roomCard);
        });
        
        // Add delete event listeners
        document.querySelectorAll('.delete-btn').forEach(btn => {
            btn.addEventListener('click', async (e) => {
                const requestId = e.target.dataset.id;
                await deleteRoom(requestId);
            });
        });
        
    } catch (err) {
        grid.innerHTML = "<p>Error: Could not connect to the backend.</p>";
    }
}

// Delete a room allocation
async function deleteRoom(requestId) {
    if (!confirm(`Delete allocation ${requestId}?`)) return;
    
    try {
        const response = await fetch(`${API_URL}/delete/${requestId}`, {
            method: 'DELETE'
        });
        const result = await response.json();
        alert(`Deleted ${requestId}`);
        loadAllocatedRooms(); // Refresh the list
    } catch (err) {
        alert("Error deleting allocation");
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

// 3. Displaying the schedules from the backend (only the newly booked room)
function showOutput(data) {
    const outputDiv = document.getElementById('room-suggestions');
    const schedules = data.schedules || [];
    if (schedules.length === 0) {
        outputDiv.innerHTML = "<p style='color:red'>No rooms available for this slot.</p>";
        return;
    }
    // Show only the most recently added schedule (last one)
    const latestSchedule = schedules[schedules.length - 1];
    outputDiv.innerHTML = "<h3 style='margin-top:20px;'>Your Booked Room:</h3>";
    const suggestion = document.createElement('div');
    suggestion.className = 'card';
    suggestion.style.marginTop = "10px";
    suggestion.style.padding = "10px";
    suggestion.innerHTML = `
        <strong>Room:</strong> ${latestSchedule.classroom_id}<br>
        <strong>Request ID:</strong> ${latestSchedule.request_id}
    `;
    outputDiv.appendChild(suggestion);
    
    // Refresh the allocated rooms list
    loadAllocatedRooms();
}
