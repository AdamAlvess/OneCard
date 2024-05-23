import sys
import time
import pygame
import random
from perso import Perso
from barre_vie import Barre_vie
from arme import Arme
from end_game_screen import EndGameScreen

class Play:
    def __init__(self, screen, joueur1, joueur2, perso_images, ser):
        pygame.init()
        SCREEN_WIDTH = 1280
        SCREEN_HEIGHT = 720
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("One Card")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.map_images = ["assets/map1.jpg", "assets/map2.jpg", "assets/map3.jpg"]
        self.background_image = pygame.image.load(random.choice(self.map_images)).convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.perso_images = perso_images 
        start_y_player1 = SCREEN_HEIGHT - 200
        start_y_player2 = SCREEN_HEIGHT - 200
        self.personnage_joueur1 = Perso(joueur1.perso, self.scale_image(self.perso_images[joueur1.perso]), y=start_y_player1)
        self.personnage_joueur2 = Perso(joueur2.perso, self.scale_image(self.perso_images[joueur2.perso]), y=start_y_player2) 
        self.personnage_joueur1.x = 50  
        self.personnage_joueur1.y = SCREEN_HEIGHT - 200 
        self.personnage_joueur2.x = SCREEN_WIDTH - 150  
        self.personnage_joueur2.y = SCREEN_HEIGHT - 200  
        self.health_bar_joueur1 = Barre_vie(self.personnage_joueur1.pv_max, (20, 50))
        self.health_bar_joueur2 = Barre_vie(self.personnage_joueur2.pv_max, (760, 50))
        self.time_left = 300
        self.last_time_update = pygame.time.get_ticks()
        self.key_states = {}
        self.arme1 = Arme("Lance_rocket", 25, "assets/arme1.png")
        self.arme2 = Arme("Pistolet", 10, "assets/arme2.png")
        self.arme3 = Arme("Dial", 15, "assets/arme3.png")
        self.weapons = []
        self.last_weapon_spawn = pygame.time.get_ticks()
        self.first_spawn = False
        self.bullets = []
        self.ser = ser  # Ajoutez cette ligne pour initialiser l'attribut ser

        
    def start_new_game(self, joueur1, joueur2, perso_images):  # Ajoutez self comme premier paramètre
        # Créez une instance de la classe Play pour démarrer une nouvelle partie
        game = Play(self.screen, joueur1, joueur2, perso_images)
        # Lancez la partie
        game.run()

    def scale_image(self, image):
        return pygame.transform.scale(image, (100, 100))

    def scale_weapon_image(self, image):
        return pygame.transform.scale(image, (50, 50))
    
    def fire_bulletJ1(self):
        if self.personnage_joueur1.arme:
            bullet_image = pygame.image.load("assets/tire.png").convert_alpha()
            bullet_x = self.personnage_joueur1.x + self.personnage_joueur1.image.get_width() // 2
            bullet_y = self.personnage_joueur1.y + self.personnage_joueur1.image.get_height() // 2
            bullet_speed = 10
            self.bullets.append((bullet_image, bullet_x, bullet_y, bullet_speed, self.personnage_joueur1))  # Ajoutez une référence au tireur

    def fire_bulletJ2(self):
        if self.personnage_joueur2.arme:
            bullet_image = pygame.image.load("assets/tire.png").convert_alpha()
            bullet_x = self.personnage_joueur2.x + self.personnage_joueur2.image.get_width() // 2
            bullet_y = self.personnage_joueur2.y + self.personnage_joueur2.image.get_height() // 2
            bullet_speed = -10
            self.bullets.append((bullet_image, bullet_x, bullet_y, bullet_speed, self.personnage_joueur2))  # Ajoutez une référence au tireur

            
    def run(self):
        nb = 0
        running = True
        while running:
            joystick_data = self.read_joystick_data()
            if joystick_data:
                x1, y1, x2, y2, btn1, btn2, btn3, btn4, btn5, btn6 = joystick_data

                # Gérer les actions en fonction des valeurs des axes et des boutons
                if btn2 == 0:  # Bouton 1 du joystick 1 pressé
                    self.fire_bulletJ1()
                if btn5 == 0:  # Bouton 2 du joystick 1 pressé
                    self.fire_bulletJ2()

                # Déplacer le joueur 1
                if btn1 == 0:  # Joystick 1 haut
                    self.personnage_joueur1.deplacer_haut()
                if x1 < 400:  # Joystick 1 gauche
                    self.personnage_joueur1.deplacer_gauche()
                    time.sleep(0.001)
                elif x1 > 600:  # Joystick 1 droite
                    self.personnage_joueur1.deplacer_droite()
                    time.sleep(0.001)

                # Déplacer le joueur 2
                if btn4 == 0:  # Joystick 2 haut
                    self.personnage_joueur2.deplacer_haut()
                if x2 < 400:  # Joystick 2 gauche
                    self.personnage_joueur2.deplacer_gauche()
                    time.sleep(0.001)
                elif x2 > 600:  # Joystick 2 droite
                    self.personnage_joueur2.deplacer_droite()
                    time.sleep(0.001)

            print(nb)
            nb = nb + 1
            time.sleep(0.001)
            self.move_characters()
            self.personnage_joueur1.update_jump()
            self.personnage_joueur2.update_jump()
            self.detect_collision()
            self.spawn_random_weapon()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(30)



    def move_characters(self, SCREEN_WIDTH=1280):
        # Déplacer le joueur 1
        if self.key_states.get(pygame.K_z):
            self.personnage_joueur1.deplacer_haut()
        if self.key_states.get(pygame.K_q):
            if self.personnage_joueur1.x > 0:  
                self.personnage_joueur1.deplacer_gauche()
                
        if self.key_states.get(pygame.K_d):
            if self.personnage_joueur1.x < SCREEN_WIDTH - self.personnage_joueur1.image.get_width(): 
                self.personnage_joueur1.deplacer_droite()

        # Déplacer le joueur 2
        if self.key_states.get(pygame.K_UP):
            self.personnage_joueur2.deplacer_haut()
        if self.key_states.get(pygame.K_LEFT):
            if self.personnage_joueur2.x > 0: 
                self.personnage_joueur2.deplacer_gauche()
        if self.key_states.get(pygame.K_RIGHT):
            if self.personnage_joueur2.x < SCREEN_WIDTH - self.personnage_joueur2.image.get_width(): 
                self.personnage_joueur2.deplacer_droite()
                
    def check_victory(self):
        if self.personnage_joueur1.pv <= 0:
            return self.joueur2
        elif self.personnage_joueur2.pv <= 0:
            return self.joueur1
        return None

    def update(self, SCREEN_HEIGHT=720, SCREEN_WIDTH=1280):
        from home import main_menu
        import end_game_screen
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_time_update >= 1000: 
            self.time_left -= 1
            self.last_time_update = current_time
               
        winner = self.check_victory()
        if winner:
            end_screen = EndGameScreen(self.screen, winner, self.joueur1, self.joueur2, self.perso_images, self.ser)
            end_screen.run()
            main_menu()
            pygame.quit()
            self.start_new_game(self.joueur1, self.joueur2, self.perso_images)  # Lancer une nouvelle partie

            sys.exit()
        
        if self.time_left == 0:
            main_menu()
            pygame.quit()
            sys.exit()
        
            
        updated_weapons = []
        for weapon, x, y in self.weapons:
            if y < SCREEN_HEIGHT - 200:  
                y += 5
            updated_weapons.append((weapon, x, y))
        
        self.weapons = [(weapon, x, y) for (weapon, x, y) in updated_weapons if y <= SCREEN_HEIGHT]

        updated_bullets = []
        for bullet in self.bullets:
            bullet_image, bullet_x, bullet_y, bullet_speed, shooter = bullet
            bullet_x += bullet_speed  
            updated_bullets.append((bullet_image, bullet_x, bullet_y, bullet_speed, shooter))
        
        self.bullets = [(bullet_image, bullet_x, bullet_y, bullet_speed, shooter) for (bullet_image, bullet_x, bullet_y, bullet_speed, shooter) in updated_bullets if bullet_x <= SCREEN_WIDTH]

    def spawn_random_weapon(self, SCREEN_WIDTH=1280):
        current_time = pygame.time.get_ticks()
        if not self.first_spawn and current_time - self.last_weapon_spawn >= 10000:
            random_weapon = random.choice([self.arme1, self.arme2, self.arme3])
            x_position = random.randint(0, SCREEN_WIDTH - random_weapon.image.get_width())
            y_position = -random_weapon.image.get_height()
            self.weapons.append((random_weapon, x_position, y_position))
            self.last_weapon_spawn = current_time
            self.first_spawn = True  
        elif self.first_spawn and current_time - self.last_weapon_spawn >= 30000:
            random_weapon = random.choice([self.arme1, self.arme2, self.arme3])
            x_position = random.randint(0, SCREEN_WIDTH - random_weapon.image.get_width())
            y_position = -random_weapon.image.get_height()
            self.weapons.append((random_weapon, x_position, y_position))
            self.last_weapon_spawn = current_time
    
    def detect_collision(self):
        player1_rect = pygame.Rect(self.personnage_joueur1.x, self.personnage_joueur1.y, self.personnage_joueur1.image.get_width(), self.personnage_joueur1.image.get_height())
        player2_rect = pygame.Rect(self.personnage_joueur2.x, self.personnage_joueur2.y, self.personnage_joueur2.image.get_width(), self.personnage_joueur2.image.get_height())

        # Vérification des collisions avec les armes
        for weapon, x, y in self.weapons:
            weapon_rect = pygame.Rect(x, y, weapon.image.get_width(), weapon.image.get_height())
            if player1_rect.colliderect(weapon_rect):
                self.personnage_joueur1.arme = weapon
                self.weapons.remove((weapon, x, y))
                break
            if player2_rect.colliderect(weapon_rect):
                self.personnage_joueur2.arme = weapon
                self.weapons.remove((weapon, x, y))
                break

        # Vérification des collisions avec les bullets
        bullets_to_remove = []
        for bullet in self.bullets:
            bullet_image, bullet_x, bullet_y, bullet_speed, shooter = bullet
            bullet_rect = pygame.Rect(bullet_x, bullet_y, bullet_image.get_width(), bullet_image.get_height())
            
            if bullet_rect.colliderect(player1_rect) and shooter != self.personnage_joueur1:
                if shooter.arme:
                    self.personnage_joueur1.perdre_pv(shooter.arme.degats)  # Appliquer les dégâts à player1
                bullets_to_remove.append(bullet)
            
            if bullet_rect.colliderect(player2_rect) and shooter != self.personnage_joueur2:
                if shooter.arme:
                    self.personnage_joueur2.perdre_pv(shooter.arme.degats)  # Appliquer les dégâts à player2
                bullets_to_remove.append(bullet)

        # Supprimer les bullets qui ont touché un joueur
        for bullet in bullets_to_remove:
            self.bullets.remove(bullet)


    def draw(self):
        SCREEN_WIDTH = self.screen.get_width()
        SCREEN_HEIGHT = self.screen.get_height()
        self.screen.blit(self.background_image, (0, 0))
        


        # Affichage des noms des joueurs
        text_joueur1 = self.font.render(self.personnage_joueur1.nom, True, (255, 255, 255))
        self.screen.blit(text_joueur1, (20, 20))
        text_joueur2 = self.font.render(self.personnage_joueur2.nom, True, (255, 255, 255))
        text_joueur2_width = text_joueur2.get_width()
        self.screen.blit(text_joueur2, (self.screen.get_width() - 20 - text_joueur2_width, 20))

        # Mise à jour et affichage des barres de vie
        self.health_bar_joueur1.update(self.personnage_joueur1.pv)
        self.health_bar_joueur2.update(self.personnage_joueur2.pv)
        self.health_bar_joueur1.draw(self.screen)
        self.health_bar_joueur2.draw(self.screen)

        # Affichage du temps restant
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        time_text = self.font.render(f"{minutes:02}:{seconds:02}", True, (255, 255, 255))
        text_rect = time_text.get_rect(center=(640, 50))
        self.screen.blit(time_text, text_rect)

        self.draw_characters_with_weapons()

        for bullet in self.bullets:
            bullet_image, bullet_x, bullet_y, bullet_speed, shooter = bullet
            self.screen.blit(bullet_image, (bullet_x, bullet_y))

    def draw_characters_with_weapons(self):
        from home import SCREEN_HEIGHT, SCREEN_WIDTH

        # Dessiner le joueur 1 avec son arme assignée
        x_position_joueur1 = max(0, min(self.personnage_joueur1.x, SCREEN_WIDTH - self.personnage_joueur1.image.get_width()))
        y_position_joueur1 = max(0, min(self.personnage_joueur1.y, SCREEN_HEIGHT - self.personnage_joueur1.image.get_height()))
        if self.joueur1.perso:
            self.screen.blit(self.perso_images[self.joueur1.perso], (x_position_joueur1, y_position_joueur1))
        if self.personnage_joueur1.arme:
            weapon_image = self.scale_weapon_image(self.personnage_joueur1.arme.image)
            weapon_width, weapon_height = weapon_image.get_size()
            weapon_x = x_position_joueur1 + (self.personnage_joueur1.image.get_width() // 2) - (weapon_width // 2)
            weapon_y = y_position_joueur1 + (self.personnage_joueur1.image.get_height() // 2) - (weapon_height // 2)
            self.screen.blit(weapon_image, (weapon_x, weapon_y))

        # Dessiner le joueur 2 avec son arme assignée
        x_position_joueur2 = self.personnage_joueur2.x
        y_position_joueur2 = self.personnage_joueur2.y
        if self.joueur2.perso:
            self.screen.blit(self.perso_images[self.joueur2.perso], (x_position_joueur2, y_position_joueur2))
        if self.personnage_joueur2.arme:
            weapon_image = self.scale_weapon_image(self.personnage_joueur2.arme.image)
            weapon_width, weapon_height = weapon_image.get_size()
            weapon_x = x_position_joueur2 + (self.personnage_joueur2.image.get_width() // 2) - (weapon_width // 2)
            weapon_y = y_position_joueur2 + (self.personnage_joueur2.image.get_height() // 2) - (weapon_height // 2)
            self.screen.blit(weapon_image, (weapon_x, weapon_y))

        # Dessiner les armes restantes
        for weapon, x, y in self.weapons:
            scaled_weapon_image = self.scale_weapon_image(weapon.image)
            self.screen.blit(scaled_weapon_image, (x, y))

    def read_joystick_data(self):  # Ajoutez self comme premier argument
        try:
            data = self.ser.readline().decode('utf-8').strip()  # Utilisez self.ser pour accéder à l'attribut ser
            if data:
                x1, y1, x2, y2, btn1, btn2, btn3, btn4, btn5, btn6 = map(int, data.split(','))
                return x1, y1, x2, y2, btn1, btn2, btn3, btn4, btn5, btn6
        except:
            return None

    def handle_joystick_input(self):
        from home import STATE_HOME
        joystick_data = self.read_joystick_data()
        if joystick_data:
            x1, y1, x2, y2, btn1, btn2, btn3, btn4, btn5, btn6 = joystick_data

            # Gérer le mouvement vers le haut ou le bas du joystick 1
            if y1 > 600:  # Joystick bas
                self.joystick1_index = (self.joystick1_index + 1) % (len(self.perso_images) // 2 + 2)
            elif btn1 == 0:  # Joystick haut
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
                        play_page = Play(self.screen, self.joueur1, self.joueur2, self.perso_images)
                        self.retour_button.action()
                        play_page.run()
                        return

            # Gérer le mouvement vers le haut ou le bas du joystick 2
            if y2 > 600:  # Joystick bas
                self.joystick2_index = (self.joystick2_index + 1) % (len(self.perso_images) // 2 + 2)
            elif btn4 == 0:  # Joystick haut
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
                        play_page = Play(self.screen, self.joueur1, self.joueur2, self.perso_images)
                        self.retour_button.action()
                        play_page.run()
                        return
