import pygame
from typing import Dict

class Input:
    def __init__(self):
        self.actions: Dict[str, int] = {
            "up": pygame.K_w,
            "down": pygame.K_s,
            "left": pygame.K_a,
            "right": pygame.K_d,
            "confirm": pygame.K_RETURN,
            "pause": pygame.K_ESCAPE,
            "inventory": pygame.K_i,
        }

    def is_action(self, event: pygame.event.Event, name: str) -> bool:
        return event.type == pygame.KEYDOWN and event.key == self.actions.get(name)
