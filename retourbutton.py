import pygame
from button import Button

class RetourButton(Button):
    def __init__(self, x, y, width, height, text, text_color, button_color):
        super().__init__(x, y, width, height, text, text_color, button_color)

    def action(self):
        print("Action: retour")
        # Implémentez la logique pour gérer la musique...
        self.play_sound()  # Joue le son de clic
