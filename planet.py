import pygame
import camera 
import random
from settings import WIDTH, HEIGHT, TRAIL_LENGTH, G
from physics import get_speed
from ui import font
from physics import *
info_panel_width = 530
info_panel_height = 200

class Planet:
    def __init__(self, x, y, mass, radius, color, id):
        self.id = id
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.mass = mass
        self.radius = radius
        self.color = color
        self.potential_energy = 0
        self.kinetic_energy = 0
        self.speed = 0
        self.object_type = ""

        self.info_rect = (0, 0, info_panel_width, info_panel_height)
        self.show_info = False
        self.info_color = (255, 255, 255)
        self.info_color_text = (0, 0, 0)
        self.trail = []

    def compute_type_of_object(self, planets):
        total_energy = self.potential_energy + self.kinetic_energy
        max_mass = max(p.mass for p in planets)
        
        type_object = None
        if self.mass == max_mass:
            type_object =  "STAR"
        elif total_energy > 0:
            type_object = "COMET"
        else: type_object = "PLANET"
        self.object_type = type_object
        

    def planet_touching_mouse(self): 
        mouse_x, mouse_y = pygame.mouse.get_pos() 
        sx, sy = camera.world_to_screen(self.x, self.y) 
        dx = mouse_x - sx 
        dy = mouse_y - sy 
        screen_radius = self.radius * camera.zoom 
        return dx * dx + dy * dy <= screen_radius * screen_radius
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            if self.planet_touching_mouse():
                self.show_info = not self.show_info
                
    
    def draw_info(self, screen):
        if not self.show_info: return

        sx, sy = camera.world_to_screen(self.x + 10, self.y + 15)
        self.info_rect = (sx, sy, info_panel_width, info_panel_height)
        pygame.draw.rect(screen, self.info_color, self.info_rect)


        screen.blit(font.render(f"Planet id: {self.id}", True, self.info_color_text), (sx + 10, sy + 1))
        screen.blit(font.render(f"Kinetic Energy: {self.kinetic_energy}", True, self.info_color_text), (sx + 10, sy + 21))
        screen.blit(font.render(f"Potential Energy: {self.potential_energy}", True, self.info_color_text), (sx + 10, sy + 41))
        screen.blit(font.render(f"Total Energy: {self.kinetic_energy + self.potential_energy}", True, self.info_color_text), (sx + 10, sy + 61))
        screen.blit(font.render(f"(vx, vy): {self.vx:1f}, {self.vy:.1f}", True, self.info_color_text), (sx + 10, sy + 81))
        screen.blit(font.render(f"Mass: {self.mass}", True, self.info_color_text), (sx + 10, sy + 101))
        screen.blit(font.render(f"Radius: {self.radius}", True, self.info_color_text), (sx + 10, sy + 121))
        screen.blit(font.render(f"(x, y): {self.x:.2f}, {self.y:2f}", True, self.info_color_text), (sx + 10, sy + 141))
        screen.blit(font.render(f"velocity: {self.speed}", True, self.info_color_text), (sx + 10, sy + 161))
        screen.blit(font.render(f"Object type: {self.object_type}", True, self.info_color_text), (sx + 10, sy + 181))

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
    def update(self, planets):
        update_energy(self, planets)
        update_position(self, show_trails)