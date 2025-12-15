import pygame
from entities.character import Character
from entities.components.animation import Spritesheet, Animation
from core.sprites import SpriteLoader
from core.sprite_registry import get_sprite_config

class NPC(Character):
    def __init__(self, x: float, y: float, game=None, sprite_scale: float = 1.0):
        self.game = game
        self.animation = None
        self.spritesheet = None
        sprite = None
        self.direction = "down"
        self.animations = {}
        # Default scale: provided or registry default
        if sprite_scale is None and game:
            try:
                sprite_scale = get_sprite_config("npc_henry").get("scale", 1.0)
            except Exception:
                sprite_scale = 1.0
        self.sprite_scale = sprite_scale if sprite_scale is not None else 1.0

        # Load Henry spritesheet (same layout as player: 3x3 frames of 290x440)
        if game:
            try:
                loader = SpriteLoader(game.assets)
                henry_cfg = get_sprite_config("npc_henry")
                sheet_img = game.assets.image(henry_cfg["path"]) 
                self.spritesheet = Spritesheet(sheet_img, frame_width=henry_cfg["frame_width"], frame_height=henry_cfg["frame_height"]) 
                # Idle animations similar to player
                self.animations["down"] = self._create_animation([0, 1, 0, 2])
                self.animations["up"] = self._create_animation([3, 4, 3, 5])
                self.animations["left"] = self._create_animation([6, 7, 6, 8])
                self.animations["right"] = self._create_animation_mirrored([6, 7, 6, 8])
                self.animation = self.animations["down"]
                sprite = self.animation.get_current_frame()
            except Exception as e:
                print(f"Warning: Could not load henry spritesheet: {e}")
                sprite = pygame.Surface((290, 440))
                sprite.fill((200, 170, 120))

        super().__init__(x, y, sprite)
        # NPCs don't move by default
        self.velocity_x = 0
        self.velocity_y = 0

    def _create_animation(self, frame_indices: list) -> Animation:
        anim = Animation(self.spritesheet, fps=6, scale=self.sprite_scale)
        anim.frame_indices = frame_indices
        return anim

    def _create_animation_mirrored(self, frame_indices: list) -> Animation:
        anim = Animation(self.spritesheet, fps=6, scale=self.sprite_scale)
        anim.frame_indices = frame_indices
        anim.mirrored = True
        return anim

    def update(self, dt: float) -> None:
        # Update idle animation
        if self.animation:
            self.animation.update(dt)
            self.sprite = self.animation.get_current_frame()
        # Update rect position
        if self.sprite:
            if not hasattr(self, 'rect') or self.rect is None:
                self.rect = self.sprite.get_rect(topleft=(self.x, self.y))
            else:
                self.rect.topleft = (self.x, self.y)
