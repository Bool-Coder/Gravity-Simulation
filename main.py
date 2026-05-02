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

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("GRAVICODE")
clock = pygame.time.Clock()
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
    global scene

    camera.reset_camera()

    scene = "MENU"

    planets.clear()
    buttons.clear()

    initialize_menu(
        planets,
        buttons,
        screen,
        set_scene,
        create_solar_system
    )

    redraw_grid()


def set_scene(new_scene):
    global scene
    planets.clear()
    buttons.clear()
    if new_scene != "MENU":
        menu_button = Button(
            screen,
            WIDTH - 75,
            HEIGHT - 35,
            60,
            25,
            lambda: go_to_menu(),
            "MENU",
            BLACK,
            WHITE,
            font
        )

        buttons.append(menu_button)

    scene = new_scene


def create_solar_system():
    global scene, planets, buttons
    menu_button = Button(
            screen,
            WIDTH - 75,
            HEIGHT - 35,
            60,
            25,
            lambda: go_to_menu(),
            "MENU",
            BLACK,
            WHITE,
            font
        )

    buttons.append(menu_button)
    
    planets.clear()
    buttons.clear()
    scene = "SOLAR-SYSTEM-SIMULATION"
    planets.clear()

    # ---------------- SUN ----------------
    sun = Planet(
        0,              # x
        0,              # y
        50000,          # mass
        30,             # radius
        (255, 220, 0), # color
        1
    )

    sun.vx = 0
    sun.vy = 0

    planets.append(sun)

    # ---------------- EARTH ----------------
    earth = Planet(
        350,            # distance from sun
        0,
        120,
        10,
        (80, 120, 255),
        2
    )

    # orbital velocity around sun
    earth.vx = 0
    earth.vy = -12

    planets.append(earth)

    # ---------------- MOON ----------------
    moon = Planet(
        390,            # earth position + moon distance
        0,
        2,
        4,
        (220, 220, 220),
        3
    )

    # IMPORTANT:
    # moon velocity = earth velocity + moon orbital velocity
    moon.vx = 0
    moon.vy = -16

    planets.append(moon)


def draw_velocity_indicator(dragging):
    if not dragging: return
    sx1, sy1 = camera.world_to_screen(*drag_start)
    sx2, sy2 = camera.world_to_screen(*drag_end)

    pygame.draw.circle(screen, WHITE, (sx1, sy1), 5)

    pygame.draw.line(
        screen,
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

    screen.blit(
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

    planet = Planet(drag_start[0], drag_start[1], mass, radius, color, len(planets) + 1)

    planet.vx = vx
    planet.vy = vy

    planets.append(planet)


initialize_menu(planets, buttons, screen, set_scene, create_solar_system)

for button in buttons:
    button.screen = screen

redraw_grid()




running = True

while running:
    screen.fill(BLACK)
    fps = clock.get_fps()
    clock.tick(60)
    if scene != "MENU":
        if camera.move_camera(): redraw_grid()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        for button in buttons:
            button.check_if_pressed(event)
        mass_box.handle_event(event)
        radius_box.handle_event(event)

        for p in planets:
            p.handle_event(event)

        if event.type == pygame.MOUSEWHEEL and scene != "MENU":
            if camera.zoom_camera(event): redraw_grid()
            
        if event.type == pygame.KEYDOWN and scene == "OPEN-SIMULATION":

            if event.key == pygame.K_r:
                planets.clear()
                camera.reset_camera()
                redraw_grid()

            if event.key == pygame.K_q:
                show_trails = not show_trails

        if (event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and scene == "OPEN-SIMULATION"):

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
    screen.blit(grid_surface, (0, 0))


    for button in buttons:
        button.update()
        button.draw()
    print(len(buttons))
    if scene == "MENU":
        draw_menu_ui(screen) 
    elif scene == "OPEN-SIMULATION":
        if len(planets) > 80:
            show_trails = False
        draw_open_simulation_ui(screen, mass_box, radius_box, planets, fps)
        update_simulation(screen, planets, show_trails)
        draw_velocity_indicator(dragging)
    elif scene == "SOLAR-SYSTEM-SIMULATION":
        draw_solar_system_simulation_ui(screen, planets, fps)
        update_solar_system_simulation(screen, planets, show_trails)
    pygame.display.flip()

pygame.quit()