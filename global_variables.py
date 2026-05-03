from settings import *
from ui import *

planets = []
screen = pygame.display.set_mode((WIDTH, HEIGHT))
scene = "MENU"
buttons = []

def set_scene(new_scene):
    global scene, planets, buttons
    planets.clear()
    buttons.clear()
    
    scene = new_scene