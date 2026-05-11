from settings import *
import pygame
camera_x = 0
camera_y = 0
zoom = 1.0

def world_to_screen(x, y):
    sx = (x - camera_x) * zoom + WIDTH // 2
    sy = (y - camera_y) * zoom + HEIGHT // 2
    return int(sx), int(sy)

def screen_to_world(x, y):
    wx = (x - WIDTH // 2) / zoom + camera_x
    wy = (y - HEIGHT // 2) / zoom + camera_y
    return wx, wy
def reset_camera():
    camera_x = 0
    camera_y = 0
    zoom = 1.0
def follow(target_x, target_y, speed=0.1):
    pass
def move_camera():
    global camera_x, camera_y
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

    return moved
def zoom_camera(event):
    global zoom
    zoom += event.y * ZOOM_SPEED
    zoom = max(MIN_ZOOM, min(MAX_ZOOM, zoom))
    return True