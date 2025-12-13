import pygame
from typing import Any

class InventoryScene:
    def __init__(self, game: Any):
        self.game = game
        self.font = pygame.font.Font(None, 32)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_i:
            self.game.stack.pop()

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        text = self.font.render("Inventory", True, (200,255,200))
        surface.blit(text, (20,20))
