"""Load and extract collision masks from mask images."""
import pygame
from typing import Dict, List


class CollisionMaskExtractor:
    """Extracts per-frame collision bounding boxes from a mask image."""
    
    def __init__(self, mask_image: pygame.Surface, variants: int, frame_width: int, frame_height: int):
        """
        Args:
            mask_image: Pygame surface with white pixels indicating collision areas
            variants: Number of frames per row
            frame_width: Width of each frame
            frame_height: Height of each frame
        """
        self.mask_image = mask_image
        self.variants = variants
        self.frame_width = frame_width
        self.frame_height = frame_height
        self.frame_masks = self._extract_frame_masks()
    
    def _extract_frame_masks(self) -> Dict[int, pygame.Rect]:
        """Extract one bounding box from the first frame and reuse for all.

        All character/NPC sprite sheets now provide a mask where only the first
        frame (top-left) contains the white collision region. We compute that
        bounding box once and apply it to every frame index so animation frames
        share a consistent hitbox.
        """
        frame_masks: Dict[int, pygame.Rect] = {}
        rows = self.mask_image.get_height() // self.frame_height

        # Use the first frame (row 0, col 0) as the source of truth
        base_box = self._find_white_box(0, 0)

        # Apply the same box to every frame in the sheet
        for row in range(rows):
            for col in range(self.variants):
                frame_idx = row * self.variants + col
                frame_masks[frame_idx] = base_box.copy()

        return frame_masks
    
    def _find_white_box(self, start_x: int, start_y: int) -> pygame.Rect:
        """Find bounding box of white pixels in a frame region (white = collision area)."""
        min_x, max_x = self.frame_width, 0
        min_y, max_y = self.frame_height, 0
        found_white = False
        
        for y in range(start_y, start_y + self.frame_height):
            for x in range(start_x, start_x + self.frame_width):
                if x < self.mask_image.get_width() and y < self.mask_image.get_height():
                    color = self.mask_image.get_at((x, y))
                    # Check if pixel is white (collision area)
                    if color[0] > 200 and color[1] > 200 and color[2] > 200:
                        found_white = True
                        local_x = x - start_x
                        local_y = y - start_y
                        min_x = min(min_x, local_x)
                        max_x = max(max_x, local_x)
                        min_y = min(min_y, local_y)
                        max_y = max(max_y, local_y)
        
        if found_white:
            width = max_x - min_x + 1
            height = max_y - min_y + 1
            return pygame.Rect(min_x, min_y, width, height)
        else:
            # Default: reasonable hitbox for sprite (roughly center-bottom, humanoid shape)
            # For a 290x440 frame: hitbox in lower body area
            center_x = self.frame_width // 2
            bottom_y = int(self.frame_height * 0.8)  # 80% down the frame
            hitbox_width = 100
            hitbox_height = 150
            return pygame.Rect(center_x - hitbox_width // 2, bottom_y - hitbox_height, hitbox_width, hitbox_height)
    
    def get_frame_collision_box(self, frame_idx: int) -> pygame.Rect:
        """Get the collision box (relative to frame origin) for a frame."""
        return self.frame_masks.get(frame_idx, pygame.Rect(0, 0, 50, 50))
