import pygame
from settings import WIDTH, HEIGHT, GRID_COLOR, GRID_SIZE
from camera import world_to_screen, screen_to_world

grid_surface = pygame.Surface((WIDTH, HEIGHT))
grid_surface.set_colorkey((0, 0, 0))

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