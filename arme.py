 
import pygame

class Arme:
    def __init__(self, nom, degats, image_path):
        self.nom = nom
        self.degats = degats
        self.image_original = pygame.image.load(image_path).convert_alpha()
        self.image_resized = pygame.transform.scale(self.image_original, (50, 50))

    @property
    def image(self):
        return self.image_resized
