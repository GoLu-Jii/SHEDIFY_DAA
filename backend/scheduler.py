from typing import List, Dict, Set
from .models import ClassRequest, Classroom, Schedule

def is_overlapping(req1: ClassRequest, req2: ClassRequest) -> bool:
    """Check if two class requests overlap in time."""
    return max(req1.start_time, req2.start_time) < min(req1.end_time, req2.end_time)

def build_conflict_graph(requests: List[ClassRequest]) -> Dict[str, Set[str]]:
    """
    Builds an adjacency list representing the conflict graph.
    Nodes are request IDs, edges are drawn if requests overlap in time.
    """
    graph = {req.id: set() for req in requests}
    n = len(requests)
    for i in range(n):
        for j in range(i + 1, n):
            if is_overlapping(requests[i], requests[j]):
                graph[requests[i].id].add(requests[j].id)
                graph[requests[j].id].add(requests[i].id)
    return graph

def schedule_classes(requests: List[ClassRequest], classrooms: List[Classroom]) -> List[Schedule]:
    """
    Schedules classes using a greedy graph coloring approach.
    Colors represent individual classrooms.
    """
    graph = build_conflict_graph(requests)
    
    # Sort requests by degree in conflict graph (descending) to color most constrained first
    # This acts as our Greedy heuristic for Graph Coloring
    sorted_requests = sorted(requests, key=lambda r: (len(graph[r.id]), r.start_time), reverse=True)
    
    schedules: List[Schedule] = []
    allocation: Dict[str, str] = {} # request_id -> classroom_id
    
    # Group classrooms by type to optimize matching
    rooms_by_type = {}
    for c in classrooms:
        rooms_by_type.setdefault(c.room_type, []).append(c)
        
    classroom_map = {c.id: c for c in classrooms}
    
    for req in sorted_requests:
        # Find colors (classrooms) used by neighbors
        neighbor_rooms = set()
        for neighbor_id in graph[req.id]:
            if neighbor_id in allocation:
                neighbor_rooms.add(allocation[neighbor_id])
                
        assigned_room = None
        
        # Consider rooms matching requested type
        candidate_rooms = rooms_by_type.get(req.requested_room_type, [])
        
        # Support for specific room booking (using requested_room_type as exact room ID)
        if req.requested_room_type in classroom_map:
            candidate_rooms = [classroom_map[req.requested_room_type]]
            
        # Sort candidates by capacity ascending (Best Fit to save larger rooms)
        candidate_rooms = sorted(candidate_rooms, key=lambda c: c.capacity)
        
        for room in candidate_rooms:
            # Check availability (no adjacent node has same room) and capacity
            if room.id not in neighbor_rooms and room.capacity >= req.expected_students:
                assigned_room = room
                break
                
        # Greedy fallback: if lecture room not found, try general rooms
        if not assigned_room and req.requested_room_type == 'lecture':
            general_rooms = sorted(rooms_by_type.get('general', []), key=lambda c: c.capacity)
            for room in general_rooms:
                if room.id not in neighbor_rooms and room.capacity >= req.expected_students:
                    assigned_room = room
                    break

        if assigned_room:
            allocation[req.id] = assigned_room.id
            schedules.append(Schedule(request_id=req.id, classroom_id=assigned_room.id))
        else:
            print(f"Warning: Could not schedule Request {req.id} ({req.course_name}) - No available matching rooms.")

    return schedules
