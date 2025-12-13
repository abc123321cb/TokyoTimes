import pygame
from typing import Any
from core.scene import Scene

class TitleScene:
    def __init__(self, game: Any):
        self.game = game
        self.title_font = pygame.font.Font(None, 64)
        self.menu_font = pygame.font.Font(None, 36)
        self.options = ["Start", "Save", "Load", "Exit"]
        self.selected = 0

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_DOWN, pygame.K_s):
                self.selected = (self.selected + 1) % len(self.options)
            elif event.key in (pygame.K_UP, pygame.K_w):
                self.selected = (self.selected - 1) % len(self.options)
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                self._activate_option()
            elif event.key == pygame.K_ESCAPE:
                self.game.quit()

    def _activate_option(self) -> None:
        choice = self.options[self.selected].lower()
        if choice == "start":
            from scenes.world_scene import WorldScene
            self.game.stack.push(WorldScene(self.game))
        elif choice == "save":
            self.game.saves.save("slot1", {"room": "room_001"}, {"seen_intro": True})
        elif choice == "load":
            run, knowledge = self.game.saves.load("slot1")
            from scenes.world_scene import WorldScene
            self.game.stack.push(WorldScene(self.game))
        elif choice == "exit":
            self.game.quit()

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        rect = surface.get_rect()
        title = self.title_font.render("Tokyo Times", True, (255,255,255))
        title_pos = (rect.centerx - title.get_width() // 2, rect.top + 120)
        surface.blit(title, title_pos)

        start_y = title_pos[1] + title.get_height() + 40
        for i, opt in enumerate(self.options):
            sel = (i == self.selected)
            color = (255,255,0) if sel else (200,200,200)
            marker = "> " if sel else "  "
            text = self.menu_font.render(f"{marker}{opt}", True, color)
            x = rect.centerx - text.get_width() // 2
            y = start_y + i * 40
            surface.blit(text, (x, y))
