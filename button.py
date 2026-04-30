import pygame
from ui import menu_button_font

text_offset = 20

class Button:
    def __init__(self, screen, x, y, width, height,
                 function, text, text_color, background_color, font=menu_button_font):

        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.function = function
        self.text = text
        self.text_color = text_color

        self.base_color = background_color
        self.font = font

        self.rect = pygame.Rect(x, y, width, height)

        self.is_hovered = False
        self.is_pressed = False

        self.hover_color = (
            min(background_color[0] + 40, 255),
            min(background_color[1] + 60, 255),
            min(background_color[2] + 40, 255)
        )

        self.press_color = (
            max(background_color[0] - 40, 0),
            max(background_color[1] - 40, 0),
            max(background_color[2] - 40, 0)
        )

    def update(self):
        mouse_pos = pygame.mouse.get_pos()

        self.is_hovered = self.rect.collidepoint(mouse_pos)
        self.is_pressed = self.is_hovered and pygame.mouse.get_pressed()[0]
        

    def draw(self):
        if self.is_hovered:
            rect = self.rect.inflate(10, 5)
        else:
            rect = self.rect
        if self.is_pressed:
            color = self.press_color
        elif self.is_hovered:
            color = self.hover_color
        else:
            color = self.base_color

        pygame.draw.rect(self.screen, color, rect)

        text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = text_surface.get_rect(center=rect.center)

        self.screen.blit(text_surface, text_rect)

    def check_if_pressed(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.function()
                return True
        return False