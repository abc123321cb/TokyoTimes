"""Central scene registry for portal transitions."""

# Scene registry maps scene names to their classes
# Populated by scenes as they're imported
SCENE_REGISTRY = {}


def register_scene(name: str, scene_class):
    """Register a scene class with a name for portal transitions."""
    SCENE_REGISTRY[name] = scene_class


def get_scene_class(name: str):
    """Get a scene class by name."""
    return SCENE_REGISTRY.get(name)
