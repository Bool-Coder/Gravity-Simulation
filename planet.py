import pygame
import camera  # 🔴 import the module, not the values
from settings import WIDTH, HEIGHT, TRAIL_LENGTH

class Planet:
    def __init__(self, x, y, mass, radius, color):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.mass = mass
        self.radius = radius
        self.color = color
        self.trail = []

    def draw_trail(self, screen):
        if len(self.trail) < 2:
            return

        points = []
        cx = camera.camera_x
        cy = camera.camera_y
        z = camera.zoom
        hw = WIDTH // 2
        hh = HEIGHT // 2

        for wx, wy in self.trail:
            sx = int((wx - cx) * z + hw)
            sy = int((wy - cy) * z + hh)
            points.append((sx, sy))

        pygame.draw.lines(screen, self.color, False, points, 2)

    def draw(self, screen):
        sx, sy = camera.world_to_screen(self.x, self.y)
        pygame.draw.circle(
            screen,
            self.color,
            (sx, sy),
            max(1, int(self.radius * camera.zoom))  # 🔴 live zoom
        )