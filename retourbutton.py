import pygame
import sys
from button import Button

class RetourButton(Button):
    def __init__(self, x, y, width, height, text, text_color, button_color):
        super().__init__(x, y, width, height, text, text_color, button_color)

    def action(self):
        self.play_sound()  # Joue le son de clic
        
    
    def action1(self):
        pygame.quit()  # Quitte la fenêtre de jeu
        sys.exit()  # Termine le programme

    def is_over(self, mouse_pos):
        # Vérifie si les coordonnées du curseur de la souris se trouvent à l'intérieur de la zone du bouton
        return self.rect.collidepoint(mouse_pos)
    
    def update_color(self, button_color, text_color):
        self.button_color = button_color
        self.text_color = text_color