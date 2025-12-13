"""Cat Cafe scene geometry - collision rects, portals, and spawn points."""
import pygame

# Wall and furniture dimensions
WALL_THICKNESS = 80
DOORWAY_TOP = 420
DOORWAY_HEIGHT = 140

# Furniture positions (x, y, width, height)
COUNTER_RECT = (100, 100, 300, 150)
TABLE_RECTS = [
    (500, 300, 120, 120),   # Table 1

    (1100, 600, 120, 120),  # Table 6
]

# Portal spawn point in kitchen when entering from cafe
PORTAL_TO_KITCHEN_SPAWN = (200, 500)


def get_collision_rects(world_width: int, world_height: int):
    """Build collision rectangles for the cat cafe scene."""
    rects = [
        # Walls (with doorway gap on right wall)
        pygame.Rect(0, 0, world_width, WALL_THICKNESS),  # Top
        pygame.Rect(0, world_height - WALL_THICKNESS, world_width, WALL_THICKNESS),  # Bottom
        pygame.Rect(0, 0, WALL_THICKNESS, world_height),  # Left
        pygame.Rect(world_width - WALL_THICKNESS, 0, WALL_THICKNESS, DOORWAY_TOP),  # Right top
        pygame.Rect(world_width - WALL_THICKNESS, DOORWAY_TOP + DOORWAY_HEIGHT, 
                   WALL_THICKNESS, world_height - (DOORWAY_TOP + DOORWAY_HEIGHT)),  # Right bottom
        
        # Furniture
        pygame.Rect(*COUNTER_RECT),
    ]
    # Add tables
    rects.extend(pygame.Rect(*table) for table in TABLE_RECTS)
    return rects


def get_portals(world_width: int, world_height: int):
    """Build portal definitions for the cat cafe scene."""
    return [
        {
            "rect": pygame.Rect(world_width - WALL_THICKNESS, DOORWAY_TOP, 
                              WALL_THICKNESS, DOORWAY_HEIGHT),
            "to_scene": "cat_cafe_kitchen",
            "spawn": PORTAL_TO_KITCHEN_SPAWN,
        }
    ]
