import pygame
from typing import Any
from entities.player import Player
from world.camera import Camera
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

class CatCafeScene:
    def __init__(self, game: Any):
        self.game = game
        try:
            self.background = game.assets.image("backgrounds/cat_cafe.jpg")
        except Exception as e:
            print(f"Warning: Could not load cat cafe background: {e}")
            self.background = None
        self.font = pygame.font.Font(None, 24)
        
        # Get world dimensions from background or use defaults
        if self.background:
            self.world_width = self.background.get_width()
            self.world_height = self.background.get_height()
        else:
            self.world_width = WINDOW_WIDTH
            self.world_height = WINDOW_HEIGHT
        
        # Create camera and player
        self.camera = Camera(WINDOW_WIDTH, WINDOW_HEIGHT)
        self.player = Player(x=self.world_width // 2, y=self.world_height // 2, game=game)
        
        # Define collision rectangles for cat cafe (1536x1024 background)
        self.collision_rects = [
            # Walls
            pygame.Rect(0, 0, self.world_width, 80),  # Top wall
            pygame.Rect(0, self.world_height - 80, self.world_width, 80),  # Bottom wall
            pygame.Rect(0, 0, 80, self.world_height),  # Left wall
            pygame.Rect(self.world_width - 80, 0, 80, self.world_height),  # Right wall
            
            # Counter area (typical cafe counter on left or right side)
            pygame.Rect(100, 100, 300, 150),  # Top left counter
            
            # Tables and furniture (adjust these based on your actual background)
            pygame.Rect(500, 300, 120, 120),  # Table 1
            pygame.Rect(800, 300, 120, 120),  # Table 2
            pygame.Rect(1100, 300, 120, 120),  # Table 3
            pygame.Rect(500, 600, 120, 120),  # Table 4
            pygame.Rect(800, 600, 120, 120),  # Table 5
            pygame.Rect(1100, 600, 120, 120),  # Table 6
        ]
        self.player.collision_rects = self.collision_rects

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                from scenes.inventory_scene import InventoryScene
                self.game.stack.push(InventoryScene(self.game))

    def update(self, dt: float) -> None:
        self.player.update(dt)
        # Camera follows player but respects world bounds
        self.camera.follow(self.player.x, self.player.y, self.world_width, self.world_height)

    def draw(self, surface: pygame.Surface) -> None:
        # Draw background at camera offset
        if self.background:
            bg_x, bg_y = self.camera.apply(0, 0)
            surface.blit(self.background, (bg_x, bg_y))
        else:
            surface.fill((139, 69, 19))
        
        # Draw collision rectangles for debugging
        for rect in self.collision_rects:
            screen_x, screen_y = self.camera.apply(rect.x, rect.y)
            pygame.draw.rect(surface, (255, 0, 0), (screen_x, screen_y, rect.width, rect.height), 2)
        
        # Draw player at camera-relative position
        player_screen_x, player_screen_y = self.camera.apply(self.player.x, self.player.y)
        temp_surface = pygame.Surface((self.player.sprite.get_width(), self.player.sprite.get_height()), pygame.SRCALPHA)
        self.player.sprite and temp_surface.blit(self.player.sprite, (0, 0))
        surface.blit(temp_surface, (player_screen_x, player_screen_y))
        
        # Draw player collision rect for debugging
        if hasattr(self.player, 'collision_rect'):
            coll_x, coll_y = self.camera.apply(
                self.player.collision_rect.x - 72,  # Offset back from center
                self.player.collision_rect.y - 200 + self.player.collision_rect.height  # Offset back from bottom
            )
            pygame.draw.rect(surface, (0, 255, 0), 
                           (coll_x, coll_y, self.player.collision_rect.width, self.player.collision_rect.height), 2)
        
        surface.blit(self.font.render("Cat Cafe (ESC for inventory)", True, (255, 255, 255)), (8, 8))
