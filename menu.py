from planet import Planet
from button import Button
from settings import WIDTH, HEIGHT

def initialize_menu(planets, buttons, screen, set_scene):
    planets.clear()
    buttons.clear()

    b = Button(
        screen,
        WIDTH / 2 - 180, 200,
        360, 80,
        function=lambda: set_scene("SIMULATION"),
        text="Open simulation",
        text_color=(0, 0, 0),
        background_color=(255, 255, 255)
    )

    buttons.append(b)

    b = Button(
        screen,
        WIDTH / 2 - 180, 320,
        360, 80,
        function=lambda: set_scene("ARTEMIS-2-SIMULATION"),
        text="ARTEMIS 2",
        text_color=(0, 0, 0),
        background_color=(255, 255, 255)
    )

    buttons.append(b)

    b = Button(
        screen,
        WIDTH / 2 - 180, 440,
        360, 80,
        function=lambda: set_scene("SOLAR-SYSTEM-SIMULATION"),
        text="SOLAR SYSTEM",
        text_color=(0, 0, 0),
        background_color=(255, 255, 255)
    )

    buttons.append(b)

    # p = Planet(0, 0, 5000, 50, (255, 255, 0))
    # planets.append(p)

    # p = Planet(0, 250, 10, 7, (255, 0, 0))
    # p.vx = 60
    # planets.append(p)

    # p = Planet(450, 0, 15, 10, (0, 255, 0))
    # p.vy = -60
    # planets.append(p)

    # p = Planet(0, -250, 10, 7, (0, 0, 255))
    # p.vx = -60
    # planets.append(p)