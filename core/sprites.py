import pygame

class SpriteLoader:
    """Centralized spritesheet loader with variants and scaling.

    Usage:
      loader = SpriteLoader(game.assets)
      sheet = loader.load_sheet(path, frame_width=290, frame_height=440, variants=1)
      frame = loader.get_variant_frame(sheet, variant_index=0, scale=1.0)
    """

    def __init__(self, assets):
        self.assets = assets

    def load_sheet(self, path: str, frame_width: int, frame_height: int, variants: int = 1) -> dict:
        image = self.assets.image(path)
        cols = image.get_width() // frame_width
        rows = image.get_height() // frame_height
        frames = []
        for row in range(rows):
            row_frames = []
            for col in range(cols):
                rect = pygame.Rect(col * frame_width, row * frame_height, frame_width, frame_height)
                row_frames.append(image.subsurface(rect).copy())
            frames.append(row_frames)
        return {"image": image, "frame_width": frame_width, "frame_height": frame_height, "frames": frames, "variants": variants}

    def get_variant_frame(self, sheet: dict, variant_index: int = 0, scale: float = 1.0, mirrored: bool = False) -> pygame.Surface:
        frames = sheet["frames"]
        # For simple idle, use first row; variant selects column group when provided
        row = 0
        cols = len(frames[row])
        col = max(0, min(variant_index, cols - 1))
        frame = frames[row][col]
        if scale and scale != 1.0:
            frame = pygame.transform.scale(frame, (int(frame.get_width() * scale), int(frame.get_height() * scale)))
        if mirrored:
            frame = pygame.transform.flip(frame, True, False)
        return frame

    def slice_variant(self, image: pygame.Surface, variants: int, index: int) -> pygame.Surface:
        """Slice horizontal variants from a sheet (for props)."""
        w = image.get_width()
        h = image.get_height()
        frame_w = w // max(1, variants)
        idx = max(0, min(index, variants - 1))
        rect = pygame.Rect(idx * frame_w, 0, frame_w, h)
        surf = pygame.Surface((frame_w, h), pygame.SRCALPHA)
        surf.blit(image, (0, 0), rect)
        return surf