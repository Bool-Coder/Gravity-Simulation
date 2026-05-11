import math
from settings import G, DT, EPS, MAX_DIST, TRAIL_LENGTH
from pygame import Vector2

def get_speed(planet):
    return (planet.vx**2 + planet.vy**2) ** 0.5

def update_energy(planet, planets):
    speed = get_speed(planet)
    planet.kinetic_energy = 0.5 * planet.mass * speed**2
    planet.potential_energy = 0

    for p in planets:
        if p is planet:
            continue
        dx = planet.x - p.x
        dy = planet.y - p.y
        r = (dx*dx + dy*dy) ** 0.5 + EPS

        planet.potential_energy += -G * planet.mass * p.mass / r

    planet.total_energy = planet.kinetic_energy + planet.potential_energy

def get_distance(a,  b):
    dx = b.x - a.x
    dy = b.y - a.y
    return math.sqrt((dx * dx + dy * dy + EPS * EPS))
def update_velocity(planet1, planet2, distance):
    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y
    force = G * planet1.mass * planet2.mass / (distance * distance)
    alpha = math.atan2(dy, dx)
    fx = force * math.cos(alpha)
    fy = force * math.sin(alpha)

    planet1.vx += fx / planet1.mass * DT
    planet1.vy += fy / planet1.mass * DT
    planet2.vx -= fx / planet2.mass * DT
    planet2.vy -= fy / planet2.mass * DT

def apply_gravity(planet1, planet2):
    distance = get_distance(Vector2 (planet1.x, planet1.y), Vector2(planet2.x, planet2.y))
    if distance > MAX_DIST: return
    update_velocity(planet1, planet2, distance)
    

def update_position(planet, show_trails):
    planet.x += planet.vx * DT
    planet.y += planet.vy * DT
    
    planet.trail.append((planet.x, planet.y))
    if len(planet.trail) > TRAIL_LENGTH:
        planet.trail.pop(0)

def check_collision_planets(planet1, planet2):
    dx = planet2.x - planet1.x
    dy = planet2.y - planet1.y
    distance = get_distance(Vector2(planet1.x, planet1.y), Vector2(planet2.x, planet2.y))
    min_dist = planet1.radius + planet2.radius
    if distance < min_dist and distance > 0:
        nx, ny = dx / distance, dy / distance

        v1n = planet1.vx * nx + planet1.vy * ny
        v2n = planet2.vx * nx + planet2.vy * ny
        e = 1
        v1n_new = (planet1.mass * v1n + planet2.mass * v2n - planet2.mass * e * (v1n - v2n)) / (planet1.mass + planet2.mass)
        v2n_new = (planet1.mass * v1n + planet2.mass * v2n + planet1.mass * e * (v1n - v2n)) / (planet1.mass + planet2.mass)

        planet1.vx += (v1n_new - v1n) * nx
        planet1.vy += (v1n_new - v1n) * ny
        planet2.vx += (v2n_new - v2n) * nx
        planet2.vy += (v2n_new - v2n) * ny

def update_collisions(planets):
    for i in range(len(planets) - 1):
        for j in range(i + 1, len(planets)):
            check_collision_planets(planets[i], planets[j])
def calculate_drag_velocity(drag_start, drag_end):
    dx = drag_start[0] - drag_end[0]
    dy = drag_start[1] - drag_end[1]

    vx = dx * 0.5
    vy = dy * 0.5

    speed = math.sqrt(dx * dx + dy * dy) * 0.5

    return vx, vy, speed
