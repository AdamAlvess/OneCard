import pygame
import sys
from retourbutton import RetourButton

class EndGameScreen:
    def __init__(self, screen, winner, joueur1, joueur2, perso_images):
        self.screen = screen
        self.winner = winner
        self.perso_images = perso_images
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.background_image = pygame.image.load("assets/back_home.jpg").convert()

        self.font = pygame.font.Font(None, 36)

        # Création des boutons
        self.retour_button = RetourButton(50, 50, 200, 50, "Retour au menu", (255, 255, 255), (183, 169, 166))
        self.new_game_button = RetourButton(50, 120, 200, 50, "Nouvelle partie", (255, 255, 255), (183, 169, 166))
        self.change_perso_button = RetourButton(50, 190, 200, 50, "Changement de personnage", (255, 255, 255), (183, 169, 166))
    
    

    def run(self):
        from home import main_menu  # Importez la fonction main_menu depuis home.py
        from play import Play  
        from select_player import SelectPersoPage

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    if self.retour_button.is_over(mouse_pos):
                        main_menu(self.retour_button, current_screen="end_game")  # Passer "end_game" comme écran actuel
                    elif self.new_game_button.is_over(mouse_pos):
                        game = Play(self.screen, self.joueur1, self.joueur2, self.perso_images)
                        game.run()  # Relancer une nouvelle partie en créant une instance de la classe Play et en appelant sa méthode run()
                    elif self.change_perso_button.is_over(mouse_pos):
                        select_perso_page = SelectPersoPage(self.screen, self.background_image)
                        select_perso_page.run()

            # Affichage de l'image de fond
            self.screen.blit(self.background_image, (0, 0))

            # Affichage du nom et de l'image du joueur gagnant
            winner_name_text = self.font.render(f"{self.winner.nom} a gagné!", True, (255, 255, 255))
            winner_image = self.perso_images[self.winner.perso]
            winner_image = pygame.transform.scale(winner_image, (200, 200))  # Redimensionne l'image
            text_rect = winner_name_text.get_rect(center=(self.screen.get_width() // 2, self.screen.get_height() // 2))
            image_rect = winner_image.get_rect(midtop=(self.screen.get_width() // 2, text_rect.bottom + 20))
            self.screen.blit(winner_name_text, text_rect)
            self.screen.blit(winner_image, image_rect)

            # Affichage des boutons
            self.retour_button.draw(self.screen, outline=(255, 255, 255))
            self.new_game_button.draw(self.screen, outline=(255, 255, 255))
            self.change_perso_button.draw(self.screen, outline=(255, 255, 255))

            pygame.display.flip()
