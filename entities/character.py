import pygame
from entities.entity import Entity

class Character(Entity):
    def __init__(self, x: float = 0, y: float = 0):
        super().__init__(x, y)
        self.speed = 120

    def update(self, dt: float) -> None:
        pass
