from planet import Planet
from ui import *
from settings import WIDTH, HEIGHT, BLACK, WHITE


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



def initialize_menu(planets, buttons, screen, set_scene, create_solar_system):
    planets.clear()
    buttons.clear()

    b = Button(
        screen,
        WIDTH / 2 - 180, 200,
        360, 80,
        function=lambda: set_scene("OPEN-SIMULATION"),
        text="Open simulation",
        text_color=BLACK,
        background_color=WHITE
    )

    buttons.append(b)

    b = Button(
        screen,
        WIDTH / 2 - 180, 320,
        360, 80,
        function=lambda: set_scene("ARTEMIS-2-SIMULATION"),
        text="ARTEMIS 2",
        text_color=BLACK,
        background_color=WHITE
    )

    buttons.append(b)

    b = Button(
        screen,
        WIDTH / 2 - 180, 440,
        360, 80,
        function=lambda: create_solar_system(),
        text="SOLAR SYSTEM",
        text_color=BLACK,
        background_color=WHITE
    )

    buttons.append(b)