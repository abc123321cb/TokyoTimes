import pygame
from typing import Any

class PauseScene:
    def __init__(self, game: Any):
        self.game = game
        self.font = pygame.font.Font(None, 36)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.stack.pop()

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        text = self.font.render("Paused - ESC to resume", True, (255,255,0))
        rect = text.get_rect(center=surface.get_rect().center)
        surface.blit(text, rect)
