"""Conflict detection utilities."""

from typing import List, Dict
from backend.models.class_request import ClassRequest


class ConflictDetector:
    """Detect conflicts between class requests."""
    
    @staticmethod
    def detect_all_conflicts(class_requests: List[ClassRequest]) -> List[Dict]:
        """
        Detect all potential conflicts in class requests.
        
        A conflict exists if two classes overlap in time.
        This is used for graph coloring representation where:
        - Each class is a node
        - An edge exists between overlapping classes
        - Each color represents a classroom
        """
        conflicts = []
        
        for i, class1 in enumerate(class_requests):
            for class2 in class_requests[i + 1:]:
                if class1.overlaps_with(class2):
                    conflicts.append({
                        "class1": class1,
                        "class2": class2,
                        "overlap_type": "time_overlap"
                    })
        
        return conflicts
    
    @staticmethod
    def build_conflict_graph(class_requests: List[ClassRequest]) -> Dict[str, List[str]]:
        """
        Build a conflict graph where:
        - Nodes are class IDs
        - Edges connect overlapping classes
        
        Returns adjacency list representation.
        """
        graph: Dict[str, List[str]] = {req.class_id: [] for req in class_requests}
        
        for i, class1 in enumerate(class_requests):
            for class2 in class_requests[i + 1:]:
                if class1.overlaps_with(class2):
                    graph[class1.class_id].append(class2.class_id)
                    graph[class2.class_id].append(class1.class_id)
        
        return graph
    
    @staticmethod
    def get_minimum_rooms_needed(class_requests: List[ClassRequest]) -> int:
        """
        Estimate minimum rooms needed using graph coloring concept.
        This gives a lower bound for the number of rooms required.
        """
        if not class_requests:
            return 0
        
        graph = ConflictDetector.build_conflict_graph(class_requests)
        
        # Simple greedy coloring to estimate minimum rooms
        # This is a heuristic, not optimal
        colors: Dict[str, int] = {}
        max_color = 0
        
        for class_id in sorted(graph.keys()):
            # Find available colors (not used by neighbors)
            used_colors = {colors[neighbor] for neighbor in graph[class_id] 
                          if neighbor in colors}
            
            # Assign smallest available color
            color = 0
            while color in used_colors:
                color += 1
            
            colors[class_id] = color
            max_color = max(max_color, color)
        
        return max_color + 1  # Colors are 0-indexed, so +1 for count
