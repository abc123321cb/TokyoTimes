import pygame
from typing import Any
from scenes.base_scene import MaskedScene
from scenes.scene_registry import register_scene


# Portal mapping will be filled when portals are defined in the mask
PORTAL_MAP = {
    0: {
        "to_scene": "outdoor",
        "spawn": (795, 530),
    },
}


class ArcadeScene(MaskedScene):
    BACKGROUND_PATH = "backgrounds/acrade.jpg"  # Uses existing asset name
    PORTAL_MAP = PORTAL_MAP
    SCENE_NAME = "arcade"
    SCENE_SCALE = 1.0

    def __init__(self, game: Any, spawn: tuple = None):
        super().__init__(game, spawn)

    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        surface.blit(self.font.render("Arcade", True, (255, 255, 255)), (8, 8))


# Register this scene
register_scene("arcade", ArcadeScene)
