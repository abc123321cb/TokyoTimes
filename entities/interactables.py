import pygame


class Interactable:
    def __init__(self, rect):
        self.rect = rect

    def interact(self, actor):
        pass


class Prop:
    """Generic prop with sprite + mask.
    Black pixels in mask = walkable; transparent/other = blocked (collision handled in player).
    """

    def __init__(self, x: float, y: float, sprite_path: str, mask_path: str = None, game=None, name: str = None):
        self.x = x
        self.y = y
        self.name = name
        self.game = game
        self.sprite = None
        self.mask = None

        if game and sprite_path:
            try:
                self.sprite = game.assets.image(sprite_path)
            except Exception as e:
                print(f"Warning: Could not load prop sprite {sprite_path}: {e}")
                self.sprite = pygame.Surface((64, 64))
                self.sprite.fill((120, 120, 120))

        if game and mask_path:
            try:
                self.mask = game.assets.image(mask_path)
            except Exception as e:
                print(f"Warning: Could not load prop mask {mask_path}: {e}")

        if self.sprite:
            self.rect = self.sprite.get_rect(topleft=(x, y))
        else:
            self.rect = pygame.Rect(x, y, 64, 64)

    def update(self, dt: float) -> None:
        pass

    def draw(self, surface: pygame.Surface, camera=None) -> None:
        if self.sprite:
            if camera:
                screen_x, screen_y = camera.apply(self.x, self.y)
            else:
                screen_x, screen_y = self.x, self.y
            surface.blit(self.sprite, (screen_x, screen_y))
        else:
            pygame.draw.rect(surface, (120, 120, 120), self.rect)

    def depth(self) -> float:
        """Return depth (y) used for sorting. Uses visible sprite bounds to ignore transparent extensions."""
        if self.sprite:
            # bounding_rect is relative to surface; bottom gives visible height ignoring full transparency
            bbox = self.sprite.get_bounding_rect(min_alpha=1)
            return self.y + bbox.bottom
        elif self.rect:
            return self.rect.bottom
        return self.y
