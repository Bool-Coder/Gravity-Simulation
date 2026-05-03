import pygame
import camera 
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

        self.info_color = (255, 255, 255)
        self.info_color_text = (0, 0, 0)
        self.info = "Info Planet"

        self.info_rect = (0, 0, 100, 100)
    
    def planet_touching_mouse(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        dx = mouse_x - self.x
        dy = mouse_y - self.y
        return (dx * dx + dy * dy <= self.radius * self.radius)
    def draw_info(self, screen):
        if not self.planet_touching_mouse(): return

        sx, sy = camera.world_to_screen(self.x + 10, self.y + 15)
        self.info_rect = (sx, sy, 150, 150)
        pygame.draw.rect(screen, self.info_color, self.info_rect)
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
            max(1, int(self.radius * camera.zoom)) 
        )