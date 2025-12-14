"""Central registry for prop presets and helper factory."""
from entities.interactables import Prop

# Add new props here; keep sprite/mask paths in one place
PROP_PRESETS = {
    "arcade_spaceship": {
        "sprite": "props/arcade_cabinet_spaceship.png",
        "mask": "props/arcade_cabinet_spaceship_mask.png",
    },
    "arcade_blocks": {
        "sprite": "props/arcade_cabinet_blocks.png",
        "mask": "props/arcade_cabinet_blocks_mask.png",
    },
}

def make_prop(name: str, x: float, y: float, game=None) -> Prop:
    cfg = PROP_PRESETS.get(name)
    if not cfg:
        raise ValueError(f"Unknown prop preset: {name}")
    return Prop(
        x=x,
        y=y,
        sprite_path=cfg.get("sprite"),
        mask_path=cfg.get("mask"),
        game=game,
        name=name,
    )
