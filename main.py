import pygame
import random
from open_simulation import *
from ui import Button, font2
from settings import *
import camera
from planet import Planet
from physics import *
from grid import grid_surface, redraw_grid
from ui import InputBox, font
from menu import *
from solar_system_simulation import *
from global_variables import *
from artemis2 import *
pygame.init()
pygame.display.set_caption("GRAVICODE")
clock = pygame.time.Clock()


mass_box = InputBox(10, 10, 80, 30, "50")
radius_box = InputBox(100, 10, 80, 30, "10")

dragging = False
drag_start = (0, 0)
drag_end = (0, 0)

show_trails = True





def draw_velocity_indicator(dragging):
    if not dragging: return
    sx1, sy1 = camera.world_to_screen(*drag_start)
    sx2, sy2 = camera.world_to_screen(*drag_end)

    pygame.draw.circle(gv.screen, WHITE, (sx1, sy1), 5)

    pygame.draw.line(
        gv.screen,
        WHITE,
        (sx1, sy1),
        (sx2, sy2),
        2
    )

    _, _, speed = calculate_drag_velocity(drag_start, drag_end)

    velocity_text = font.render(
        f"v = {speed:.5f} px/s",
        True,
        WHITE
    )

    gv.screen.blit(
        velocity_text,
        (sx1 + 10, sy1 + 10)
    )


def create_planet():
    mass = mass_box.get_value(50)
    radius = radius_box.get_value(10)

    vx, vy, _ = calculate_drag_velocity(drag_start, drag_end)

    color = (
        random.randint(120, 255),
        random.randint(120, 255),
        random.randint(120, 255),
    )

    planet = Planet(drag_start[0], drag_start[1], mass, radius, color, len(gv.planets) + 1)

    planet.vx = vx
    planet.vy = vy

    gv.planets.append(planet)

initialize_menu(gv.planets, gv.buttons, gv.screen, gv.set_scene)

for button in gv.buttons:
    button.screen = gv.screen

redraw_grid()


running = True

while running:
    gv.screen.fill(BLACK)
    fps = clock.get_fps()
    clock.tick(60)
    if gv.scene != "MENU":
        if camera.move_camera(): redraw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for p in gv.planets:
            p.handle_event(event)
            
        for button in gv.buttons:
            button.check_if_pressed(event)
        mass_box.handle_event(event)
        radius_box.handle_event(event)

       

        if event.type == pygame.MOUSEWHEEL and gv.scene != "MENU":
            if camera.zoom_camera(event): redraw_grid()
        if gv.scene == "SOLAR-SYSTEM-SIMULATION" and event.type == pygame.KEYDOWN and event.key == pygame.K_q:
            show_trails = not show_trails
        if event.type == pygame.KEYDOWN and gv.scene == "OPEN-SIMULATION":

            if event.key == pygame.K_r:
                gv.planets.clear()
                camera.reset_camera()
                redraw_grid()

            if event.key == pygame.K_q:
                show_trails = not show_trails

        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and gv.scene == "OPEN-SIMULATION"):

            mouse_over_input = (mass_box.rect.collidepoint(event.pos) or radius_box.rect.collidepoint(event.pos))

            if not mouse_over_input:
                dragging = True
                drag_start = camera.screen_to_world(*event.pos)
                drag_end = drag_start

        if (event.type == pygame.MOUSEMOTION and dragging):

            drag_end = camera.screen_to_world(*event.pos)
        if (event.type == pygame.MOUSEBUTTONUP and event.button == 1 and dragging):
            dragging = False
            create_planet()
    gv.screen.blit(grid_surface, (0, 0))


    for button in gv.buttons:
        button.update()
        button.draw()
    if gv.scene == "MENU":
        draw_menu_ui(gv.screen) 
    elif gv.scene == "OPEN-SIMULATION":
        if len(gv.planets) > 80:
            show_trails = False
        draw_open_simulation_ui(gv.screen, mass_box, radius_box, gv.planets, fps)
        update_simulation(gv.screen, gv.planets, show_trails)
        draw_velocity_indicator(dragging)
    elif gv.scene == "SOLAR-SYSTEM-SIMULATION":
        draw_solar_system_simulation_ui(gv.screen, gv.planets, fps)
        update_solar_system_simulation(gv.screen, gv.planets, show_trails)
    elif gv.scene == "ARTEMIS-2-SIMULATION":
        draw_artemis_2_simulation_ui(gv.screen, gv.planets, fps)
        update_artemis_2_simulation(gv.set_scene, gv.planets, fps)
    
    pygame.display.flip()

pygame.quit()