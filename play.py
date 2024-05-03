import sys
import pygame
import random
from perso import Perso
from barre_vie import Barre_vie
from arme import Arme
import math

class Play:
    def __init__(self, screen, joueur1, joueur2, perso_images):
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


            
    def throw_weapon(self, player_number, SCREEN_HEIGHT=720, SCREEN_WIDTH=1280):
        if player_number == 1:
            player = self.personnage_joueur1
        elif player_number == 2:
            player = self.personnage_joueur2
        else:
            return

        if player.arme:
            weapon = player.arme
            player.arme = None

            weapon_x = player.x + player.image.get_width() // 2
            weapon_y = player.y + player.image.get_height() // 2

            initial_velocity = 15  # Augmenter la vitesse initiale
            angle_degrees = 60      # Ajuster l'angle de lancement (plus petit angle pour une trajectoire plus plate)
            gravity = 0.8           # Gravité constante pour simuler la chute

            angle_radians = math.radians(angle_degrees)
            vx = initial_velocity * math.cos(angle_radians)
            vy = -initial_velocity * math.sin(angle_radians)

            time = 0
            while True:
                pygame.time.wait(30)
                time += 1
                weapon_x += vx
                weapon_y += vy + 0.5 * gravity * time ** 2

                # Dessiner l'arme avec l'image redimensionnée
                self.screen.blit(weapon.image, (weapon_x, weapon_y))

                if self.check_collision_with_opponent(weapon_x, weapon_y, weapon):
                    if player_number == 1:
                        opponent = self.personnage_joueur2
                    else:
                        opponent = self.personnage_joueur1
                    opponent.perdre_pv(weapon.degats)
                    break

                if weapon_y > SCREEN_HEIGHT or weapon_x > SCREEN_WIDTH:
                    break

                pygame.display.flip()




    def check_collision_with_opponent(self, x, y, weapon):
        opponent_rect = pygame.Rect(self.personnage_joueur2.x, self.personnage_joueur2.y,
                                     self.personnage_joueur2.image.get_width(), self.personnage_joueur2.image.get_height())
        weapon_rect = pygame.Rect(x, y, weapon.image.get_width(), weapon.image.get_height())
        return weapon_rect.colliderect(opponent_rect)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.key_states[event.key] = True

                    if event.key == pygame.K_a:
                        self.fire_bulletJ1()
                    elif event.key == pygame.K_m:
                        self.fire_bulletJ2()

                    elif event.key == pygame.K_e:
                        self.throw_weapon(1)  
                    elif event.key == pygame.K_p:
                        self.throw_weapon(2)  

                elif event.type == pygame.KEYUP:
                    self.key_states[event.key] = False

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

    def update(self, SCREEN_HEIGHT=720, SCREEN_WIDTH=1280):
        from home import main_menu
        current_time = pygame.time.get_ticks()
        
        if current_time - self.last_time_update >= 1000: 
            self.time_left -= 1
            self.last_time_update = current_time
        
        if self.time_left == 0:
            main_menu()
            pygame.quit()
            sys.exit()
        
        if self.personnage_joueur1.pv == 0:
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
        # Dessiner le joueur 1 avec son arme assignée
        x_position_joueur1 = self.personnage_joueur1.x
        y_position_joueur1 = self.personnage_joueur1.y
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

