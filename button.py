import pygame

class Button:
    def __init__(self, x, y, width, height, text, text_color, button_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.button_color = button_color

    def draw(self, surface, outline=None):
        if outline:
            pygame.draw.rect(surface, outline, self.rect, 0)
        pygame.draw.rect(surface, self.button_color, self.rect, 0)

        if self.text != '':
            font = pygame.font.SysFont(None, 36)
            text = font.render(self.text, True, self.text_color)
            surface.blit(text, (self.rect.x + (self.rect.width // 2 - text.get_width() // 2),
                                self.rect.y + (self.rect.height // 2 - text.get_height() // 2)))
