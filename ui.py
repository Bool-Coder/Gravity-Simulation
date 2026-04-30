import pygame
from settings import GRAY, LIGHT_GRAY, WHITE

pygame.font.init()
font = pygame.font.SysFont("consolas", 18)
menu_button_font = pygame.font.SysFont("consolas", 40)


class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pygame.Rect(x, y, w, h)
        self.color = GRAY
        self.text = text
        self.txt_surface = font.render(text, True, WHITE)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
            self.color = LIGHT_GRAY if self.active else GRAY

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.active = False
                self.color = GRAY
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if len(self.text) < 6 and (event.unicode.isdigit() or event.unicode == '.'):
                    self.text += event.unicode

            self.txt_surface = font.render(self.text, True, WHITE)

    def draw(self, screen):
        screen.blit(self.txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)

    def get_value(self, default):
        try:
            return float(self.text)
        except:
            return default