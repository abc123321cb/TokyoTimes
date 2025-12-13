from dataclasses import dataclass

@dataclass(frozen=True)
class Layers:
    BACKGROUND: int = 0
    TERRAIN: int = 1
    ENTITIES: int = 2
    OVERLAY: int = 3
