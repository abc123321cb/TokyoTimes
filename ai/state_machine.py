import random
import math

class State:
    """Base class for NPC states."""
    def __init__(self, npc):
        self.npc = npc
        self.time_in_state = 0.0
    
    def enter(self):
        """Called when entering this state."""
        self.time_in_state = 0.0
    
    def exit(self):
        """Called when exiting this state."""
        pass
    
    def update(self, dt: float) -> str:
        """Update state logic. Returns name of next state or None to stay in current state."""
        self.time_in_state += dt
        return None
    
    def get_name(self) -> str:
        """Get the name of this state."""
        return self.__class__.__name__


class IdleState(State):
    """NPC stands still for a duration."""
    def __init__(self, npc):
        super().__init__(npc)
        # Get config from NPC
        config = getattr(npc, 'config', None)
        self.min_duration = config.idle_min_duration if config else 2.0
        self.max_duration = config.idle_max_duration if config else 5.0
        self.wander_probability = config.wander_probability if config else 0.65
        self.travel_probability = config.travel_probability if config else 0.10
        self.duration = random.uniform(self.min_duration, self.max_duration)
    
    def enter(self):
        super().enter()
        # Pick a random idle duration
        self.duration = random.uniform(self.min_duration, self.max_duration)
        # Stop any current movement
        self.npc.path = []
        self.npc.current_waypoint_idx = 0
        self.npc.destination = None
    
    def update(self, dt: float) -> str:
        super().update(dt)
        
        # After idle duration, decide on next state
        if self.time_in_state >= self.duration:
            rand = random.random()
            if rand < self.wander_probability:
                return "WanderState"
            elif rand < self.wander_probability + self.travel_probability:
                return "TravelToSceneState"
            else:
                # Idle again
                self.enter()
        
        return None


class WanderState(State):
    """NPC walks to a random nearby location within the current scene."""
    def __init__(self, npc):
        super().__init__(npc)
        # Get config from NPC
        config = getattr(npc, 'config', None)
        self.wander_radius = config.wander_radius if config else 200.0
        self.max_wander_time = config.max_wander_time if config else 10.0
        self.portal_min_distance = config.wander_portal_min_distance if config else 50.0
    
    def enter(self):
        super().enter()
        
        # Try to find a valid walkable target point in current scene
        max_attempts = 20
        target_x, target_y = None, None
        
        # Get feet position as reference point for wander calculations
        feet_x, feet_y = self.npc._get_feet_position()
        
        for attempt in range(max_attempts):
            # Pick a random point near current position
            angle = random.uniform(0, 2 * 3.14159)
            distance = random.uniform(50, self.wander_radius)
            test_x = feet_x + distance * math.cos(angle)
            test_y = feet_y + distance * math.sin(angle)
            
            # Check if this point is walkable
            if not (self.npc.mask_system and self.npc.mask_system.is_walkable(int(test_x), int(test_y))):
                continue
            
            # Check if point is in or too close to a portal
            is_too_close_to_portal = False
            if self.npc.mask_system:
                # Check if directly in a portal
                if self.npc.mask_system.is_portal(int(test_x), int(test_y)) is not None:
                    continue
                
                # Check distance to all portal regions
                for portal_id in self.npc.mask_system.portal_regions:
                    portal_bounds = self.npc.mask_system.get_portal_bounds(portal_id)
                    if portal_bounds:
                        # Calculate distance to closest point in portal bounds
                        portal_center_x = (portal_bounds.left + portal_bounds.right) / 2
                        portal_center_y = (portal_bounds.top + portal_bounds.bottom) / 2
                        dist_to_portal = math.sqrt((test_x - portal_center_x)**2 + (test_y - portal_center_y)**2)
                        
                        if dist_to_portal < self.portal_min_distance:
                            is_too_close_to_portal = True
                            break
                
                if is_too_close_to_portal:
                    continue
            
            # This point is valid - not in portal and not too close
            target_x, target_y = test_x, test_y
            break
        
        # If found a valid target, pathfind to it
        if target_x is not None:
            self.npc.pathfind_to(target_x, target_y, avoid_portals=True)
        else:
            # No valid point found - will immediately transition back to idle
            self.npc.path = []
    
    def update(self, dt: float) -> str:
        super().update(dt)
        
        # Check if reached destination
        has_path = self.npc.path and self.npc.current_waypoint_idx < len(self.npc.path)
        
        if not has_path or self.time_in_state >= self.max_wander_time:
            # Finished wandering or gave up - return to idle
            return "IdleState"
        
        return None


class TravelToSceneState(State):
    """NPC decides to travel to a different scene."""
    def __init__(self, npc):
        super().__init__(npc)
        # Get config from NPC
        config = getattr(npc, 'config', None)
        self.max_travel_time = config.max_travel_time if config else 30.0
    
    def enter(self):
        super().enter()
        # Pick a random connected scene to travel to
        if hasattr(self.npc, 'scene') and hasattr(self.npc.scene, 'PORTAL_MAP'):
            portals = list(self.npc.scene.PORTAL_MAP.values())
            if portals:
                target_portal = random.choice(portals)
                target_scene = target_portal.get('to_scene')
                if target_scene:
                    print(f"NPC traveling to different scene: {target_scene}")
                    self.npc.pathfind_to_scene(target_scene)
                    return
        
        # No valid scene found - path will be empty
        self.npc.path = []
    
    def update(self, dt: float) -> str:
        super().update(dt)
        
        # Check if still traveling
        has_path = self.npc.path and self.npc.current_waypoint_idx < len(self.npc.path)
        has_scene_path = self.npc.scene_path and self.npc.current_scene_step < len(self.npc.scene_path)
        
        if (not has_path and not has_scene_path) or self.time_in_state >= self.max_travel_time:
            # Finished traveling or gave up - return to idle
            return "IdleState"
        
        return None


class StateMachine:
    """Manages NPC state transitions."""
    def __init__(self, npc, initial_state_name="IdleState"):
        self.npc = npc
        self.states = {}
        self.current_state = None
        self.current_state_name = None
        
        # Register default states
        self.register_state("IdleState", IdleState(npc))
        self.register_state("WanderState", WanderState(npc))
        self.register_state("TravelToSceneState", TravelToSceneState(npc))
        
        # Set initial state
        self.set_state(initial_state_name)
    
    def register_state(self, name: str, state: State):
        """Register a new state by name."""
        self.states[name] = state
    
    def set_state(self, state_name: str):
        """Transition to a new state."""
        if state_name not in self.states:
            print(f"Warning: State '{state_name}' not registered")
            return
        
        # Exit current state
        if self.current_state:
            self.current_state.exit()
        
        # Enter new state
        self.current_state = self.states[state_name]
        self.current_state_name = state_name
        self.current_state.enter()
    
    def update(self, dt: float):
        """Update the current state."""
        if not self.current_state:
            return
        
        # Update current state and check for transition
        next_state = self.current_state.update(dt)
        if next_state:
            self.set_state(next_state)
    
    def get_current_state_name(self) -> str:
        """Get the name of the current state."""
        return self.current_state_name
