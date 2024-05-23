import pygame
import sys
from Joueur import Joueur
from assets.couleur import SetupPygame
from play import Play
from retourbutton import RetourButton
from assets.couleur import Couleur


class SelectPersoPage:
    def __init__(self, screen, background_image, ser):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.background_image = background_image
        self.joueur1 = Joueur("Joueur 1", None)
        self.joueur2 = Joueur("Joueur 2", None)
        self.retour_button = RetourButton(20, 20, 100, 50, "Retour", Couleur.BLACK, Couleur.GRIS)

        self.player1_rect = pygame.Rect(50, 100, 200, 500)
        self.player2_rect = pygame.Rect(1030, 100, 200, 500)
        self.perso_images = {
            "Luffy1": pygame.image.load("assets/luffy1(2).png"),
            "Luffy2": pygame.image.load("assets/luffy2(2).png"),
            "Nami1": pygame.image.load("assets/nami1(3).png"),
            "Nami2": pygame.image.load("assets/nami2(1).png"),
            "Zoro1": pygame.image.load("assets/zoro1(3).png"),
            "Zoro2": pygame.image.load("assets/zoro2(2).png"),
            "Usopp1": pygame.image.load("assets/usopp1.png"),
            "Usopp2": pygame.image.load("assets/usopp2(3).png")
        }
        self.selected_color = (0, 255, 0)  # Green for selected
        self.current_color = (255, 255, 0)  # Yellow for current
        self.play_rect = pygame.Rect(550, 600, 180, 60)

        self.ser = ser  # Ajoutez cette ligne pour initialiser l'attribut ser

        # Ajouter des variables pour suivre les sélections des joysticks
        self.joystick1_selection = "Retour"
        self.joystick2_selection = "Retour"
        self.joystick1_index = 0
        self.joystick2_index = 0

        # Variable pour suivre si le bouton retour est sélectionné
        self.retour_selected = False

    @staticmethod
    def run(screen, ser):
        select_perso_page = SelectPersoPage(screen, pygame.image.load("assets/background.jpg"), ser)
        return select_perso_page.run()

    def run(self):
        from home import main_menu
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = pygame.mouse.get_pos()
                    if self.retour_button.rect.collidepoint(pos):
                        print("Retour...")
                        self.retour_button.action()
                        return "home"
                    elif self.player1_rect.collidepoint(pos):
                        self.joueur1.perso = self.select_perso(pos)
                    elif self.player2_rect.collidepoint(pos):
                        self.joueur2.perso = self.select_perso(pos)
                    elif self.play_rect.collidepoint(pos):
                        if self.joueur1.perso is not None and self.joueur2.perso is not None:
                            play_page = Play(self.screen, self.joueur1, self.joueur2, self.perso_images, self.ser)
                            self.retour_button.action()
                            play_page.run()
                            return

            self.handle_joystick_input()
            self.draw()
            pygame.display.flip()
            self.clock.tick(30)

    def handle_joystick_input(self):
        from home import STATE_HOME
        joystick_data = self.read_joystick_data()
        if joystick_data:
            x1, y1, x2, y2, btn1, btn2, btn3, btn4, btn5, btn6 = joystick_data

            # Gérer le mouvement vers le haut ou le bas du joystick 1
            if y1 > 600:  # Joystick bas
                self.joystick1_index = (self.joystick1_index + 1) % (len(self.perso_images) // 2 + 2)
            elif y1 < 400:  # Joystick haut
                self.joystick1_index = (self.joystick1_index - 1) % (len(self.perso_images) // 2 + 2)

            if self.joystick1_index == len(self.perso_images) // 2:
                self.joystick1_selection = "Retour"
                self.retour_selected = True  # Bouton retour sélectionné
            elif self.joystick1_index == len(self.perso_images) // 2 + 1:
                self.joystick1_selection = "Play"
                self.retour_selected = False  # Bouton retour non sélectionné
            else:
                self.joystick1_selection = list(self.perso_images.keys())[self.joystick1_index * 2]
                self.retour_selected = False  # Bouton retour non sélectionné

            if btn1 == 0:  # Bouton du joystick 1 pressé
                if self.joystick1_selection in self.perso_images:
                    self.joueur1.perso = self.joystick1_selection
                elif self.joystick1_selection == "Retour":
                    print("Retour1111...")
                    self.retour_button.action()
                    return STATE_HOME   # Retourne "home" immédiatement pour revenir à l'accueil
                elif self.joystick1_selection == "Play":
                    if self.joueur1.perso is not None and self.joueur2.perso is not None:
                        play_page = Play(self.screen, self.joueur1, self.joueur2, self.perso_images, self.ser)
                        self.retour_button.action()
                        play_page.run()
                        return

            # Gérer le mouvement vers le haut ou le bas du joystick 2
            if y2 > 600:  # Joystick bas
                self.joystick2_index = (self.joystick2_index + 1) % (len(self.perso_images) // 2 + 2)
            elif y2 < 400:  # Joystick haut
                self.joystick2_index = (self.joystick2_index - 1) % (len(self.perso_images) // 2 + 2)

            if self.joystick2_index == len(self.perso_images) // 2:
                self.joystick2_selection = "Retour"
            elif self.joystick2_index == len(self.perso_images) // 2 + 1:
                self.joystick2_selection = "Play"
            else:
                self.joystick2_selection = list(self.perso_images.keys())[self.joystick2_index * 2 + 1]

            if btn4 == 0:  # Bouton du joystick 2 pressé
                if self.joystick2_selection in self.perso_images:
                    self.joueur2.perso = self.joystick2_selection
                elif self.joystick2_selection == "Retour":
                    print("Retour...")
                    self.retour_button.action()  # Appeler la méthode action du bouton Retour
                    return "home"  # Retourne "home" immédiatement pour revenir à l'accueil
                elif self.joystick2_selection == "Play":
                    if self.joueur1.perso is not None and self.joueur2.perso is not None:
                        play_page = Play(self.screen, self.joueur1, self.joueur2, self.perso_images, self.ser)
                        self.retour_button.action()
                        play_page.run()
                        return

    def select_perso(self, pos):
        for perso, image in self.perso_images.items():
            if perso.endswith("1"):
                rect = pygame.Rect(50, 150 + 100 * (list(self.perso_images.keys()).index(perso) // 2), image.get_width(), image.get_height())
            else:
                rect = pygame.Rect(1030, 150 + 100 * (list(self.perso_images.keys()).index(perso) // 2), image.get_width(), image.get_height())
            if rect.collidepoint(pos):
                return perso

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))

        pygame.draw.rect(self.screen, (255, 0, 0), self.player1_rect, 2)
        pygame.draw.rect(self.screen, (0, 0, 255), self.player2_rect, 2)

        # Dessiner les personnages et les sélections
        offset = 0
        for perso, image in self.perso_images.items():
            if perso.endswith("1"):
                rect = image.get_rect(topleft=(50, 150 + offset))
                self.screen.blit(image, (50, 150 + offset))
                if perso == self.joueur1.perso:
                    pygame.draw.rect(self.screen, self.selected_color, rect, 2)
                elif perso == self.joystick1_selection:
                    pygame.draw.rect(self.screen, self.current_color, rect, 2)
                offset += 100

        offset = 0
        for perso, image in self.perso_images.items():
            if perso.endswith("2"):
                rect = image.get_rect(topleft=(1030, 150 + offset))
                self.screen.blit(image, (1030, 150 + offset))
                if perso == self.joueur2.perso:
                    pygame.draw.rect(self.screen, self.selected_color, rect, 2)
                elif perso == self.joystick2_selection:
                    pygame.draw.rect(self.screen, self.current_color, rect, 2)
                offset += 100

        # Dessiner le bouton Retour avec des couleurs différentes si sélectionné
        retour_color = Couleur.RED if self.retour_selected else Couleur.BLACK
        retour_text_color = Couleur.BLACK if self.retour_selected else Couleur.RED
        self.retour_button.update_color(retour_color, retour_text_color)
        self.retour_button.draw(self.screen)

        # Dessiner le bouton Play avec la couleur de sélection
        play_color = self.current_color if self.joystick1_selection == "Play" or self.joystick2_selection == "Play" else (0, 255, 0)
        pygame.draw.rect(self.screen, play_color, self.play_rect, 2)
        text_play = self.font.render("Play", True, play_color)
        self.screen.blit(text_play, text_play.get_rect(center=self.play_rect.center))

        pygame.display.flip()

    def read_joystick_data(self):  # Ajoutez self comme premier argument
        try:
            data = self.ser.readline().decode('utf-8').strip()  # Utilisez self.ser pour accéder à l'attribut ser
            if data:
                x1, y1, x2, y2, btn1, btn2, btn3, btn4, btn5, btn6 = map(int, data.split(','))
                return x1, y1, x2, y2, btn1, btn2, btn3, btn4, btn5, btn6
        except:
            return None
