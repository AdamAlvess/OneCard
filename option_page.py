import pygame
from assets.couleur import Couleur
from button import Button
from retourbutton import RetourButton
from musicbutton import MusicButton
from commandbutton import CommandButton
from soundbutton import SoundButton

pygame.init()

class OptionPage:
    current_music_volume = 0.5  # Volume initial (de 0 à 1)
    sound_effect1 = pygame.mixer.Sound("assets/Son_clic.wav")
    sound_on = True  # Variable pour le son

    def __init__(self, app):
        self.app = app
        self.SCREEN_WIDTH = 1280
        self.SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.set_caption("Options")

        self.background_image = pygame.image.load("assets/back_home.jpg").convert()
        self.font = pygame.font.SysFont(None, 36)

        self.retour_button = RetourButton(250, 20, 200, 50, "Retour", Couleur.BLACK, Couleur.GRIS)
        self.music_button = MusicButton(500, 250, 200, 50, "Music", Couleur.BLACK, Couleur.GRIS)
        self.sound_button = SoundButton(500, 350, 200, 50, "Sound", Couleur.BLACK, Couleur.GRIS)
        self.command_button = CommandButton(500, 450, 200, 50, "Commands", Couleur.BLACK, Couleur.GRIS)
        self.buttons = [self.retour_button, self.music_button, self.sound_button, self.command_button]

        # Variables pour le curseur de volume
        self.volume_slider_x = 400
        self.volume_slider_y = 300
        self.volume_slider_width = 400
        self.volume_slider_height = 10

    def draw_text(self, text, font, color, surface, x, y):
        text_obj = font.render(text, True, color)
        text_rect = text_obj.get_rect()
        text_rect.topleft = (x, y)
        surface.blit(text_obj, text_rect)
        
    @staticmethod
    def set_music_volume(option_page):
        global current_music_volume
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        mouse_x, _ = pygame.mouse.get_pos()
                        current_music_volume = max(0, min(1, (mouse_x - option_page.volume_slider_x) - option_page.volume_slider_width))
                        pygame.mixer.music.set_volume(current_music_volume)
                        print("Volume de la musique:", current_music_volume)
                        return


    def show_volume_slider(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:  # Left mouse button
                        self.handle_slider_movement()  # Correction du nom de la méthode
                        if self.is_ok_clicked(event.pos):  # Vérifie si le bouton "OK" est cliqué
                            return  # Retourne à la page des options si le bouton "OK" est cliqué
                elif event.type == pygame.MOUSEMOTION:
                    if pygame.mouse.get_pressed()[0]:  # Si le bouton de la souris est maintenu enfoncé
                        self.handle_slider_movement()  # Gère le mouvement continu du curseur

            # Affiche la fenêtre pop-up avec le slider
            self.screen.blit(self.background_image, (0, 0))
            pygame.draw.rect(self.screen, Couleur.GRIS, (self.volume_slider_x, self.volume_slider_y,
                                                        self.volume_slider_width, self.volume_slider_height))
            pygame.draw.rect(self.screen, Couleur.BLACK, (int(self.volume_slider_x + OptionPage.current_music_volume *
                                                            self.volume_slider_width - 5),
                                                        self.volume_slider_y - 5, 10, 20))

            # Dessine le bouton "OK"
            pygame.draw.rect(self.screen, Couleur.GRIS, (550, 500, 100, 50))
            self.draw_text("OK", self.font, Couleur.BLACK, self.screen, 580, 515)

            pygame.display.update()


    def handle_slider_movement(self):
        # Gère le mouvement continu du curseur
        mouse_x, mouse_y = pygame.mouse.get_pos()
        if (self.volume_slider_x <= mouse_x <= self.volume_slider_x + self.volume_slider_width and
            self.volume_slider_y - 5 <= mouse_y <= self.volume_slider_y + 20):
            volume = (mouse_x - self.volume_slider_x) / self.volume_slider_width
            volume = max(0, min(1, volume))
            pygame.mixer.music.set_volume(volume)
            OptionPage.current_music_volume = volume
            print("Volume de la musique:", volume)



    def is_ok_clicked(self, mouse_pos):
        # Vérifie si le bouton "OK" est cliqué
        ok_button_rect = pygame.Rect(550, 500, 100, 50)
        if ok_button_rect.collidepoint(mouse_pos):
            self.retour_button.action()  
            return True
        return False

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
                                self.retour_button.action()
                                return "home"
                            elif button == self.music_button:
                                print("Affichage de la fenêtre de contrôle du volume...")
                                self.music_button.action()
                                self.show_volume_slider()
                            elif button == self.sound_button:
                                print("Action Sound...")
                                self.sound_button.action()
                                OptionPage.sound_on = not OptionPage.sound_on # Inverser l'état du son lorsque le bouton Sound est cliqué
                            elif button == self.command_button:
                                print("Action Commands...")
                                self.command_button.action()
                                self.show_command_window()

            self.screen.blit(self.background_image, (0, 0))
            self.draw_text("Page des options", self.font, Couleur.BLACK, self.screen, 20, 20)

            for button in self.buttons:
                button.draw(self.screen, Couleur.BLACK)

            # Afficher le texte "ON" ou "OFF" à côté du bouton Sound en fonction de l'état du son
            sound_text = "ON" if OptionPage.sound_on else "OFF"
            self.draw_text(sound_text, self.font, Couleur.WHITE, self.screen, 730, 365)

        pygame.display.update()  # Met à jour l'affichage après la boucle while


    def show_command_window(self):
        # Crée une nouvelle surface pour la fenêtre des commandes
        command_screen = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        command_screen.blit(self.background_image, (0, 0))  # Ajoute le fond d'écran

        # Charge l'image des commandes
        command_image = pygame.image.load("assets/commande.png")
        command_image_rect = command_image.get_rect(center=command_screen.get_rect().center)

        # Affiche les commandes et le bouton OK
        command_screen.blit(command_image, command_image_rect)
        pygame.draw.rect(command_screen, Couleur.GRIS, (550, 600, 100, 50))
        self.draw_text("OK", self.font, Couleur.BLACK, command_screen, 580, 615)

        # Affiche la nouvelle surface
        self.screen.blit(command_screen, (0, 0))
        pygame.display.update()

        # Attend le clic sur le bouton OK
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.Rect(550, 600, 100, 50).collidepoint(event.pos):
                        self.retour_button.action()
                        return  # Retourne à la page des options si le bouton "OK" est cliqué
