from planet import Planet

def initialize_menu(planets):
    planets.clear()

    p = Planet(0, 0, 5000, 50, (255, 255, 0))
    planets.append(p)

    p = Planet(0, 250, 10, 7, (255, 0, 0))
    p.vx = 60
    planets.append(p)

    p = Planet(450, 0, 15, 10, (0, 255, 0))
    p.vy = -60
    planets.append(p)

    p = Planet(0, -250, 10, 7, (0, 0, 255))
    p.vx = -60
    planets.append(p)