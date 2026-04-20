from settings import WIDTH, HEIGHT

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