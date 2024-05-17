import pygame

pygame.init()

class Button:
    sound_effect = pygame.mixer.Sound("assets/Son_clic.wav")  # Charger le son de clic une seule fois

    def __init__(self, x, y, width, height, text, text_color, button_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.button_color = button_color
        self.sound_on = True  # Variable pour le son

    def draw(self, surface, outline=None):
        if outline:
            pygame.draw.rect(surface, outline, self.rect, 0)
        pygame.draw.rect(surface, self.button_color, self.rect, 0)

        if self.text != '':
            font = pygame.font.SysFont(None, 36)
            text = font.render(self.text, True, self.text_color)
            surface.blit(text, (self.rect.x + (self.rect.width // 2 - text.get_width() // 2),
                                self.rect.y + (self.rect.height // 2 - text.get_height() // 2)))

    def play_sound(self):
        from option_page import OptionPage
        if OptionPage.sound_on and self.sound_on:
            self.sound_effect.play()
            
    def update_color(self, button_color, text_color):
        self.button_color = button_color
        self.text_color = text_color


