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
    def get_valid_rect_position(old_rect: pygame.Rect, new_rect: pygame.Rect, 
                                collision_rects: list[pygame.Rect]) -> tuple[int, int]:
        """Return valid rect (x, y), sliding along walls if needed.
        Operates directly on the player's collision rect coordinates rather than sprite top-left.
        """
        # If new rect doesn't collide, accept it
        if not Collisions.check_collision(new_rect, collision_rects):
            return new_rect.x, new_rect.y

        # Try X-only movement
        test_rect = new_rect.copy()
        test_rect.x = new_rect.x
        test_rect.y = old_rect.y
        if not Collisions.check_collision(test_rect, collision_rects):
            return test_rect.x, test_rect.y

        # Try Y-only movement
        test_rect.x = old_rect.x
        test_rect.y = new_rect.y
        if not Collisions.check_collision(test_rect, collision_rects):
            return test_rect.x, test_rect.y

        # No valid movement
        return old_rect.x, old_rect.y
