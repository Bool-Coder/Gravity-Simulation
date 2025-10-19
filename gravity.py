import pygame
import math
import random

# --- Constants ---
WIDTH, HEIGHT = 1200, 800
G = 400  # gravitational constant
DT = 1 / 60
MAX_VELOCITY = 25
BORDER_THICKNESS = 5

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gravity Simulation - Add Planets")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 20)

# --- UI Colors ---
WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (180, 180, 180)
BLACK = (0, 0, 0)

# --- Planet Class ---
class Planet:
    def __init__(self, x, y, mass, radius, color):
        self.x = x
        self.y = y
        self.vx = 0.0
        self.vy = 0.0
        self.mass = mass
        self.radius = radius
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), int(self.radius))

# --- UI Input Box ---
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.txt_surface = font.render(text, True, WHITE)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = LIGHT_GRAY if self.active else GRAY
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = GRAY
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 5 and (event.unicode.isdigit() or event.unicode == '.'):
                    self.text += event.unicode
            self.txt_surface = font.render(self.text, True, WHITE)

    def draw(self):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_value(self, default):
        try:
            return float(self.text)
        except ValueError:
            return default

# --- Physics Functions ---
def apply_gravity(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    dist_sq = dx * dx + dy * dy
    if dist_sq == 0:
        return

    dist = math.sqrt(dist_sq)
    if dist > p1.radius + p2.radius + 5:
        force = G * p1.mass * p2.mass / dist_sq
        fx = force * dx / dist
        fy = force * dy / dist
        p1.vx += fx / p1.mass * DT
        p1.vy += fy / p1.mass * DT
        p2.vx -= fx / p2.mass * DT
        p2.vy -= fy / p2.mass * DT

def clamp_velocity(p):
    v = math.sqrt(p.vx ** 2 + p.vy ** 2)
    if v > MAX_VELOCITY:
        scale = MAX_VELOCITY / v
        p.vx *= scale
        p.vy *= scale

def update_position(p):
    p.x += p.vx * DT * 60
    p.y += p.vy * DT * 60

    # Bounce off borders
    if p.x - p.radius < 0:
        p.x = p.radius
        p.vx *= -0.8
    if p.x + p.radius > WIDTH:
        p.x = WIDTH - p.radius
        p.vx *= -0.8
    if p.y - p.radius < 0:
        p.y = p.radius
        p.vy *= -0.8
    if p.y + p.radius > HEIGHT:
        p.y = HEIGHT - p.radius
        p.vy *= -0.8

def handle_collision(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y
    dist = math.sqrt(dx * dx + dy * dy)
    min_dist = p1.radius + p2.radius
    if dist < min_dist and dist > 0:
        overlap = 0.5 * (min_dist - dist)
        nx = dx / dist
        ny = dy / dist
        p1.x -= nx * overlap
        p1.y -= ny * overlap
        p2.x += nx * overlap
        p2.y += ny * overlap

# --- Setup ---
planets = []
mass_box = InputBox(10, 10, 80, 30, "50")
radius_box = InputBox(100, 10, 80, 30, "10")

# --- Main Loop ---
running = True
while running:
    screen.fill(BLACK)
    dt = clock.tick(60)
    fps = clock.get_fps()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        mass_box.handle_event(event)
        radius_box.handle_event(event)

        if event.type == pygame.MOUSEBUTTONDOWN:
            if not (mass_box.rect.collidepoint(event.pos) or radius_box.rect.collidepoint(event.pos)):
                mass = mass_box.get_value(50)
                radius = radius_box.get_value(10)
                color = (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))
                planets.append(Planet(event.pos[0], event.pos[1], mass, radius, color))

    # --- Physics ---
    n = len(planets)
    # Gravity pass
    for i in range(n - 1):
        p1 = planets[i]
        for j in range(i + 1, n):
            p2 = planets[j]
            apply_gravity(p1, p2)

    # Update pass
    for p in planets:
        clamp_velocity(p)
        update_position(p)

    # Collision pass
    for i in range(n - 1):
        p1 = planets[i]
        for j in range(i + 1, n):
            handle_collision(p1, planets[j])

    # --- Draw ---
    for p in planets:
        p.draw()

    # UI
    mass_box.draw()
    radius_box.draw()
    screen.blit(font.render("Mass:", True, WHITE), (10, 45))
    screen.blit(font.render("Radius:", True, WHITE), (100, 45))
    screen.blit(font.render(f"FPS: {int(fps)}", True, WHITE), (WIDTH - 100, 10))

    pygame.display.flip()

pygame.quit()
