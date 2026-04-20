import math
from settings import G, DT, EPS, MAX_DIST_SQ, TRAIL_LENGTH

def apply_gravity(p1, p2):
    dx = p2.x - p1.x
    dy = p2.y - p1.y

    dist_sq = dx * dx + dy * dy + EPS * EPS
    if dist_sq > MAX_DIST_SQ:
        return

    dist = math.sqrt(dist_sq)
    force = G * p1.mass * p2.mass / dist_sq

    alpha = math.atan2(dy, dx)
    fx = force * math.cos(alpha)
    fy = force * math.sin(alpha)

    p1.vx += fx / p1.mass * DT
    p1.vy += fy / p1.mass * DT
    p2.vx -= fx / p2.mass * DT
    p2.vy -= fy / p2.mass * DT

def update_position(p, show_trails):
    p.x += p.vx * DT
    p.y += p.vy * DT

    if show_trails:
        p.trail.append((p.x, p.y))
        if len(p.trail) > TRAIL_LENGTH:
            p.trail.pop(0)

def check_planet_collisions(planets):
    for i in range(len(planets) - 1):
        for j in range(i + 1, len(planets)):
            p1 = planets[i]
            p2 = planets[j]
            dx = p2.x - p1.x
            dy = p2.y - p1.y
            dist = math.sqrt(dx*dx + dy*dy)
            min_dist = p1.radius + p2.radius
            if dist < min_dist and dist > 0:
                overlap = (min_dist - dist) / 2
                nx = dx / dist
                ny = dy / dist
                p1.x -= nx * overlap
                p1.y -= ny * overlap
                p2.x += nx * overlap
                p2.y += ny * overlap