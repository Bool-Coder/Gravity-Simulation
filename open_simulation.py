from settings import *
from ui import font
import camera
from physics import *
from grid import *
from planet import Planet
import global_variables as gv
from ui import *
import menu as menu

def create_open_simulation():
    global scene, planets, buttons

    gv.buttons.clear()
    gv.planets.clear()
    menu_button = Button(
        gv.screen,
        WIDTH - 75,
        HEIGHT - 35,
        60,
        25,
        lambda: menu.go_to_menu(),
        "MENU",
        BLACK,
        WHITE,
        font
    )
    gv.buttons.append(menu_button)
    gv.scene = "OPEN-SIMULATION"

    redraw_grid()

def draw_open_simulation_ui(screen, mass_box, radius_box, planets, fps):
    mass_box.draw(screen)
    radius_box.draw(screen)

    screen.blit(
        font.render("Mass kg", True, WHITE),
        (10, 45)
    )

    screen.blit(
        font.render("Radius px", True, WHITE),
        (100, 45)
    )

    screen.blit(
        font.render(f"FPS: {int(fps)}", True, WHITE),
        (WIDTH - 100, 10)
    )

    screen.blit(
        font.render(
            f"Zoom: {camera.zoom:.2f}",
            True,
            WHITE
        ),
        (WIDTH - 100, 30)
    )

    screen.blit(
        font.render("R reset", True, WHITE),
        (10, 85)
    )

    screen.blit(
        font.render("Q orbits on/off", True, WHITE),
        (10, 105)
    )

    screen.blit(
        font.render(
            f"Planets: {len(planets)}",
            True,
            WHITE
        ),
        (10, 125)
    )

    mouse_world_x, mouse_world_y = camera.screen_to_world(
        *pygame.mouse.get_pos()
    )

    pos_text = font.render(
        f"X: {mouse_world_x:.1f} Y: {mouse_world_y:.1f}",
        True,
        WHITE
    )

    screen.blit(pos_text, (10, HEIGHT - 30))
def update_simulation(screen, planets, show_trails):
    
    for i in range(len(planets) - 1):
        for j in range(i + 1, len(planets)):
            apply_gravity(planets[i], planets[j])
    for p in planets:
        update_energy(p, planets)
        update_position(p, show_trails)
    update_collisions(planets)
    if show_trails:
        for p in planets:
            p.draw_trail(screen)
    for p in planets:
        p.compute_type_of_object(planets)
        p.speed = get_speed(p)
        p.draw(screen)
        p.draw_info(screen)
