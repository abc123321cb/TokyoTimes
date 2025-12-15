import pygame
import math
from entities.character import Character
from entities.components.animation import Spritesheet, Animation
from core.sprites import SpriteLoader
from core.sprite_registry import get_sprite_config
from ai.pathfinding import Pathfinding

class NPC(Character):
    def __init__(self, x: float, y: float, game=None, sprite_scale: float = 1.0):
        self.game = game
        self.animation = None
        self.spritesheet = None
        sprite = None
        self.direction = "down"
        self.animations = {}
        # Default scale: provided or registry default
        if sprite_scale is None and game:
            try:
                sprite_scale = get_sprite_config("npc_henry").get("scale", 1.0)
            except Exception:
                sprite_scale = 1.0
        self.sprite_scale = sprite_scale if sprite_scale is not None else 1.0

        # Load Henry spritesheet (same layout as player: 3x3 frames of 290x440)
        if game:
            try:
                loader = SpriteLoader(game.assets)
                henry_cfg = get_sprite_config("npc_henry")
                sheet_img = game.assets.image(henry_cfg["path"]) 
                self.spritesheet = Spritesheet(sheet_img, frame_width=henry_cfg["frame_width"], frame_height=henry_cfg["frame_height"]) 
                # Idle animations (single frame - first pose of each direction)
                self.idle_animations = {}
                self.idle_animations["down"] = self._create_animation([0])
                self.idle_animations["up"] = self._create_animation([3])
                self.idle_animations["right"] = self._create_animation([6])
                self.idle_animations["left"] = self._create_animation_mirrored([6])
                # Moving animations (cycling frames)
                self.moving_animations = {}
                self.moving_animations["down"] = self._create_animation([0, 1, 0, 2])
                self.moving_animations["up"] = self._create_animation([3, 4, 3, 5])
                self.moving_animations["right"] = self._create_animation([6, 7, 6, 8])
                self.moving_animations["left"] = self._create_animation_mirrored([6, 7, 6, 8])
                # Start with idle down
                self.animation = self.idle_animations["down"]
                sprite = self.animation.get_current_frame()
            except Exception as e:
                print(f"Warning: Could not load henry spritesheet: {e}")
                sprite = pygame.Surface((290, 440))
                sprite.fill((200, 170, 120))

        super().__init__(x, y, sprite)
        # NPCs don't move by default
        self.velocity_x = 0
        self.velocity_y = 0
        
        # Pathfinding
        self.pathfinder = Pathfinding(cell_size=20)
        self.path = []  # Current path waypoints (list of (x, y) tuples)
        self.current_waypoint_idx = 0
        self.speed = 100  # pixels per second
        self.mask_system = None  # Will be set by scene
        self.destination = None  # Target destination (x, y) for re-pathfinding
        self.stuck_timer = 0.0  # Time spent not making progress
        self.last_position = (x, y)  # Track position for stuck detection
        self.repath_interval = 2.0  # Re-pathfind every N seconds if moving
        self.repath_timer = 0.0

    def _create_animation(self, frame_indices: list) -> Animation:
        anim = Animation(self.spritesheet, fps=6, scale=self.sprite_scale)
        anim.frame_indices = frame_indices
        return anim

    def _create_animation_mirrored(self, frame_indices: list) -> Animation:
        anim = Animation(self.spritesheet, fps=6, scale=self.sprite_scale)
        anim.frame_indices = frame_indices
        anim.mirrored = True
        return anim

    def update(self, dt: float) -> None:
        # Determine if moving
        is_moving = self.path and self.current_waypoint_idx < len(self.path)
        
        # Check if stuck or need to re-path
        if is_moving and self.destination:
            # Check if stuck (not making progress)
            current_pos = (self.x, self.y)
            distance_moved = math.sqrt((current_pos[0] - self.last_position[0])**2 + 
                                     (current_pos[1] - self.last_position[1])**2)
            
            if distance_moved < 1.0:  # Less than 1 pixel moved
                self.stuck_timer += dt
                if self.stuck_timer > 0.5:  # Stuck for more than 0.5 seconds
                    print(f"NPC stuck, re-pathfinding to {self.destination}")
                    self.pathfind_to(self.destination[0], self.destination[1])
                    self.stuck_timer = 0.0
            else:
                self.stuck_timer = 0.0
            
            self.last_position = current_pos
            
            # Periodic re-pathfinding to handle dynamic obstacles
            self.repath_timer += dt
            if self.repath_timer >= self.repath_interval:
                self.repath_timer = 0.0
                # Re-pathfind to destination
                if self.destination:
                    self.pathfind_to(self.destination[0], self.destination[1])
        
        # Choose animation based on movement state
        if is_moving:
            # Use moving animation for current direction
            self.animation = self.moving_animations.get(self.direction, self.idle_animations.get(self.direction))
        else:
            # Use idle animation (single frame)
            self.animation = self.idle_animations.get(self.direction, self.idle_animations.get("down"))
        
        # Update animation frame
        if self.animation:
            self.animation.update(dt)
            self.sprite = self.animation.get_current_frame()
        
        # Update rect position
        if self.sprite:
            if not hasattr(self, 'rect') or self.rect is None:
                self.rect = self.sprite.get_rect(topleft=(self.x, self.y))
            else:
                self.rect.topleft = (self.x, self.y)
        
        # Follow path if one exists
        if self.path and self.current_waypoint_idx < len(self.path):
            self._follow_path(dt)
    
    def pathfind_to(self, target_x: float, target_y: float) -> None:
        """Pathfind from current position to target using A* algorithm."""
        if not self.mask_system:
            print("Warning: NPC has no mask_system, cannot pathfind")
            return
        
        # Store destination for re-pathfinding
        self.destination = (target_x, target_y)
        self.stuck_timer = 0.0
        self.repath_timer = 0.0
        
        # Define walkable function: a position is walkable if it's not colliding
        def is_walkable(x, y):
            # Check if position is blocked by collision mask
            walkable = self.mask_system.is_walkable(int(x), int(y))
            if not walkable:
                return False
            
            # Check props (if they have collision)
            if hasattr(self, 'props') and self.props:
                for prop in self.props:
                    if not getattr(prop, 'picked_up', False):
                        prop_scale = getattr(prop, 'scale', 1.0)
                        if hasattr(prop, 'sprite') and prop.sprite:
                            bbox = prop.sprite.get_bounding_rect(min_alpha=1)
                            scaled_width = int(bbox.width * prop_scale)
                            scaled_height = int(bbox.height * prop_scale)
                            prop_rect = pygame.Rect(
                                int(prop.x + bbox.x * prop_scale),
                                int(prop.y + bbox.y * prop_scale),
                                scaled_width,
                                scaled_height
                            )
                            check_rect = pygame.Rect(int(x) - 5, int(y) - 5, 10, 10)
                            if check_rect.colliderect(prop_rect):
                                return False
            
            return True
        
        # If start is not walkable, try to find a nearby walkable position
        if not is_walkable(self.x, self.y):
            print(f"Start position ({self.x}, {self.y}) not walkable, searching nearby...")
            found_start = False
            for offset_x in range(-50, 51, 10):
                for offset_y in range(-50, 51, 10):
                    test_x = self.x + offset_x
                    test_y = self.y + offset_y
                    if is_walkable(test_x, test_y):
                        print(f"Found walkable position at ({test_x}, {test_y})")
                        self.x = test_x
                        self.y = test_y
                        found_start = True
                        break
                if found_start:
                    break
            if not found_start:
                print(f"Could not find walkable start position!")
                return
        
        # Calculate path using A*
        world_width = 1920  # Default; can be made dynamic
        world_height = 1080
        if hasattr(self, 'scene') and hasattr(self.scene, 'world_width'):
            world_width = self.scene.world_width
            world_height = self.scene.world_height
        
        self.path = self.pathfinder.astar(
            is_walkable,
            (self.x, self.y),
            (target_x, target_y),
            (world_width, world_height)
        )
        self.current_waypoint_idx = 0
        if self.path:
            print(f"NPC pathfinding to ({target_x}, {target_y}): found {len(self.path)} waypoints")
        else:
            print(f"NPC pathfinding to ({target_x}, {target_y}): no path found")
    
    def _follow_path(self, dt: float) -> None:
        """Move along the current path."""
        if self.current_waypoint_idx >= len(self.path):
            self.path = []
            self.current_waypoint_idx = 0
            return
        
        target = self.path[self.current_waypoint_idx]
        dx = target[0] - self.x
        dy = target[1] - self.y
        distance = math.sqrt(dx**2 + dy**2)
        
        # Update direction based on movement
        if abs(dx) > abs(dy):
            self.direction = "right" if dx > 0 else "left"
        else:
            self.direction = "down" if dy > 0 else "up"
        
        # If close enough to waypoint, move to next
        if distance < 5:
            self.current_waypoint_idx += 1
            return
        
        # Move towards waypoint
        if distance > 0:
            move_distance = self.speed * dt
            if move_distance >= distance:
                self.x = target[0]
                self.y = target[1]
                self.current_waypoint_idx += 1
            else:
                self.x += (dx / distance) * move_distance
                self.y += (dy / distance) * move_distance
