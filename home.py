import pygame
import sys

pygame.init()

# Définition des couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRIS = (183, 169, 166 )


SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("One Card")

background_image = pygame.image.load("assets/back_home.jpg").convert()

font = pygame.font.SysFont(None, 36)

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu():
    while True:
        screen.blit(background_image, (0, 0))

        draw_text("Meilleur score: 1000", font, WHITE, screen, SCREEN_WIDTH - 300, 650)

        play_button = pygame.Rect(500, 250, 200, 50)
        pygame.draw.rect(screen, GRIS, play_button)
        draw_text("PLAY", font, BLACK, screen, 560, 265)

        options_button = pygame.Rect(500, 350, 200, 50)
        pygame.draw.rect(screen, GRIS, options_button)
        draw_text("OPTIONS", font, BLACK, screen, 540, 365)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if play_button.collidepoint(mouse_pos):
                    print("Lancement du jeu...")

                    return
                elif options_button.collidepoint(mouse_pos):
                    print("Aller à l'écran des options...")

        pygame.display.update()

if __name__ == "__main__":
    main_menu()
