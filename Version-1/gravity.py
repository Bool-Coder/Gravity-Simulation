import pygame
import math
import random

WIDTH, HEIGHT = 1200, 800
G = 400
DT = 1 / 60
EPS = 2
MAX_DIST_SQ = 2000 * 2000

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Physics Engine")
clock = pygame.time.Clock()
font = pygame.font.SysFont("consolas", 18)
font2 = pygame.font.SysFont("consolas", 50)

WHITE = (255, 255, 255)
GRAY = (100, 100, 100)
LIGHT_GRAY = (180, 180, 180)
BLACK = (0, 0, 0)
GRID_COLOR = (40, 40, 40)

camera_x = 0
camera_y = 0
CAMERA_SPEED = 15
zoom = 1.0
ZOOM_SPEED = 0.1
MIN_ZOOM = 0.2
MAX_ZOOM = 5
GRID_SIZE = 100
TRAIL_LENGTH = 2000
show_trails = True
menu = True

last_camera_x = camera_x
last_camera_y = camera_y
last_zoom = zoom

grid_surface = pygame.Surface((WIDTH, HEIGHT))
grid_surface.set_colorkey((0, 0, 0))

def world_to_screen(x, y):
    sx = (x - camera_x) * zoom + WIDTH // 2
    sy = (y - camera_y) * zoom + HEIGHT // 2
    return int(sx), int(sy)

