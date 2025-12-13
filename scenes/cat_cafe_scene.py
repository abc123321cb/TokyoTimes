import pygame
from typing import Any

class CatCafeScene:
    def __init__(self, game: Any):
        self.game = game
        try:
            self.background = game.assets.image("backgrounds/cat_cafe.jpg")
        except Exception as e:
            print(f"Warning: Could not load cat cafe background: {e}")
            self.background = None
        self.font = pygame.font.Font(None, 24)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from scenes.inventory_scene import InventoryScene
                self.game.stack.push(InventoryScene(self.game))

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        if self.background:
            surface.blit(self.background, (0, 0))
        else:
            surface.fill((139, 69, 19))  #Fallback brown color
        
        surface.blit(self.font.render("Cat Cafe (ESC for inventory)", True, (255, 255, 255)), (8, 8))
