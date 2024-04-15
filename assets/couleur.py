import pygame

class Couleur:
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    GRIS = (183, 169, 166 )

class SetupPygame:
    @staticmethod
    def initialize():
        pygame.init()
        SCREEN_WIDTH = 1280
        SCREEN_HEIGHT = 720
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("One Card")
        background_image = pygame.image.load("assets/back_home.jpg")
        return screen, background_image