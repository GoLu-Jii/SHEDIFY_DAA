document.addEventListener('DOMContentLoaded', () => {
    fetchSchedule();
    document.getElementById('recommendation-form').addEventListener('submit', handleRecommendations);
});

async function handleRecommendations(e) {
    e.preventDefault();
    const btn = e.target.querySelector('button');
    const msg = document.getElementById('booking-message');
    const container = document.getElementById('recommendations-container');
    const list = document.getElementById('recommendations-list');
    
    btn.textContent = 'Finding...';
    btn.disabled = true;
    msg.className = 'message hidden';
    container.classList.add('hidden');
    list.innerHTML = '';
    
    // Save these for when a user actually clicks "Book"
    window.currentBookingPayload = {
        course_name: document.getElementById('course_name').value,
        start_time: document.getElementById('start_time').value,
        end_time: document.getElementById('end_time').value,
        expected_students: parseInt(document.getElementById('expected_students').value),
        room_type: document.getElementById('room_type').value
    };
    
    try {
        const res = await fetch('http://localhost:8000/api/recommend', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify(window.currentBookingPayload)
        });
        const data = await res.json();
        
        if (res.ok && data.data && data.data.length > 0) {
            renderRecommendations(data.data);
            msg.classList.add('hidden'); // Hide any previous error messages
        } else {
            msg.textContent = data.detail || 'No available rooms found for these parameters.';
            msg.className = 'message error';
            msg.classList.remove('hidden');
        }
    } catch (err) {
        msg.textContent = 'Network error while finding recommendations.';
        msg.className = 'message error';
        msg.classList.remove('hidden');
    } finally {
        btn.textContent = 'Find Recommendations';
        btn.disabled = false;
    }
}

function renderRecommendations(rooms) {
    const container = document.getElementById('recommendations-container');
    const list = document.getElementById('recommendations-list');
    container.classList.remove('hidden');
    
    rooms.forEach(room => {
        const card = document.createElement('div');
        card.className = 'recommendation-card';
        card.innerHTML = `
            <div class="rec-info">
                <strong>${room.id}</strong>
                <span>${room.room_type} | ${room.capacity} cap</span>
            </div>
            <button type="button" class="btn btn-small" onclick="bookRoom('${room.id}')">Book</button>
        `;
        list.appendChild(card);
    });
}

async function bookRoom(roomId) {
    const msg = document.getElementById('booking-message');
    msg.className = 'message hidden';
    
    const payload = {
        ...window.currentBookingPayload,
        room_id: roomId
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
            document.getElementById('recommendation-form').reset();
            document.getElementById('recommendations-container').classList.add('hidden');
            fetchSchedule();  // Refresh the schedule grid
        } else {
            msg.textContent = data.detail || 'Booking failed';
            msg.className = 'message error';
        }
        msg.classList.remove('hidden');
    } catch (err) {
        msg.textContent = 'Network error while booking.';
        msg.className = 'message error';
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
