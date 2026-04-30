import pygame
import math
import random
from button import Button

from settings import *
import camera
from planet import Planet
from physics import apply_gravity, update_position, update_collisions
from grid import grid_surface, redraw_grid
from ui import InputBox, font
from menu import initialize_menu

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GRAVICODE")
clock = pygame.time.Clock()
font2 = pygame.font.SysFont("consolas", 50)

planets = []
buttons = []
mass_box = InputBox(10, 10, 80, 30, "50")
radius_box = InputBox(100, 10, 80, 30, "10")

dragging = False
drag_start = (0, 0)
drag_end = (0, 0)

show_trails = True

scene = "MENU"

def go_to_menu():
    camera.camera_x = camera.camera_y = 0
    camera.zoom = 1.0
    global scene
    scene = "MENU"
    planets.clear()
    buttons.clear()
    initialize_menu(planets, buttons, screen, set_scene)
    redraw_grid()

def set_scene(new_scene):
    global scene
    planets.clear()
    buttons.clear()
    if new_scene != "MENU":
        menu_button = Button(screen, WIDTH - 75, HEIGHT - 35, 60, 25, lambda: go_to_menu(), "MENU", (0, 0, 0), WHITE, font)
        buttons.append(menu_button)
    scene = new_scene


initialize_menu(planets, buttons, screen, set_scene)
for button in buttons: button.screen = screen
redraw_grid()

running = True
while running:
    screen.fill(BLACK)
    fps = clock.get_fps()
    clock.tick(60)
    

    if scene != "MENU":
        keys = pygame.key.get_pressed()
        moved = False

        if keys[pygame.K_a] or keys[pygame.K_LEFT]:
            camera.camera_x -= CAMERA_SPEED / camera.zoom
            moved = True
        if keys[pygame.K_d] or keys[pygame.K_RIGHT]:
            camera.camera_x += CAMERA_SPEED / camera.zoom
            moved = True
        if keys[pygame.K_w] or keys[pygame.K_UP]:
            camera.camera_y -= CAMERA_SPEED / camera.zoom
            moved = True
        if keys[pygame.K_s] or keys[pygame.K_DOWN]:
            camera.camera_y += CAMERA_SPEED / camera.zoom
            moved = True

        if moved:
            redraw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        pressed = False 
        for button in buttons: pressed = button.check_if_pressed(event)
        if scene == "MENU":
            pass
        elif scene == "SIMULATION":   
            mass_box.handle_event(event)
            radius_box.handle_event(event)

            if event.type == pygame.MOUSEWHEEL and scene != "MENU":
                camera.zoom += event.y * ZOOM_SPEED
                camera.zoom = max(MIN_ZOOM, min(MAX_ZOOM, camera.zoom))
                redraw_grid()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and scene != "MENU":
                    planets.clear()
                    camera.camera_x = 0
                    camera.camera_y = 0
                    camera.zoom = 1.0
                    redraw_grid()

                if event.key == pygame.K_q:
                    show_trails = not show_trails

            if scene == "SIMULATION" and event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if not (mass_box.rect.collidepoint(event.pos) or radius_box.rect.collidepoint(event.pos)):
                    dragging = True
                    drag_start = camera.screen_to_world(*event.pos)
                    drag_end = drag_start

            if scene == "SIMULATION" and event.type == pygame.MOUSEMOTION and dragging:
                drag_end = camera.screen_to_world(*event.pos)

            if scene == "SIMULATION" and event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragging:
                dragging = False

                mass = mass_box.get_value(50)
                radius = radius_box.get_value(10)

                dx = drag_start[0] - drag_end[0]
                dy = drag_start[1] - drag_end[1]

                vx = dx * 0.5
                vy = dy * 0.5

                color = (
                    random.randint(120, 255),
                    random.randint(120, 255),
                    random.randint(120, 255),
                )

                p = Planet(drag_start[0], drag_start[1], mass, radius, color, len(planets) + 1)
                p.vx = vx
                p.vy = vy
                planets.append(p)

    screen.blit(grid_surface, (0, 0))
    for button in buttons:
        button.update()
        button.draw()

    
    if scene == "MENU":
        screen.blit(font2.render("GRAVICODE", True, WHITE), (WIDTH / 2 - 120, 100))        
        screen.blit(font.render("AUTHOR: TIMOFEI FILIP EMANUEL -> 8C", True, WHITE), (30, HEIGHT - 60))
        screen.blit(font.render("AUTHOR: BUNGHEZ ANDREI -> 6C ", True, WHITE), (30, HEIGHT - 40))
        screen.blit(font.render("TEACHER 1: RADU SIMONA", True, WHITE), (WIDTH - 260, HEIGHT - 80))
        screen.blit(font.render("TEACHER 2: DOBRIN FLORIN ", True, WHITE), (WIDTH - 260, HEIGHT - 60))
        screen.blit(font.render("TEACHER 3: MEMET EDEN ", True, WHITE), (WIDTH - 260, HEIGHT - 40))

        pygame.display.flip()
        continue
    elif scene == "SIMULATION":

        if len(planets) > 80:
            show_trails = False

        for i in range(len(planets) - 1):
            for j in range(i + 1, len(planets)):
                apply_gravity(planets[i], planets[j])

        for p in planets:
            update_position(p, show_trails)
        
        update_collisions(planets)
        if show_trails:
            for p in planets:
                p.draw_trail(screen)
        for p in planets:

            p.draw(screen)
            p.draw_info(screen)


        # 🔹 UI BOXES
        mass_box.draw(screen)
        radius_box.draw(screen)

        # 🔹 LABELS (restored)
        screen.blit(font.render("Mass kg", True, WHITE), (10, 45))
        screen.blit(font.render("Radius px", True, WHITE), (100, 45))
        screen.blit(font.render(f"FPS: {int(fps)}", True, WHITE), (WIDTH - 100, 10))
        screen.blit(font.render(f"Zoom: {camera.zoom:.2f}", True, WHITE), (WIDTH - 100, 30))
        screen.blit(font.render("R reset", True, WHITE), (10, 85))
        screen.blit(font.render("Q orbits on/off", True, WHITE), (10, 105))
        screen.blit(font.render(f"Planets: {len(planets)}", True, WHITE), (10, 125))

        mouse_world_x, mouse_world_y = camera.screen_to_world(*pygame.mouse.get_pos())
        pos_text = font.render(f"X: {mouse_world_x:.1f} Y: {mouse_world_y:.1f}", True, WHITE)
        screen.blit(pos_text, (10, HEIGHT - 30))

        
        if dragging:
            sx1, sy1 = camera.world_to_screen(*drag_start)
            sx2, sy2 = camera.world_to_screen(*drag_end)

            pygame.draw.circle(screen, WHITE, (sx1, sy1), 5)
            pygame.draw.line(screen, WHITE, (sx1, sy1), (sx2, sy2), 2)

            dx = drag_start[0] - drag_end[0]
            dy = drag_start[1] - drag_end[1]
            speed = math.sqrt(dx * dx + dy * dy) * 0.5

            screen.blit(font.render(f"v = {speed:.5f} px/s", True, WHITE), (sx1 + 10, sy1 + 10))

    pygame.display.flip()

pygame.quit()