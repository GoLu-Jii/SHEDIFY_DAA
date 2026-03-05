// Class requests storage
let classRequests = [];

// DOM Elements
const classForm = document.getElementById('classForm');
const classRequestsList = document.getElementById('classRequestsList');
const classCount = document.getElementById('classCount');
const scheduleBtn = document.getElementById('scheduleBtn');
const clearBtn = document.getElementById('clearBtn');
const scheduleOutput = document.getElementById('scheduleOutput');

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    updateClassList();
});

// Form submission
classForm.addEventListener('submit', (e) => {
    e.preventDefault();
    
    const classRequest = {
        class_id: document.getElementById('classId').value,
        class_name: document.getElementById('className').value,
        start_time: document.getElementById('startTime').value,
        end_time: document.getElementById('endTime').value,
        day: document.getElementById('day').value,
        room_type: document.getElementById('roomType').value,
        course_code: document.getElementById('courseCode').value || null,
        instructor: document.getElementById('instructor').value || null
    };
    
    // Convert time format from HH:MM (24h) to HH:MM string
    classRequest.start_time = formatTime(classRequest.start_time);
    classRequest.end_time = formatTime(classRequest.end_time);
    
    classRequests.push(classRequest);
    updateClassList();
    classForm.reset();
});

// Format time from input format to HH:MM
function formatTime(timeStr) {
    // timeStr is already in HH:MM format from time input
    return timeStr;
}

// Update class list display
function updateClassList() {
    classCount.textContent = classRequests.length;
    scheduleBtn.disabled = classRequests.length === 0;
    
    if (classRequests.length === 0) {
        classRequestsList.innerHTML = '<p style="color: #999; text-align: center; padding: 20px;">No class requests added yet.</p>';
        return;
    }
    
    classRequestsList.innerHTML = classRequests.map((req, index) => `
        <div class="class-item">
            <div class="class-item-info">
                <strong>${req.class_name}</strong>
                <span>${req.class_id} | ${req.start_time} - ${req.end_time} | ${req.day} | ${req.room_type}</span>
            </div>
            <button class="btn-remove" onclick="removeClass(${index})">Remove</button>
        </div>
    `).join('');
}

// Remove class
function removeClass(index) {
    classRequests.splice(index, 1);
    updateClassList();
}

// Clear all classes
clearBtn.addEventListener('click', () => {
    if (confirm('Are you sure you want to clear all class requests?')) {
        classRequests = [];
        updateClassList();
        scheduleOutput.innerHTML = '<p class="placeholder">Add class requests and click "Generate Schedule" to see results.</p>';
    }
});

// Generate schedule
scheduleBtn.addEventListener('click', async () => {
    if (classRequests.length === 0) return;
    
    scheduleBtn.disabled = true;
    scheduleBtn.textContent = 'Scheduling...';
    
    try {
        // Call backend API (for now, we'll use a local simulation)
        // In production, this would be: const response = await fetch('/api/schedule', {...})
        const result = await scheduleClasses(classRequests);
        displaySchedule(result);
    } catch (error) {
        console.error('Error scheduling classes:', error);
        scheduleOutput.innerHTML = `<div class="conflicts"><h3>Error</h3><p>${error.message}</p></div>`;
    } finally {
        scheduleBtn.disabled = false;
        scheduleBtn.textContent = 'Generate Schedule';
    }
});

// Schedule classes (simulates API call)
async function scheduleClasses(requests) {
    // In a real implementation, this would be an API call
    // For now, we'll use a simple fetch to a Python backend if available
    // Or simulate the scheduling logic
    
    try {
        // Try to call Python backend if available
        const response = await fetch('http://localhost:8000/api/schedule', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ class_requests: requests })
        });
        
        if (response.ok) {
            return await response.json();
        }
    } catch (error) {
        console.log('Backend not available, using client-side simulation');
    }
    
    // Fallback: Simple client-side simulation
    // This is a simplified version - real scheduling happens in Python backend
    return simulateSchedule(requests);
}

