"""Central registry for prop presets and helper factory."""
from entities.interactables import Prop
from core.sprite_registry import get_sprite_config

# Add new props here; keep sprite/mask paths in one place
PROP_PRESETS = {
    "arcade_spaceship": {
        "sprite_key": "prop_arcade_spaceship",
        "variants": 1,
        "default_variant": 0,
    },
    "arcade_blocks": {
        "sprite_key": "prop_arcade_blocks",
        "variants": 1,
        "default_variant": 0,
    },
    "cat_food_dish": {
        "sprite_key": "prop_cat_food_dish",
        "variants": 3,
        "default_variant": 0,
        "scale": 2.0,
        "is_item": True,
        "item_data": {"name": "cat_food_dish", "description": "A tasty cat food dish", "sprite": "props/cat_food_dish.png"},
    },
}

def make_prop(name: str, x: float, y: float, game=None, variant_index: int = None, scale: float = None, item_id: str = None, scene_scale: float = 1.0) -> Prop:
    cfg = PROP_PRESETS.get(name)
    if not cfg:
        raise ValueError(f"Unknown prop preset: {name}")
    variants = cfg.get("variants", 1)
    default_variant = cfg.get("default_variant", 0)
    sprite_key = cfg.get("sprite_key")
    # Default scale: prop preset override, otherwise registry scale, else 1.0
    default_scale = cfg.get("scale", None)
    if default_scale is None and sprite_key:
        sprite_cfg = get_sprite_config(sprite_key)
        default_scale = sprite_cfg.get("scale", 1.0)
    if default_scale is None:
        default_scale = 1.0
    # Base scale comes from caller override or defaults; scene_scale multiplies on top
    base_scale = scale if scale is not None else default_scale
    is_item = cfg.get("is_item", False)
    item_data = cfg.get("item_data", {})
    # Resolve sprite paths from registry
    sprite_path = None
    mask_path = None
    if sprite_key:
        sprite_cfg = get_sprite_config(sprite_key)
        sprite_path = sprite_cfg.get("path")
        mask_path = sprite_cfg.get("mask_path")
    else:
        # Backward compatibility
        sprite_path = cfg.get("sprite")
        mask_path = cfg.get("mask")
    if variant_index is None:
        variant_index = default_variant
    if scale is None:
        scale = default_scale
    
    # Generate item_id if this is an item and no id provided
    final_item_id = item_id
    if is_item and not final_item_id:
        # Default ID format: name:x:y
        final_item_id = f"{name}:{int(x)}:{int(y)}"
    
    return Prop(
        x=x,
        y=y,
        sprite_path=sprite_path,
        mask_path=mask_path,
        game=game,
        name=name,
        variants=variants,
        variant_index=variant_index,
        scale=base_scale,
        scene_scale=scene_scale,
        is_item=is_item,
        item_data=item_data,
        item_id=final_item_id
    )
