from backend.models import Schedule


# conflict graph tells overlapping class requests 
def build_conflict_graph(requests):
    # create empty graph
    graph = {}
    for req in requests:
        graph[req.id] = set()
    
    # build graph via overlap check
    n = len(requests)
    for i in range(n):
        for j in range(i + 1, n):
            req1 = requests[i]
            req2 = requests[j]
            start = max(req1.start_time, req2.start_time)
            end = min(req1.end_time, req2.end_time)
            if(start < end):
                graph[req1.id].add(req2.id)
                graph[req2.id].add(req1.id)
    return graph


# class schedule engine
def schedule_classes(requests, classrooms):

    graph = build_conflict_graph(requests)

    # sort based on number of conflicts and start time 
    def sort_key(req):
        conflicts = len(graph[req.id])
        start = req.start_time
        return (conflicts, start)
    sorted_requests = sorted(requests, key=sort_key, reverse=True)

    
    schedules = []   # final list of scheduled classes
    allocation = {}  # keeps track of assigned requests
    
    # Group classrooms by type (lab or lecture)
    rooms_by_type = {}
    for c in classrooms:
        room_type = c.room_type

        if(room_type not in rooms_by_type):
            rooms_by_type[room_type] = []

        rooms_by_type[room_type].append(c)


    
    for req in sorted_requests:

        available_rooms = []

        # find rooms already used by neighbors
        neighbor_rooms = set()
        for neighbor in graph[req.id]:
            if(neighbor in allocation):
                neighbor_rooms.add(allocation[neighbor])
                
        assigned_room = None    # acts as a flag: none means "room not assigned"
        
        # get room by type for current request
        candidate_rooms = rooms_by_type.get(req.requested_room_type, [])
        
        # Sort candidates by capacity ascending
        candidate_rooms = sorted(candidate_rooms, key=lambda c: c.capacity)
        
        for room in candidate_rooms:
            # Check availability and capacity
            if room.id not in neighbor_rooms and room.capacity >= req.expected_students:
                available_rooms.append(room)
                if not assigned_room:
                    assigned_room = room
                

        if assigned_room:
            allocation[req.id] = assigned_room.id
            schedules.append(Schedule(request_id=req.id, classroom_id=assigned_room.id))
        else:
            print(f"Warning: Could not schedule Request {req.id} ({req.course_name}) - No available matching rooms.")

    return schedules
