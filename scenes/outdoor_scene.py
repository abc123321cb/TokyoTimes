import pygame
from typing import Any
from scenes.base_scene import MaskedScene
from scenes.scene_registry import register_scene


# Portal mapping will be filled when portals are defined in the mask
PORTAL_MAP = {
    0: {        # ?
        "to_scene": "arcade",
        "spawn": (257, 380),
    },
    1: {        # cat cafe
        "to_scene": "cat_cafe",
        "spawn": (217, 411),
    },
    2: {        # arcade
        "to_scene": "arcade",
        "spawn": (257, 380),
    },
    3: {        # ?
        "to_scene": "arcade",
        "spawn": (257, 380),
    },
    4: {        # convenience store
        "to_scene": "arcade",
        "spawn": (257, 380),
    },
    5: {        # ?
        "to_scene": "arcade",
        "spawn": (257, 380),
    },
    6: {    # street-left
        "to_scene": "outdoor",
        "spawn": (1480, 750),
    },
    7: {    # street-right
        "to_scene": "outdoor",
        "spawn": (61, 750),
    },
}


class OutdoorScene(MaskedScene):
    BACKGROUND_PATH = "backgrounds/outdoor.jpg"
    PORTAL_MAP = PORTAL_MAP
    SCENE_NAME = "outdoor"
    SCENE_SCALE = 0.4

    def __init__(self, game: Any, spawn: tuple = None):
        super().__init__(game, spawn)

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        surface.blit(self.font.render("Outdoor", True, (255, 255, 255)), (8, 8))


# Register this scene
register_scene("outdoor", OutdoorScene)
