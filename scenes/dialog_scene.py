import pygame
from typing import Any

class DialogScene:
    def __init__(self, game: Any, lines: list[str]):
        self.game = game
        self.lines = lines
        self.font = pygame.font.Font(None, 28)

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_RETURN, pygame.K_ESCAPE):
            self.game.stack.pop()

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        y = surface.get_height() - 120
        pygame.draw.rect(surface, (0,0,0), (0, y, surface.get_width(), 120))
        pygame.draw.rect(surface, (255,255,255), (0, y, surface.get_width(), 120), 2)
        for i, line in enumerate(self.lines[:3]):
            surface.blit(self.font.render(line, True, (255,255,255)), (16, y + 16 + i*28))
