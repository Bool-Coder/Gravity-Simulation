from ui import *
from settings import *
from physics import *
import camera
from planet import Planet
import global_variables as gv
from grid import *
import menu as menu

def create_artemis_2_simulation():
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
    gv.scene = "ARTEMIS-2-SIMULATION"

    # ---------------- Earth ----------------
    earth = Planet(
        0, 0,
        5000,
        100,
        (80, 120, 255),
        "Earth"
    )
    earth.vx = 0
    earth.vy = 0
    gv.planets.append(earth)

    # ---------------- Moon ----------------
    moon = Planet(
        500, -200,
        500,
        30,
        (220, 220, 220),
        "Moon"
    )
    moon.vx = 0
    moon.vy = 60
    gv.planets.append(moon)

    # ---------------- Artemis ----------------
    artemis = Planet(
        100, 200,
        1,
        10,
        (220, 0, 0),
        "Artemis"
    )
    artemis.vx = 100
    artemis.vy = 0
    gv.planets.append(artemis)




def draw_artemis_2_simulation_ui(screen, planets, fps):
    screen.blit(
        font.render("Q orbits on/off", True, WHITE),
        (10, 15)
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

    mouse_world_x, mouse_world_y = camera.screen_to_world(
        *pygame.mouse.get_pos()
    )

    pos_text = font.render(
        f"X: {mouse_world_x:.1f} Y: {mouse_world_y:.1f}",
        True,
        WHITE
    )
    screen.blit(pos_text, (10, HEIGHT - 30))
def update_artemis_2_simulation(screen, planets, show_trails):
    for i in range(len(planets) - 1):
        for j in range(i + 1, len(planets)):
            apply_gravity(planets[i], planets[j])
    for p in planets:
        update_energy(p, planets)
        if p.id != "Earth":
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