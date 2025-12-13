import pygame
from typing import Any

class ArcadeBase:
    def __init__(self, game: Any):
        self.game = game

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass
