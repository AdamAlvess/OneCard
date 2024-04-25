import sys
import pygame
import random
from perso import Perso
from barre_vie import Barre_vie

class Play:
    def __init__(self, screen, joueur1, joueur2, perso_images):
        pygame.init()
        SCREEN_WIDTH = 1280
        SCREEN_HEIGHT = 720
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("One Card")
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        self.map_images = ["assets/map1.jpg", "assets/map2.jpg", "assets/map3.jpg"]
        self.background_image = pygame.image.load(random.choice(self.map_images)).convert()
        self.background_image = pygame.transform.scale(self.background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.joueur1 = joueur1
        self.joueur2 = joueur2
        self.perso_images = perso_images  
        self.personnage_joueur1 = Perso(joueur1.perso)
        self.personnage_joueur2 = Perso(joueur2.perso)
        self.personnage_joueur1.x = 50  
        self.personnage_joueur1.y = SCREEN_HEIGHT - 200 
        self.personnage_joueur2.x = SCREEN_WIDTH - 150  
        self.personnage_joueur2.y = SCREEN_HEIGHT - 200  
        self.health_bar_joueur1 = Barre_vie(self.personnage_joueur1.pv_max, (20, 50))
        self.health_bar_joueur2 = Barre_vie(self.personnage_joueur2.pv_max, (760, 50))
        self.time_left = 300
        self.last_time_update = pygame.time.get_ticks()
        self.key_states = {}

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    self.key_states[event.key] = True 
                elif event.type == pygame.KEYUP:
                    self.key_states[event.key] = False 
            self.move_characters() 
            self.personnage_joueur1.update_jump() 
            self.personnage_joueur2.update_jump() 
            self.draw()
            self.update()
            pygame.display.flip()
            self.clock.tick(30)


    def move_characters(self):
    # Déplacer le joueur 1
        if self.key_states.get(pygame.K_z):
            self.personnage_joueur1.deplacer_haut()
        if self.key_states.get(pygame.K_q):
            self.personnage_joueur1.deplacer_gauche()
        if self.key_states.get(pygame.K_d):
            self.personnage_joueur1.deplacer_droite()

        # Déplacer le joueur 2
        if self.key_states.get(pygame.K_UP):
            self.personnage_joueur2.deplacer_haut()
        if self.key_states.get(pygame.K_LEFT):
            self.personnage_joueur2.deplacer_gauche()
        if self.key_states.get(pygame.K_RIGHT):
            self.personnage_joueur2.deplacer_droite()

    def update(self):
        from home import main_menu
        current_time = pygame.time.get_ticks()
        if current_time - self.last_time_update >= 1000: 
            self.time_left -= 1
            self.last_time_update = current_time
        if self.time_left == 0:
            main_menu() 
            pygame.quit()
            sys.exit()

    def draw(self):
        self.screen.blit(self.background_image, (0, 0))
        text_joueur1 = self.font.render(self.personnage_joueur1.nom, True, (255, 255, 255))
        self.screen.blit(text_joueur1, (20, 20))
        text_joueur2 = self.font.render(self.personnage_joueur2.nom, True, (255, 255, 255))
        self.screen.blit(text_joueur2, (self.screen.get_width() - 20 - text_joueur2.get_width(), 20))
        
        self.health_bar_joueur1.update(self.personnage_joueur1.pv)
        self.health_bar_joueur2.update(self.personnage_joueur2.pv)
        self.health_bar_joueur1.draw(self.screen)
        self.health_bar_joueur2.draw(self.screen)

        minutes = self.time_left // 60
        seconds = self.time_left % 60
        time_text = self.font.render(f"{minutes:02}:{seconds:02}", True, (255, 255, 255))
        text_rect = time_text.get_rect(center=(640, 50))
        self.screen.blit(time_text, text_rect)
        
        x_position_joueur1 = self.personnage_joueur1.x
        y_position_joueur1 = self.personnage_joueur1.y
        x_position_joueur2 = self.personnage_joueur2.x
        y_position_joueur2 = self.personnage_joueur2.y
        
        if self.joueur1.perso:
            self.screen.blit(self.perso_images[self.joueur1.perso], (x_position_joueur1, y_position_joueur1))
        if self.joueur2.perso:
            self.screen.blit(self.perso_images[self.joueur2.perso], (x_position_joueur2, y_position_joueur2))
