"""NPC definitions for the world.

Each NPC is defined once with their initial scene and position.
Once the game starts, they become persistent world objects that can move between scenes.
"""

from entities.npc_configs import HENRY_CONFIG

# Map of npc_id -> NPC definition
# Each NPC has a unique ID, type, initial scene, and starting position
NPCS_DEFINITION = {
    "henry": {
        "type": "henry",
        "initial_scene": "cat_cafe",
        "x": 400,
        "y": 720,
        "sprite_scale": 0.5,
        "config": HENRY_CONFIG,
    },
    # Add more NPCs here as you create them
    # "sarah": {
    #     "type": "sarah",
    #     "initial_scene": "cat_cafe_kitchen_scene",
    #     "x": 500,
    #     "y": 600,
    #     "sprite_scale": 1.0,
    #     "config": LAZY_CONFIG,
    # },
}


def get_npcs_for_scene(scene_name: str) -> list:
    """Deprecated: Use world_registry.get_npcs_in_scene() instead.
    
    This function is kept for backwards compatibility during migration.
    """
    from world.world_registry import get_npcs_in_scene
    npcs_in_scene = get_npcs_in_scene(scene_name)
    # Convert to the old format for compatibility
    return [
        {
            "type": npc.npc_type,
            "x": npc.x,
            "y": npc.y,
        }
        for npc in npcs_in_scene
    ]

