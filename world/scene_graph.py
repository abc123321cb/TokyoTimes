"""Scene graph for cross-scene pathfinding.

This module builds a graph of scene connections based on portal definitions,
and provides algorithms to find paths between scenes.
"""

from typing import Dict, List, Tuple, Optional
from collections import deque


class SceneGraph:
    """Manages the connectivity graph of scenes via portals."""
    
    def __init__(self):
        # scene_name -> list of (portal_id, destination_scene_name, spawn_point)
        self.connections: Dict[str, List[Tuple[int, str, Tuple[float, float]]]] = {}
    
    def register_scene(self, scene_name: str, portal_map: dict):
        """Register a scene and its portal connections.
        
        Args:
            scene_name: Name of the scene
            portal_map: Dict mapping portal_id -> {to_scene, spawn}
        """
        connections = []
        for portal_id, portal_info in portal_map.items():
            to_scene = portal_info.get("to_scene")
            spawn = portal_info.get("spawn", (0, 0))
            if to_scene:
                connections.append((portal_id, to_scene, spawn))
        
        self.connections[scene_name] = connections
    
    def find_scene_path(self, from_scene: str, to_scene: str) -> Optional[List[Tuple[str, int, Tuple[float, float]]]]:
        """Find the path of scenes and portals to traverse from one scene to another.
        
        Uses BFS to find the shortest path through the scene graph.
        
        Args:
            from_scene: Starting scene name
            to_scene: Destination scene name
            
        Returns:
            List of (scene_name, portal_id, spawn_point) tuples representing the path,
            or None if no path exists.
            The first entry is the current scene with the portal to enter.
            The last entry is the destination scene (portal_id will be None).
        """
        if from_scene == to_scene:
            return [(to_scene, None, None)]
        
        if from_scene not in self.connections:
            return None
        
        # BFS to find shortest path
        queue = deque([(from_scene, [])])
        visited = {from_scene}
        
        while queue:
            current_scene, path = queue.popleft()
            
            # Check all portals from current scene
            if current_scene in self.connections:
                for portal_id, next_scene, spawn in self.connections[current_scene]:
                    if next_scene == to_scene:
                        # Found the destination!
                        result_path = path + [
                            (current_scene, portal_id, spawn),
                            (to_scene, None, None)
                        ]
                        return result_path
                    
                    if next_scene not in visited:
                        visited.add(next_scene)
                        new_path = path + [(current_scene, portal_id, spawn)]
                        queue.append((next_scene, new_path))
        
        # No path found
        return None
    
    def get_portal_to_scene(self, from_scene: str, to_scene: str) -> Optional[Tuple[int, Tuple[float, float]]]:
        """Get the portal ID to use to go directly from one scene to an adjacent scene.
        
        Args:
            from_scene: Current scene name
            to_scene: Adjacent scene name
            
        Returns:
            (portal_id, spawn_point) or None if scenes are not directly connected
        """
        if from_scene not in self.connections:
            return None
        
        for portal_id, next_scene, spawn in self.connections[from_scene]:
            if next_scene == to_scene:
                return (portal_id, spawn)
        
        return None


# Global scene graph instance
_scene_graph = SceneGraph()


def get_scene_graph() -> SceneGraph:
    """Get the global scene graph instance."""
    return _scene_graph


def register_scene_portals(scene_name: str, portal_map: dict):
    """Register a scene's portals with the global scene graph."""
    _scene_graph.register_scene(scene_name, portal_map)
