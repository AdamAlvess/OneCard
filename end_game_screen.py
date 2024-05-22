import pygame
import sys
from assets.couleur import Couleur

from retourbutton import RetourButton


class EndGameScreen:
    def __init__(self, screen, winner, joueur1, joueur2, perso_images, ser):
        self.screen = screen
        self.winner = winner
        self.perso_images = perso_images
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.background_image = pygame.image.load("assets/back_home.jpg").convert()
        self.ser = ser  # Ajoutez cette ligne pour initialiser l'attribut ser


        self.font = pygame.font.Font(None, 36)

        # Création des boutons
        self.retour_button = RetourButton(50, 50, 200, 50, "Retour au menu", Couleur.RED, Couleur.BLACK)
        self.new_game_button = RetourButton(50, 120, 200, 50, "Nouvelle partie", Couleur.RED, Couleur.GRIS)
        self.change_perso_button = RetourButton(50, 190, 200, 50, "Changement de personnage", Couleur.RED, Couleur.GRIS)
        self.buttons = [self.retour_button, self.new_game_button, self.change_perso_button]

        
        self.selected_button = self.retour_button  # Par défaut, le bouton Retour est sélectionné
        self.selected_button_index = 0  # Indice du bouton sélectionné par défaut
        self.ok_button_selected = False # Ajouter une variable de sélection pour le bouton "OK"
    
    

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
                
                        
            # Lire les données du joystick
            joystick_data = self.read_joystick_data()
            if joystick_data:
                x1, y1, x2, y2, btn1, btn2, btn3, btn4, btn5, btn6 = joystick_data
                # Utiliser les données du joystick ici
                if y1 > 600:  # Joystick down
                    self.move_selection(1)
                    self.update_selected_button_color()  # Met à jour la couleur des boutons après le déplacement
                elif btn3 == 0:  # Joystick up
                    self.move_selection(-1)
                    self.update_selected_button_color()  # Met à jour la couleur des boutons après le déplacement
                if btn1 == 0:  # Joystick button pressed
                    return self.select_button()

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
            
    def select_button(self):
        from play import Play
        from select_player import SelectPersoPage
        button = self.selected_button
        if button == self.retour_button:
            print("Home...")
            self.retour_button.action()
            return "home"
        elif button == self.new_game_button:
            print("Affichage nouvelle game ")
            self.retour_button.action()
            game = Play(self.screen, self.joueur1, self.joueur2, self.perso_images, self.ser)
            game.run()
        elif button == self.change_perso_button:
            print("change perso")
            self.retour_button.action()
            select_perso_page = SelectPersoPage(self.screen, self.background_image, self.ser)
            select_perso_page.run()
            
    def move_selection(self, direction):
        current_index = self.buttons.index(self.selected_button)
        new_index = (current_index + direction) % len(self.buttons)
        self.selected_button = self.buttons[new_index]

    def read_joystick_data(self):
        try:
            data = self.ser.readline().decode('utf-8').strip()
            if data:
                x1, y1, x2, y2, btn1, btn2, btn3, btn4, btn5, btn6 = map(int, data.split(','))
                return x1, y1, x2, y2, btn1, btn2, btn3, btn4, btn5, btn6
        except:
            return None
        
    def update_selected_button_color(self):
        for button in self.buttons:
            if button == self.selected_button:
                button.update_color(Couleur.BLACK, Couleur.RED)  # Met à jour la couleur du bouton sélectionné
            else:
                button.update_color(Couleur.GRIS, Couleur.RED)  # Réinitialise la couleur des autres boutons



               