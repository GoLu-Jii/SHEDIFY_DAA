document.addEventListener('DOMContentLoaded', () => {
    fetchRooms();
    fetchSchedule();
    
    document.getElementById('booking-form').addEventListener('submit', handleBooking);
});

async function fetchRooms() {
    try {
        const res = await fetch('http://localhost:8000/api/rooms');
        const result = await res.json();
        if (result.status === 'success') {
            const select = document.getElementById('room_id');
            select.innerHTML = '<option value="">Select a room</option>';
            result.data.forEach(r => {
                select.innerHTML += `<option value="${r.id}">${r.id} (${r.room_type}, cap: ${r.capacity})</option>`;
            });
        }
    } catch (e) {
        console.error('Error fetching rooms', e);
    }
}

async function handleBooking(e) {
    e.preventDefault();
    const btn = e.target.querySelector('button');
    const msg = document.getElementById('booking-message');
    
    btn.textContent = 'Booking...';
    btn.disabled = true;
    msg.className = 'message hidden';
    
    const payload = {
        course_name: document.getElementById('course_name').value,
        room_id: document.getElementById('room_id').value,
        start_time: document.getElementById('start_time').value,
        end_time: document.getElementById('end_time').value,
        expected_students: parseInt(document.getElementById('expected_students').value)
    };
    
    try {
        const res = await fetch('http://localhost:8000/api/book', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(payload)
        });
        const data = await res.json();
        
        if (res.ok) {
            msg.textContent = data.message;
            msg.className = 'message success';
            e.target.reset(); // Clear the form
            fetchSchedule();  // Refresh the grid
        } else {
            msg.textContent = data.detail || 'Booking failed';
            msg.className = 'message error';
        }
    } catch (err) {
        msg.textContent = 'Network error while booking.';
        msg.className = 'message error';
    } finally {
        btn.textContent = 'Confirm Booking';
        btn.disabled = false;
        msg.classList.remove('hidden');
    }
}

async function fetchSchedule() {
    try {
        const response = await fetch('http://localhost:8000/api/schedule');
        const result = await response.json();
        
        if (result.status === 'success') {
            renderSchedule(result.data);
        } else {
            showError('Failed to fetch schedule.');
        }
    } catch (error) {
        console.error('Error fetching schedule:', error);
        showError('Cannot connect to the backend server. Make sure it is running on port 8000.');
    }
}

function renderSchedule(rooms) {
    const loader = document.getElementById('loader');
    const grid = document.getElementById('schedule-grid');
    
    if (loader) loader.classList.add('hidden');
    grid.classList.remove('hidden');
    grid.innerHTML = '';
    
    rooms.forEach(room => {
        const card = document.createElement('div');
        card.className = 'room-card';
        
        const header = `
            <div class="room-header">
                <h2>${room.id}</h2>
                <span class="badge">${room.type} (${room.capacity} cap)</span>
            </div>
        `;
        
        let classesHtml = '<div class="class-list">';
        
        if (room.classes.length === 0) {
            classesHtml += '<div class="empty-state">No classes scheduled</div>';
        } else {
            room.classes.forEach(cls => {
                // Determine if this is a manual booking to style differently
                const isManual = cls.id.startsWith("BOOK_");
                classesHtml += `
                    <div class="class-item ${isManual ? 'manual-booking' : ''}">
                        <div class="class-time">${cls.start_time} - ${cls.end_time}</div>
                        <div class="class-title">${cls.course_name} <span style="font-size:0.8rem; font-weight:normal;">(${cls.class_type})</span></div>
                        <div class="class-meta">
                            <span>👥 ${cls.expected_students} students</span>
                        </div>
                    </div>
                `;
            });
        }
        
        classesHtml += '</div>';
        card.innerHTML = header + classesHtml;
        grid.appendChild(card);
    });
}

function showError(message) {
    const loader = document.getElementById('loader');
    loader.textContent = message;
    loader.style.color = '#ef4444';
}