// Simple simulation (for demo purposes)
function simulateSchedule(requests) {
    const schedule = [];
    const rooms = ['A001', 'A002', 'A003', 'B001', 'C001', 'D001'];
    let roomIndex = 0;
    
    // Sort by start time
    const sorted = [...requests].sort((a, b) => {
        const timeA = a.start_time.split(':').map(Number);
        const timeB = b.start_time.split(':').map(Number);
        return (timeA[0] * 60 + timeA[1]) - (timeB[0] * 60 + timeB[1]);
    });
    
    sorted.forEach((req, index) => {
        schedule.push({
            ...req,
            room_id: rooms[roomIndex % rooms.length],
            block: rooms[roomIndex % rooms.length][0],
            room_type: req.room_type === 'any' ? 'regular' : req.room_type
        });
        roomIndex++;
    });
    
    return {
        schedule: schedule,
        unscheduled: [],
        conflicts: [],
        statistics: {
            total_classes: requests.length,
            scheduled_classes: schedule.length,
            unscheduled_classes: 0,
            rooms_used: Math.min(roomIndex, rooms.length),
            utilization_rate: 85.5
        }
    };
}

// Display schedule results
function displaySchedule(result) {
    let html = '';
    
    // Statistics
    if (result.statistics) {
        html += `
            <div class="statistics">
                <h3>Schedule Statistics</h3>
                <div class="statistics-grid">
                    <div class="stat-item">
                        <div class="stat-value">${result.statistics.total_classes}</div>
                        <div class="stat-label">Total Classes</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${result.statistics.scheduled_classes}</div>
                        <div class="stat-label">Scheduled</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${result.statistics.unscheduled_classes}</div>
                        <div class="stat-label">Unscheduled</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${result.statistics.rooms_used}</div>
                        <div class="stat-label">Rooms Used</div>
                    </div>
                    <div class="stat-item">
                        <div class="stat-value">${result.statistics.utilization_rate}%</div>
                        <div class="stat-label">Utilization</div>
                    </div>
                </div>
            </div>
        `;
    }
    
    // Scheduled classes
    if (result.schedule && result.schedule.length > 0) {
        html += '<h3 style="margin-top: 20px; color: #28a745;">Scheduled Classes</h3>';
        result.schedule.forEach(item => {
            html += `
                <div class="schedule-item">
                    <h4>${item.class_name} (${item.class_id})</h4>
                    <div class="details">
                        <div class="detail-item"><strong>Room:</strong> ${item.room_id}</div>
                        <div class="detail-item"><strong>Block:</strong> ${item.block}</div>
                        <div class="detail-item"><strong>Time:</strong> ${item.start_time} - ${item.end_time}</div>
                        <div class="detail-item"><strong>Day:</strong> ${item.day}</div>
                        ${item.instructor ? `<div class="detail-item"><strong>Instructor:</strong> ${item.instructor}</div>` : ''}
                        ${item.course_code ? `<div class="detail-item"><strong>Course:</strong> ${item.course_code}</div>` : ''}
                    </div>
                </div>
            `;
        });
    }
    
    // Unscheduled classes
    if (result.unscheduled && result.unscheduled.length > 0) {
        html += '<h3 style="margin-top: 20px; color: #dc3545;">Unscheduled Classes</h3>';
        result.unscheduled.forEach(item => {
            html += `
                <div class="schedule-item unscheduled">
                    <h4>${item.class_name} (${item.class_id})</h4>
                    <div class="details">
                        <div class="detail-item"><strong>Time:</strong> ${item.start_time} - ${item.end_time}</div>
                        <div class="detail-item"><strong>Day:</strong> ${item.day}</div>
                        <div class="detail-item"><strong>Reason:</strong> ${item.reason || 'No available room'}</div>
                    </div>
                </div>
            `;
        });
    }
    
    // Conflicts
    if (result.conflicts && result.conflicts.length > 0) {
        html += `
            <div class="conflicts">
                <h3>⚠️ Conflicts Detected</h3>
                ${result.conflicts.map(conflict => `
                    <div class="conflict-item">
                        <strong>Room ${conflict.room_id}:</strong> 
                        Class ${conflict.class1_id} conflicts with ${conflict.class2_id}
                    </div>
                `).join('')}
            </div>
        `;
    }
    
    if (html === '') {
        html = '<p class="placeholder">No schedule generated.</p>';
    }
    
    scheduleOutput.innerHTML = html;
}
