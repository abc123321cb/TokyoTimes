"""Central registry for sprite metadata (frame sizes, variants, paths)."""

SPRITE_REGISTRY = {
    # Characters
    "player_girl": {
        "path": "sprites/girl.png",
        "frame_width": 290,
        "frame_height": 440,
        "rows": 3,
        "cols": 3,
        "variants": 1,
        "scale": 0.5,
    },
    "npc_henry": {
        "path": "sprites/henry.png",
        "frame_width": 290,
        "frame_height": 440,
        "rows": 3,
        "cols": 3,
        "variants": 1,
        "scale": 0.5,
    },

    # Props with horizontal variants
    "prop_cat_food_dish": {
        "path": "props/cat_food_dish.png",
        "mask_path": "props/cat_food_dish_mask.png",
        "variants": 3,
        "scale": 2.0,
    },
    "prop_arcade_spaceship": {
        "path": "props/arcade_cabinet_spaceship.png",
        "mask_path": "props/arcade_cabinet_spaceship_mask.png",
        "variants": 1,
        "scale": 1.0,
    },
    "prop_arcade_blocks": {
        "path": "props/arcade_cabinet_blocks.png",
        "mask_path": "props/arcade_cabinet_blocks_mask.png",
        "variants": 1,
        "scale": 1.0,
    },
}

def get_sprite_config(key: str) -> dict:
    cfg = SPRITE_REGISTRY.get(key)
    if not cfg:
        raise KeyError(f"Sprite config not found for key: {key}")
    return cfg