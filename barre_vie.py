import pygame

class Barre_vie:
    def __init__(self, max_health, position):
        self.max_health = max_health
        self.health = max_health
        self.position = position
        self.width = 500
        self.height = 20

    def update(self, new_health):
        self.health = new_health

    def draw(self, screen):
        bar_length = (self.health / self.max_health) * self.width
        pygame.draw.rect(screen, (255, 0, 0), (self.position[0], self.position[1], self.width, self.height))
        pygame.draw.rect(screen, (0, 255, 0), (self.position[0], self.position[1], bar_length, self.height))