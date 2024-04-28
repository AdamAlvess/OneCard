import pygame
from assets.couleur import Couleur
from button import Button
from musicbutton import MusicButton
from commandbutton import CommandButton
from soundbutton import SoundButton

class OptionPage:
    def __init__(self, app):
        self.app = app
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Options")

        self.background_image = pygame.image.load("assets/back_home.jpg").convert()
        self.font = pygame.font.SysFont(None, 36)

        self.retour_button = Button(250, 20, 200, 50, "Retour", Couleur.BLACK, Couleur.GRIS)
        self.music_button = MusicButton(500, 250, 200, 50, "Music", Couleur.BLACK, Couleur.GRIS)
        self.sound_button = SoundButton(500, 350, 200, 50, "Sound", Couleur.BLACK, Couleur.GRIS)
        self.command_button = CommandButton(500, 450, 200, 50, "Commands", Couleur.BLACK, Couleur.GRIS)
        self.buttons = [self.retour_button, self.music_button, self.sound_button, self.command_button]

    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_obj, text_rect)

    def show_options(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    for button in self.buttons:
                        if button.rect.collidepoint(mouse_pos):
                            if button == self.retour_button:
                                print("Home...")
                                return "home"  # Retour à la page d'accueil
                            elif button == self.music_button:
                                # Action à effectuer lors du clic sur le bouton Music
                                print("Action Music...")
                            elif button == self.sound_button:
                                # Action à effectuer lors du clic sur le bouton Sound
                                print("Action Sound...")
                            elif button == self.command_button:
                                # Action à effectuer lors du clic sur le bouton Commands
                                print("Action Commands...")

            self.screen.blit(self.background_image, (0, 0))
            self.draw_text("Page des options", self.font, Couleur.BLACK, self.screen, 20, 20)

            for button in self.buttons:
                button.draw(self.screen, Couleur.BLACK)

            pygame.display.update()  # Met à jour l'affichage
