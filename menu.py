from planet import Planet
from ui import *
from settings import WIDTH, HEIGHT, BLACK, WHITE
import camera
import global_variables as gv
import solar_system_simulation as solar_system
import open_simulation as open_simulation
import artemis2 as artemis2
from grid import *

def draw_menu_ui(screen):
    screen.blit(
            font2.render("GRAVICODE", True, WHITE),
            (WIDTH / 2 - 120, 100)
        )

    screen.blit(
            font.render(
                "AUTHOR: TIMOFEI FILIP EMANUEL -> 8C",
                True,
                WHITE
            ),
            (30, HEIGHT - 60)
        )

    screen.blit(
            font.render(
                "AUTHOR: BUNGHEZ ANDREI -> 6C",
                True,
                WHITE
            ),
            (30, HEIGHT - 40)
        )

    screen.blit(
            font.render(
                "TEACHER 1: RADU SIMONA",
                True,
                WHITE
            ),
            (WIDTH - 260, HEIGHT - 80)
        )

    screen.blit(
            font.render(
                "TEACHER 2: DOBRIN FLORIN",
                True,
                WHITE
            ),
            (WIDTH - 260, HEIGHT - 60)
        )

    screen.blit(
            font.render(
                "TEACHER 3: MEMET EDEN",
                True,
                WHITE
            ),
            (WIDTH - 260, HEIGHT - 40)
        )



def initialize_menu(planets, buttons, screen, set_scene):
    planets.clear()
    buttons.clear()

    b = Button(
        screen,
        WIDTH / 2 - 180, 200,
        360, 80,
        function=lambda: open_simulation.create_open_simulation(),
        text="Open simulation",
        text_color=BLACK,
        background_color=WHITE
    )

    buttons.append(b)

    b = Button(
        screen,
        WIDTH / 2 - 180, 320,
        360, 80,
        function=lambda: artemis2.create_artemis_2_simulation(),
        text="ARTEMIS 2",
        text_color=BLACK,
        background_color=WHITE
    )

    buttons.append(b)

    b = Button(
        screen,
        WIDTH / 2 - 180, 440,
        360, 80,
        function=lambda: solar_system.create_solar_system(),
        text="SOLAR SYSTEM",
        text_color=BLACK,
        background_color=WHITE
    )

    buttons.append(b)
def go_to_menu():
    global scene

    camera.reset_camera()

    gv.scene = "MENU"

    gv.planets.clear()
    gv.buttons.clear()

    initialize_menu(
        gv.planets,
        gv.buttons,
        gv.screen,
        gv.set_scene,
    )

    redraw_grid()
