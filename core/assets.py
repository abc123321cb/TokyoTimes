import pygame
from functools import lru_cache

class Assets:
    def __init__(self):
        self.base = "assets"

    @lru_cache(maxsize=None)
    def image(self, path: str) -> pygame.Surface:
        return pygame.image.load(f"{self.base}/{path}").convert_alpha()

    @lru_cache(maxsize=None)
    def sound(self, path: str) -> pygame.mixer.Sound:
        return pygame.mixer.Sound(f"{self.base}/{path}")
