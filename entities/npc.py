import pygame
from entities.character import Character
from entities.components.animation import Spritesheet, Animation
import pygame
from core.sprites import SpriteLoader
from core.sprite_registry import get_sprite_config
from ai.pathfinding import Pathfinding

class NPC(Character):
    def __init__(self, x: float, y: float, game=None, sprite_scale: float = 1.0):
        self.game = game
        self.animation = None
        self.spritesheet = None
        sprite = None
        self.direction = "down"
        self.animations = {}
        self.sprite_scale = sprite_scale

        # Load Henry spritesheet (same layout as player: 3x3 frames of 290x440)
        if game:
            try:
                loader = SpriteLoader(game.assets)
                henry_cfg = get_sprite_config("npc_henry")
                sheet_img = game.assets.image(henry_cfg["path"]) 
                self.spritesheet = Spritesheet(sheet_img, frame_width=henry_cfg["frame_width"], frame_height=henry_cfg["frame_height"]) 
                # Idle animations similar to player
                # Rows: 1=down, 2=up, 3=right; left mirrors right
                self.animations["down"] = self._create_animation([0, 1, 0, 2])
                self.animations["up"] = self._create_animation([3, 4, 3, 5])
                self.animations["right"] = self._create_animation([6, 7, 6, 8])
                self.animations["left"] = self._create_animation_mirrored([6, 7, 6, 8])
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
        self.path: list[tuple[int,int]] = []
        self.path_index = 0
        self.speed = 100
        self.base_speed = 100
        self.pathfinder = Pathfinding(cell_size=20)

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
        moving = False
        # Update rect position
        if self.sprite:
            if not hasattr(self, 'rect') or self.rect is None:
                self.rect = self.sprite.get_rect(topleft=(self.x, self.y))
            else:
                self.rect.topleft = (self.x, self.y)

        # Follow path if present
        if self.path and self.path_index < len(self.path):
            tx, ty = self.path[self.path_index]
            import math
            dx = tx - self.x
            dy = ty - self.y
            dist = math.hypot(dx, dy)
            if dist < 4:
                self.path_index += 1
            else:
                dirx = dx / dist
                diry = dy / dist
                self.x += dirx * self.speed * dt
                self.y += diry * self.speed * dt
                if abs(dirx) > abs(diry):
                    self.direction = "right" if dirx > 0 else "left"
                else:
                    self.direction = "down" if diry > 0 else "up"
                if self.direction in self.animations:
                    self.animation = self.animations[self.direction]
                moving = True

        # If path finished, stop movement/animation
        if not self.path or self.path_index >= len(self.path):
            self.speed = 0

        # Animate only when moving; idle shows first variant
        if self.animation:
            if moving:
                self.animation.update(dt)
            else:
                self.animation.current_frame = 0
            self.sprite = self.animation.get_current_frame()

    def set_destination(self, goal: tuple[int,int], scene) -> None:
        """Compute a path to goal using scene collision for walkability."""
        def walkable_fn(wx, wy):
            # Build a small collision rect like player's feet
            rect = pygame.Rect(0,0, scene.PLAYER_HITBOX_WIDTH or 40, scene.PLAYER_HITBOX_HEIGHT or 20)
            rect.centerx = int(wx)
            rect.bottom = int(wy)
            room_block = scene.mask_system.rect_collides(rect) if scene.mask_system else False
            # Check props collision reusing player's method if available
            if hasattr(scene.player, '_rect_collides_with_props'):
                props_block = scene.player._rect_collides_with_props(rect)
            else:
                props_block = False
            return not room_block and not props_block

        bounds = (scene.world_width, scene.world_height)
        start = (int(self.x), int(self.y))
        # Reset speed for new travel
        self.speed = self.base_speed
        path = self.pathfinder.astar(walkable_fn, start, goal, bounds)
        self.path = path
        self.path_index = 0
        try:
            print(f"NPC path planned from {start} to {goal}: {len(self.path)} nodes")
        except Exception:
            pass
