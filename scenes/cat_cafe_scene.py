import pygame
from typing import Any
from scenes.base_scene import MaskedScene
from scenes.scene_registry import register_scene


# Portal mapping: portal_id (from white regions in mask) -> scene configuration
# To find portal IDs, run the game with debug enabled and check console output
PORTAL_MAP = {
    0: {
        "to_scene": "cat_cafe_kitchen",
        "spawn": (1085, 400),
    },
    1: {
        "to_scene": "cat_cafe_kitchen",
        "spawn": (1085, 400),
    },
}


class CatCafeScene(MaskedScene):
    BACKGROUND_PATH = "backgrounds/cat_cafe.jpg"
    PORTAL_MAP = PORTAL_MAP
    
    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        surface.blit(self.font.render("Cat Cafe (ESC for inventory)", True, (255, 255, 255)), (8, 8))


# Register this scene
register_scene("cat_cafe", CatCafeScene)
