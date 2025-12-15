import pygame
from typing import Any
from scenes.base_scene import MaskedScene
from scenes.scene_registry import register_scene


# Portal mapping: portal_id (from white regions in mask) -> scene configuration
PORTAL_MAP = {
    0: {
        "to_scene": "cat_cafe",
        "spawn": (650, 850),
    },
}


class CatCafeKitchenScene(MaskedScene):
    BACKGROUND_PATH = "backgrounds/cat_cafe_kitchen.jpg"
    PORTAL_MAP = PORTAL_MAP
    SCENE_NAME = "cat_cafe_kitchen"
    SCENE_SCALE = 1.1
    
    def __init__(self, game: Any, spawn: tuple = None):
        super().__init__(game, spawn)
        
        # Update player's prop reference if player exists
        if hasattr(self, 'player'):
            self.player.props = self.props
    
    def draw(self, surface: pygame.Surface) -> None:
        super().draw(surface)
        surface.blit(self.font.render("Kitchen (ESC for inventory)", True, (255, 255, 255)), (8, 8))


# Register this scene
register_scene("cat_cafe_kitchen", CatCafeKitchenScene)
