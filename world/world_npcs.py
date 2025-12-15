"""Central world-level NPC registry defining all NPCs and their initial placements per scene."""

# Map of scene_name -> list of NPC definitions
# Each NPC definition includes the NPC type/class and position
WORLD_NPCS = {
    "cat_cafe": [
        {
            "type": "henry",
            "x": 400,
            "y": 650,
            "destination": (1250, 450),  # Optional: NPC will pathfind to this location when scene loads
            # Optional: "sprite_scale": 0.5  (defaults to scene PLAYER_SPRITE_SCALE)
        },
    ],
    "cat_cafe_kitchen": [
        # No NPCs in the kitchen
    ],
}


def get_npcs_for_scene(scene_name: str) -> list:
    """Get the list of NPC definitions for a given scene."""
    return WORLD_NPCS.get(scene_name, [])
