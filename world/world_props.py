"""Central world-level prop registry defining all props and their initial placements per scene."""

# Map of scene_name -> list of prop definitions
# Each prop definition includes the name (from prop_registry), position, and optional overrides
WORLD_PROPS = {
    "cat_cafe": [
        {
            "name": "arcade_spaceship",
            "x": 600,
            "y": 350,
        },
        {
            "name": "arcade_blocks",
            "x": 740,
            "y": 350,
        },
        {
            "name": "cat_food_dish",
            "x": 850,
            "y": 650,
            "scale": 2.0,  # Item-level scale override
        },
    ],
    "cat_cafe_kitchen": [
        # No initial props in the kitchen
    ],
}


def get_props_for_scene(scene_name: str) -> list:
    """Get the list of prop definitions for a given scene."""
    return WORLD_PROPS.get(scene_name, [])