def screen_to_world(x, y):
    wx = (x - WIDTH // 2) / zoom + camera_x
    wy = (y - HEIGHT // 2) / zoom + camera_y
    return wx, wy

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

    def draw_trail(self):
        if len(self.trail) < 2:
            return

        points = []

        cx = camera_x
        cy = camera_y
        z = zoom
        hw = WIDTH // 2
        hh = HEIGHT // 2

        for wx, wy in self.trail:
            sx = int((wx - cx) * z + hw)
            sy = int((wy - cy) * z + hh)
            points.append((sx, sy))

        pygame.draw.lines(screen, self.color, False, points, 2)

    def draw(self):
        sx, sy = world_to_screen(self.x, self.y)
        pygame.draw.circle(screen, self.color, (sx, sy), max(1, int(self.radius * zoom)))

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
                if len(self.text) < 6 and (event.unicode.isdigit() or event.unicode == '.'):
                    self.text += event.unicode
            self.txt_surface = font.render(self.text, True, WHITE)

    def draw(self):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_value(self, default):
        try:
            return float(self.text)
        except:
            return default

def apply_gravity(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y

    dist_sq = dx * dx + dy * dy + EPS * EPS
    if dist_sq > MAX_DIST_SQ:
        return

    dist = math.sqrt(dist_sq)
    force = G * p1.mass * p2.mass / dist_sq

    alpha = math.atan2(dy, dx)
    fx = force * math.cos(alpha)
    fy = force * math.sin(alpha)

    p1.vx += fx / p1.mass * DT
    p1.vy += fy / p1.mass * DT
    p2.vx -= fx / p2.mass * DT
    p2.vy -= fy / p2.mass * DT

def update_position(p):
    p.x += p.vx * DT
    p.y += p.vy * DT

    if show_trails:
        p.trail.append((p.x, p.y))
        if len(p.trail) > TRAIL_LENGTH:
            p.trail.pop(0)

def redraw_grid():
    grid_surface.fill((0, 0, 0))

    top_left_x, top_left_y = screen_to_world(0, 0)
    bottom_right_x, bottom_right_y = screen_to_world(WIDTH, HEIGHT)

    start_x = int(top_left_x // GRID_SIZE * GRID_SIZE)
    start_y = int(top_left_y // GRID_SIZE * GRID_SIZE)

    x = start_x
    while x < bottom_right_x:
        sx, _ = world_to_screen(x, 0)
        pygame.draw.line(grid_surface, GRID_COLOR, (sx, 0), (sx, HEIGHT))
        x += GRID_SIZE

    y = start_y
    while y < bottom_right_y:
        _, sy = world_to_screen(0, y)
        pygame.draw.line(grid_surface, GRID_COLOR, (0, sy), (WIDTH, sy))
        y += GRID_SIZE

planets = []
def check_planet_collisions():
    for i in range(len(planets) - 1):
        for j in range(i + 1, len(planets)):
            p1 = planets[i]
            p2 = planets[j]
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            dist = math.sqrt(dx*dx + dy*dy)
            min_dist = p1.radius + p2.radius
            if dist < min_dist and dist > 0:  
                overlap = (min_dist - dist) / 2
                nx = dx / dist
                ny = dy / dist
                p1.x -= nx * overlap
                p1.y -= ny * overlap
                p2.x += nx * overlap
                p2.y += ny * overlap

def initiliaze_menu():
    planets.clear()

    p = Planet(0, 0, 5000, 50, (255, 255, 0))
    planets.append(p)

    p = Planet(0, 250, 10, 7, (255, 0, 0))
    p.vx = 60
    planets.append(p)

    p = Planet(450, 0, 15, 10, (0, 255, 0))
    p.vy = -60
    planets.append(p)

    p = Planet(0, -250, 10, 7, (0, 0, 255))
    p.vx = -60
    planets.append(p)

mass_box = InputBox(10, 10, 80, 30, "50")
radius_box = InputBox(100, 10, 80, 30, "10")

dragging = False
drag_start = (0, 0)
drag_end = (0, 0)

running = True
if menu:
    initiliaze_menu()
    redraw_grid()

while running:
    screen.fill(BLACK)
    fps = clock.get_fps()
    clock.tick(60)

    if not menu:
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            camera_x -= CAMERA_SPEED / zoom
            moved = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            camera_x += CAMERA_SPEED / zoom
            moved = True
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            camera_y -= CAMERA_SPEED / zoom
            moved = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            camera_y += CAMERA_SPEED / zoom
            moved = True

        if moved:
            redraw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if menu and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            menu = False
            planets = []
            continue

        mass_box.handle_event(event)
        radius_box.handle_event(event)

        if event.type == pygame.MOUSEWHEEL and not menu:
            zoom += event.y * ZOOM_SPEED
            zoom = max(MIN_ZOOM, min(MAX_ZOOM, zoom))
            redraw_grid()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not menu:
                planets.clear()
                camera_x = 0
                camera_y = 0
                zoom = 1.0
                redraw_grid()

            if event.key == pygame.K_q:
                show_trails = not show_trails

            if event.key == pygame.K_m or event.key == pygame.K_ESCAPE:
                camera_x = camera_y = 0
                zoom = 1.0
                menu = True
                planets.clear()
                initiliaze_menu()
                redraw_grid()
                continue

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if not (mass_box.rect.collidepoint(event.pos) or radius_box.rect.collidepoint(event.pos)):
                dragging = True
                drag_start = screen_to_world(*event.pos)
                drag_end = drag_start

        if event.type == pygame.MOUSEMOTION and dragging:
            drag_end = screen_to_world(*event.pos)

        if event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragging:
            dragging = False
            mass = mass_box.get_value(50)
            radius = radius_box.get_value(10)

            dx = drag_start[0] - drag_end[0]
            dy = drag_start[1] - drag_end[1]

            velocity_scale = 0.5
            vx = dx * velocity_scale
            vy = dy * velocity_scale

            color = (
                random.randint(120, 255),
                random.randint(120, 255),
                random.randint(120, 255),
            )

            p = Planet(drag_start[0], drag_start[1], mass, radius, color)
            p.vx = vx
            p.vy = vy
            planets.append(p)

    screen.blit(grid_surface, (0, 0))

    if menu:
        for p in planets:
            p.draw_trail()
        for p in planets:
            p.draw()
        n = len(planets)
        for i in range(n - 1):
            for j in range(i + 1, n):
                apply_gravity(planets[i], planets[j])
        for p in planets:
            update_position(p)

        screen.blit(font2.render("PHYSICS ENGINE", True, WHITE), (WIDTH / 2 - 200, 100))
        screen.blit(font.render("PRESS CLICK TO BEGIN", True, WHITE), (WIDTH / 2 - 120, 150))
        
        screen.blit(font2.render("PHYSICS ENGINE", True, WHITE), (WIDTH / 2 - 200, 100)) 
        screen.blit(font.render("PRESS CLICK TO BEGIN", True, WHITE), (WIDTH / 2 - 120, 150)) 
        screen.blit(font.render("AUTHOR: TIMOFEI FILIP EMANUEL ", True, WHITE), (30, HEIGHT - 80)) 
        screen.blit(font.render("GRADE: 8C ", True, WHITE), (30, HEIGHT - 60)) 
        screen.blit(font.render("TEACHER 1: RADU SIMONA", True, WHITE), (WIDTH - 260, HEIGHT - 80)) 
        screen.blit(font.render("TEACHER 2: DOBRIN FLORIN ", True, WHITE), (WIDTH - 260, HEIGHT - 60))
        pygame.display.flip()
        continue

    if len(planets) > 80:
        show_trails = False

    n = len(planets)
    for i in range(n - 1):
        for j in range(i + 1, n):
            apply_gravity(planets[i], planets[j])

    for p in planets:
        update_position(p)
    check_planet_collisions()
    if show_trails:
        for p in planets:
            p.draw_trail()

    for p in planets:
        p.draw()

    mass_box.draw()
    radius_box.draw()

    screen.blit(font.render("Mass kg", True, WHITE), (10, 45))
    screen.blit(font.render("Radius px", True, WHITE), (100, 45))
    screen.blit(font.render(f"FPS: {int(fps)}", True, WHITE), (WIDTH - 100, 10))
    screen.blit(font.render(f"Zoom: {zoom:.2f}", True, WHITE), (WIDTH - 100, 30))
    screen.blit(font.render("R reset", True, WHITE), (10, 85))
    screen.blit(font.render("Q orbits on/off", True, WHITE), (10, 105))
    screen.blit(font.render(f"Planets: {len(planets)}", True, WHITE), (10, 125))
    mouse_world_x, mouse_world_y = screen_to_world(*pygame.mouse.get_pos())
    pos_text = font.render(f"X: {mouse_world_x:.1f} Y: {mouse_world_y:.1f}", True, WHITE)
    screen.blit(pos_text, (10, HEIGHT - 30))  
    if dragging:
        sx1, sy1 = world_to_screen(*drag_start)
        sx2, sy2 = world_to_screen(*drag_end)
        pygame.draw.circle(screen, WHITE, (sx1, sy1), 5)
        pygame.draw.line(screen, WHITE, (sx1, sy1), (sx2, sy2), 2)

        dx = drag_start[0] - drag_end[0]
        dy = drag_start[1] - drag_end[1]
        speed = math.sqrt(dx * dx + dy * dy) * 0.5

        screen.blit(font.render(f"v = {speed:.5f} px/s", True, WHITE), (sx1 + 10, sy1 + 10))

    pygame.display.flip()

pygame.quit()