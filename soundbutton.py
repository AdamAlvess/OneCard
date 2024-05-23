import pygame
from button import Button

pygame.init()

class SoundButton(Button):
    sound_on = True
    sound_effect = pygame.mixer.Sound("assets/Son_clic.wav")

    @classmethod
    def toggle_sound(cls):
        # Inverse l'état du son
        cls.sound_on = not cls.sound_on


    def __init__(self, x, y, width, height, text, text_color, button_color):
        super().__init__(x, y, width, height, text, text_color, button_color)

    def action(self):
        print("Action: Gestion du son")
        if SoundButton.sound_on:
            self.play_sound(SoundButton.sound_effect)  # Joue le son de clic

    def play_sound(self, sound):
        # Joue le son uniquement si le son est activé
        if SoundButton.sound_on:
            sound.play()

    def update_color(self, button_color, text_color):
        self.button_color = button_color
        self.text_color = text_color
