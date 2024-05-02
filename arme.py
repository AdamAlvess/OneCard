from perso import Perso  
import pygame

class Arme:
    def __init__(self, nom, degats, image_path):
        self.nom = nom
        self.degats = degats
        self.image = pygame.image.load(image_path).convert_alpha()
    
    def attaquer(self, ennemi):
        ennemi.perdre_pv(self.degats)
        print(f"{ennemi.nom} a perdu {self.degats} PV après avoir été attaqué par {self.nom}.")
