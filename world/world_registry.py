"""World registry for persistent NPCs and props.

These objects exist independently of scenes and persist throughout gameplay.
Scenes only contain references to which objects are currently present.
"""

from typing import Dict, List, Optional, Tuple
from entities.npc import NPC
from entities.interactables import Prop

# Global world state
_npcs: Dict[str, NPC] = {}  # npc_id -> NPC instance
_props: Dict[str, Prop] = {}  # prop_id -> Prop instance
_npc_locations: Dict[str, str] = {}  # npc_id -> current scene_name
_prop_locations: Dict[str, str] = {}  # prop_id -> current scene_name


def initialize_world(game) -> None:
    """Initialize the world with all NPCs and props.
    
    This is called once at game start, before any scenes load.
    """
    global _npcs, _props, _npc_locations, _prop_locations
    
    _npcs.clear()
    _props.clear()
    _npc_locations.clear()
    _prop_locations.clear()
    
    # Create all NPCs
    from world.world_npcs import NPCS_DEFINITION
    for npc_id, npc_def in NPCS_DEFINITION.items():
        npc = NPC(
            x=npc_def['x'],
            y=npc_def['y'],
            game=game,
            sprite_scale=npc_def.get('sprite_scale', 1.0),
            config=npc_def.get('config', None)
        )
        npc.npc_id = npc_id
        npc.npc_type = npc_def.get('type', 'henry')
        _npcs[npc_id] = npc
        _npc_locations[npc_id] = npc_def['initial_scene']
        print(f"World: Initialized NPC '{npc_id}' for scene '{npc_def['initial_scene']}'")
    
    # Create all props
    from world.world_props import PROPS_DEFINITION
    for prop_id, prop_def in PROPS_DEFINITION.items():
        prop = Prop(
            x=prop_def['x'],
            y=prop_def['y'],
            game=game,
            sprite_path=prop_def.get('sprite_path', ''),
            mask_path=prop_def.get('mask_path', None),
            name=prop_id,
            variants=prop_def.get('variants', 1),
            variant_index=prop_def.get('variant_index', 0),
            scale=prop_def.get('scale', 1.0),
            is_item=prop_def.get('is_item', False),
            item_data=prop_def.get('item_data', None),
        )
        prop.prop_id = prop_id
        _props[prop_id] = prop
        _prop_locations[prop_id] = prop_def['initial_scene']
        print(f"World: Initialized prop '{prop_id}' for scene '{prop_def['initial_scene']}'")


def get_npc(npc_id: str) -> Optional[NPC]:
    """Get an NPC by ID."""
    return _npcs.get(npc_id)


def get_prop(prop_id: str) -> Optional[Prop]:
    """Get a prop by ID."""
    return _props.get(prop_id)


def get_npcs_in_scene(scene_name: str) -> List[NPC]:
    """Get all NPCs currently in a scene."""
    npcs = [_npcs[npc_id] for npc_id in _npc_locations 
            if _npc_locations[npc_id] == scene_name and npc_id in _npcs]
    print(f"World: Found {len(npcs)} NPCs in scene '{scene_name}' (total NPCs: {len(_npcs)}, locations: {_npc_locations})")
    return npcs


def get_props_in_scene(scene_name: str) -> List[Prop]:
    """Get all props currently in a scene."""
    props = [_props[prop_id] for prop_id in _prop_locations 
            if _prop_locations[prop_id] == scene_name and prop_id in _props]
    print(f"World: Found {len(props)} props in scene '{scene_name}' (total props: {len(_props)}, locations: {_prop_locations})")
    return props


def move_npc_to_scene(npc_id: str, scene_name: str) -> None:
    """Move an NPC to a different scene."""
    if npc_id in _npc_locations:
        _npc_locations[npc_id] = scene_name


def move_prop_to_scene(prop_id: str, scene_name: str) -> None:
    """Move a prop to a different scene."""
    if prop_id in _prop_locations:
        _prop_locations[prop_id] = scene_name


def get_npc_location(npc_id: str) -> Optional[str]:
    """Get the current scene of an NPC."""
    return _npc_locations.get(npc_id)


def get_prop_location(prop_id: str) -> Optional[str]:
    """Get the current scene of a prop."""
    return _prop_locations.get(prop_id)


def get_all_npcs() -> List[NPC]:
    """Get all NPCs in the world."""
    return list(_npcs.values())


def get_all_props() -> List[Prop]:
    """Get all props in the world."""
    return list(_props.values())


def remove_npc(npc_id: str) -> None:
    """Remove an NPC from the world (e.g., if defeated or removed)."""
    if npc_id in _npcs:
        del _npcs[npc_id]
    if npc_id in _npc_locations:
        del _npc_locations[npc_id]


def remove_prop(prop_id: str) -> None:
    """Remove a prop from the world (e.g., if picked up and discarded)."""
    if prop_id in _props:
        del _props[prop_id]
    if prop_id in _prop_locations:
        del _prop_locations[prop_id]
