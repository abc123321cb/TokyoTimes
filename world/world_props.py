"""Prop definitions for the world.

Each prop is defined once with their initial scene and position.
Once the game starts, they become persistent world objects that can move between scenes or be picked up.
"""

# Map of prop_id -> prop definition
# Each prop has a unique ID, sprite path, initial scene, and starting position
PROPS_DEFINITION = {
    "arcade_spaceship": {
        "sprite_path": "props/arcade_cabinet_spaceship.png",
        "mask_path": "props/arcade_cabinet_spaceship_mask.png",
        "initial_scene": "cat_cafe",
        "x": 600,
        "y": 350,
        "scale": 1.0,
    },
    "arcade_blocks": {
        "sprite_path": "props/arcade_cabinet_blocks.png",
        "mask_path": "props/arcade_cabinet_blocks_mask.png",
        "initial_scene": "cat_cafe",
        "x": 740,
        "y": 350,
        "scale": 1.0,
    },
    "cat_food_dish": {
        "sprite_path": "props/cat_food_dish.png",
        "mask_path": "props/cat_food_dish_mask.png",
        "initial_scene": "cat_cafe",
        "x": 980,
        "y": 670,
        "scale": 2.0,
        "variants": 3,
        "variant_index": 0,
        "is_item": True,
        "item_data": {
            "name": "cat_food_dish",
            "description": "A dish of cat food",
            "type": "food",
        },
    },
}


def get_props_for_scene(scene_name: str) -> list:
    """Deprecated: Use world_registry.get_props_in_scene() instead.
    
    This function is kept for backwards compatibility during migration.
    """
    from world.world_registry import get_props_in_scene
    props_in_scene = get_props_in_scene(scene_name)
    # Convert to the old format for compatibility
    return [
        {
            "name": prop.prop_id,
            "x": prop.x,
            "y": prop.y,
            "scale": getattr(prop, 'scale', 1.0),
        }
        for prop in props_in_scene
    ]

