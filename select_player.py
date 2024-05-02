import pygame
import sys
from Joueur import Joueur 
from assets.couleur import SetupPygame
from play import Play
from retourbutton import RetourButton
from assets.couleur import Couleur


class SelectPersoPage:
    def __init__(self, screen, background_image):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.background_image = background_image
        self.joueur1 = Joueur("Joueur 1", None)  
        self.joueur2 = Joueur("Joueur 2", None) 
        self.retour_button = RetourButton(20, 20, 100, 50, "Retour", Couleur.BLACK, Couleur.GRIS)  # Positionne le bouton de retour

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
        self.selected_color = (255, 255, 0)
        self.play_rect = pygame.Rect(550, 600, 180, 60)
        #self.return_button_rect = pygame.Rect(20, 20, 100, 50) 
        
    @staticmethod
    def run(screen):
        select_perso_page = SelectPersoPage(screen)
        select_perso_page.run()

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
                    if self.retour_button.rect.collidepoint(pos):  # Vérifie si le bouton de retour est cliqué
                        print("Retour...")
                        return "home"  # Retourne à la page d'accueil
                    
                    elif self.player1_rect.collidepoint(pos):
                        self.joueur1.perso = self.select_perso(pos)
                    elif self.player2_rect.collidepoint(pos):
                        self.joueur2.perso = self.select_perso(pos)
                    elif self.play_rect.collidepoint(pos):
                        if self.joueur1.perso is not None and self.joueur2.perso is not None:
                            play_page = Play(self.screen, self.joueur1, self.joueur2, self.perso_images)
                            play_page.run()
                            return
                     

            self.draw()
            pygame.display.flip()
            self.clock.tick(30) 
            
    def select_perso(self, pos):
        for perso, image in self.perso_images.items():
            if perso.endswith("1"):
                rect = pygame.Rect(50, 150 + 100 * (list(self.perso_images.keys()).index(perso) // 2), image.get_width(), image.get_height())  # Rectangle pour joueur 1
            else:
                rect = pygame.Rect(1030, 150 + 100 * (list(self.perso_images.keys()).index(perso) // 2), image.get_width(), image.get_height())  # Rectangle pour joueur 2
            if rect.collidepoint(pos):
                return perso

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))

        pygame.draw.rect(self.screen, (255, 0, 0), self.player1_rect, 2)
        pygame.draw.rect(self.screen, (0, 0, 255), self.player2_rect, 2)
        self.retour_button.draw(self.screen)  # Dessine le bouton de retour


        offset = 0
        for perso, image in self.perso_images.items():
            if perso.endswith("1"):
                rect = image.get_rect(topleft=(50, 150 + offset))
                self.screen.blit(image, (50, 150 + offset))
                if perso == self.joueur1.perso:
                    pygame.draw.rect(self.screen, self.selected_color, rect, 2)
                offset += 100

        offset = 0
        for perso, image in self.perso_images.items():
            if perso.endswith("2"):
                rect = image.get_rect(topleft=(1030, 150 + offset))
                self.screen.blit(image, (1030, 150 + offset))
                if perso == self.joueur2.perso:
                    pygame.draw.rect(self.screen, self.selected_color, rect, 2)
                offset += 100

        pygame.draw.rect(self.screen, (0, 255, 0), self.play_rect)
        play_text = self.font.render("Play", True, (255, 255, 255))
        self.screen.blit(play_text, self.play_rect.topleft)

        #pygame.draw.rect(self.screen, (255, 0, 0), self.return_button_rect)
        #return_text = self.font.render("Retour", True, (255, 255, 255))
        #self.screen.blit(return_text, self.return_button_rect.topleft)