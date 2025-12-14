import pygame
import random
import math
from settings import WINDOW_WIDTH, WINDOW_HEIGHT

class AsteroidsState:
    def __init__(self):
        self.width = int(WINDOW_WIDTH * 0.8)
        self.height = int(WINDOW_HEIGHT * 0.7)
        self.player = {
            "x": self.width // 2,
            "y": self.height // 2,
            "angle": 0.0,
            "vx": 0.0,
            "vy": 0.0,
        }
        self.shots = []
        self.asteroids = self._spawn_asteroids(6)
        self.thrust = 160.0
        self.turn_speed = 180.0
        self.friction = 0.98
        self.shot_speed = 300.0
        self.game_over = False
        self.fire_cooldown = 0.2
        self._fire_timer = 0.0

    def _spawn_asteroids(self, count):
        ast = []
        for _ in range(count):
            ax = random.randint(20, self.width - 20)
            ay = random.randint(20, self.height - 20)
            avx = random.uniform(-60, 60)
            avy = random.uniform(-60, 60)
            radius = random.randint(26, 34)
            ast.append({"x": ax, "y": ay, "vx": avx, "vy": avy, "r": radius, "size": 3})
        return ast

    def handle_key(self, key):
        if self.game_over:
            return
        if key in (pygame.K_a, pygame.K_LEFT):
            self.player["angle"] -= self.turn_speed / 60.0
        elif key in (pygame.K_d, pygame.K_RIGHT):
            self.player["angle"] += self.turn_speed / 60.0
        elif key in (pygame.K_w, pygame.K_UP):
            import math
            rad = math.radians(self.player["angle"])
            self.player["vx"] += math.cos(rad) * (self.thrust / 60.0)
            self.player["vy"] += math.sin(rad) * (self.thrust / 60.0)
        elif key in (pygame.K_SPACE,):
            import math
            rad = math.radians(self.player["angle"])
            sx = self.player["x"]
            sy = self.player["y"]
            svx = math.cos(rad) * self.shot_speed
            svy = math.sin(rad) * self.shot_speed
            self.shots.append({"x": sx, "y": sy, "vx": svx, "vy": svy, "life": 1.5})

    def _handle_held_input(self, dt):
        if self.game_over:
            return
        keys = pygame.key.get_pressed()
        import math
        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            self.player["angle"] -= self.turn_speed * dt
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            self.player["angle"] += self.turn_speed * dt
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            rad = math.radians(self.player["angle"])
            self.player["vx"] += math.cos(rad) * (self.thrust * dt)
            self.player["vy"] += math.sin(rad) * (self.thrust * dt)
        # Held-fire with cooldown
        self._fire_timer -= dt
        if self._fire_timer < 0:
            self._fire_timer = 0
        if keys[pygame.K_SPACE] and self._fire_timer == 0:
            rad = math.radians(self.player["angle"])
            sx = self.player["x"]
            sy = self.player["y"]
            svx = math.cos(rad) * self.shot_speed
            svy = math.sin(rad) * self.shot_speed
            self.shots.append({"x": sx, "y": sy, "vx": svx, "vy": svy, "life": 1.25})
            self._fire_timer = self.fire_cooldown

    def update(self, dt):
        if self.game_over:
            return
        # Continuous input while keys are held
        self._handle_held_input(dt)
        self.player["x"] += self.player["vx"] * dt
        self.player["y"] += self.player["vy"] * dt
        self.player["vx"] *= self.friction
        self.player["vy"] *= self.friction
        self.player["x"] %= self.width
        self.player["y"] %= self.height
        for s in self.shots:
            s["x"] += s["vx"] * dt
            s["y"] += s["vy"] * dt
            s["life"] -= dt
        self.shots = [s for s in self.shots if s["life"] > 0]
        for a in self.asteroids:
            a["x"] += a["vx"] * dt
            a["y"] += a["vy"] * dt
            a["x"] %= self.width
            a["y"] %= self.height
        # Shots vs asteroids with splitting
        new_asteroids = []
        for a in self.asteroids:
            hit_by = None
            for s in self.shots:
                dx = s["x"] - a["x"]
                dy = s["y"] - a["y"]
                if dx*dx + dy*dy <= a["r"]*a["r"]:
                    hit_by = s
                    break
            if hit_by:
                hit_by["life"] = 0
                # Split if not at smallest size
                if a.get("size", 1) > 1:
                    # Create two smaller fragments
                    child_size = a["size"] - 1
                    child_radius = {3: 24, 2: 16, 1: 10}[child_size]
                    # Randomized scatter velocities
                    ang1 = random.uniform(0, 6.283)
                    ang2 = ang1 + random.uniform(1.0, 2.5)
                    spd = random.uniform(60, 120)
                    vx1 = spd * math.cos(ang1)
                    vy1 = spd * math.sin(ang1)
                    vx2 = spd * math.cos(ang2)
                    vy2 = spd * math.sin(ang2)
                    new_asteroids.append({"x": a["x"], "y": a["y"], "vx": vx1, "vy": vy1, "r": child_radius, "size": child_size})
                    new_asteroids.append({"x": a["x"], "y": a["y"], "vx": vx2, "vy": vy2, "r": child_radius, "size": child_size})
                # else: destroyed, no children
            else:
                new_asteroids.append(a)
        self.asteroids = new_asteroids
        if not self.asteroids:
            self.game_over = True
        for a in self.asteroids:
            dx = self.player["x"] - a["x"]
            dy = self.player["y"] - a["y"]
            if dx*dx + dy*dy <= (a["r"]+10)*(a["r"]+10):
                self.game_over = True
                break

    def draw(self, surface: pygame.Surface, x: int, y: int, w: int, h: int, font: pygame.font.Font):
        px = x + (w - self.width) // 2
        py = y + (h - self.height) // 2
        pygame.draw.rect(surface, (5, 5, 20), (px, py, self.width, self.height))
        for i in range(60):
            sx = px + (i * 37 % self.width)
            sy = py + (i * 53 % self.height)
            surface.fill((255, 255, 255), (sx, sy, 1, 1))
        for a in self.asteroids:
            pygame.draw.circle(surface, (140, 140, 140), (int(px + a["x"]), int(py + a["y"])), a["r"], 0)
            pygame.draw.circle(surface, (90, 90, 90), (int(px + a["x"]), int(py + a["y"])), a["r"], 2)
        for s in self.shots:
            surface.fill((255, 200, 120), (int(px + s["x"])-2, int(py + s["y"])-2, 4, 4))
        import math
        rad = math.radians(self.player["angle"])
        cx = px + self.player["x"]
        cy = py + self.player["y"]
        nose = (cx + math.cos(rad) * 12, cy + math.sin(rad) * 12)
        left = (cx + math.cos(rad + math.pi*0.75) * 10, cy + math.sin(rad + math.pi*0.75) * 10)
        right = (cx + math.cos(rad - math.pi*0.75) * 10, cy + math.sin(rad - math.pi*0.75) * 10)
        pygame.draw.polygon(surface, (120, 220, 255), [nose, left, right])
        title = font.render("Spaceship Arcade (ESC to exit)", True, (255, 255, 255))
        surface.blit(title, (x + 20, y + 20))
        hint = font.render("W/UP thrust, A/D turn, SPACE shoot", True, (200, 200, 200))
        surface.blit(hint, (x + 20, y + 50))
        if self.game_over:
            over = font.render("You Win! (ESC)", True, (120, 255, 160)) if not self.asteroids else font.render("Game Over (ESC)", True, (255, 120, 120))
            surface.blit(over, (x + 20, y + 80))
