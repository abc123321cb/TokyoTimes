import pygame

class Entity:
    def __init__(self, x: float = 0, y: float = 0):
        self.x = x
        self.y = y
        self.rect = pygame.Rect(x, y, 32, 32)

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pygame.draw.rect(surface, (100,200,250), self.rect)
