import pygame

class Collisions:
    @staticmethod
    def check_collision(rect: pygame.Rect, collision_rects: list[pygame.Rect]) -> bool:
        """Check if rect collides with any collision rectangles."""
        for collision_rect in collision_rects:
            if rect.colliderect(collision_rect):
                return True
        return False
    
    @staticmethod
    def get_valid_position(old_x: float, old_y: float, new_x: float, new_y: float, 
                          player_rect: pygame.Rect, collision_rects: list[pygame.Rect]) -> tuple[float, float]:
        """Return valid position, sliding along walls if needed."""
        # Create test rect at new position
        test_rect = player_rect.copy()
        test_rect.x = new_x
        test_rect.y = new_y
        
        # If no collision, allow movement
        if not Collisions.check_collision(test_rect, collision_rects):
            return new_x, new_y
        
        # Try X movement only
        test_rect.x = new_x
        test_rect.y = old_y
        if not Collisions.check_collision(test_rect, collision_rects):
            return new_x, old_y
        
        # Try Y movement only
        test_rect.x = old_x
        test_rect.y = new_y
        if not Collisions.check_collision(test_rect, collision_rects):
            return old_x, new_y
        
        # No valid movement
        return old_x, old_y
