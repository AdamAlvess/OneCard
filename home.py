import pygame
import sys
from assets.couleur import Couleur
from assets.couleur import SetupPygame
from option_page import OptionPage
from retourbutton import RetourButton

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 1280
SCREEN_HEIGHT = 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("One Card")

background_image = pygame.image.load("assets/back_home.jpg").convert()

font = pygame.font.SysFont(None, 36)

# Load music at program start
music_loaded = False
music_path = "assets/Musique_onepiece.wav"  # Update with your music file path
nb = 0

# Create retour_button instance
retour_button = RetourButton(250, 20, 200, 50, "Retour", Couleur.BLACK, Couleur.GRIS)

def load_music():
    global music_loaded
    if not music_loaded:
        pygame.mixer.music.load(music_path)
        music_loaded = True

def play_music():
    if not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)  # Play in loop

def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

def main_menu(retour_button):
    global music_loaded, nb
    
    load_music()  # Ensure music is loaded
    
    if nb == 0:
        play_music()  # Start or resume music playback

    while True:
        screen.blit(background_image, (0, 0))

        draw_text("Meilleur score: 1000", font, Couleur.WHITE, screen, SCREEN_WIDTH - 300, 650)

        play_button = pygame.Rect(500, 250, 200, 50)
        pygame.draw.rect(screen, Couleur.GRIS, play_button)
        draw_text("PLAY", font, Couleur.BLACK, screen, 560, 265)

        options_button = pygame.Rect(500, 350, 200, 50)
        pygame.draw.rect(screen, Couleur.GRIS, options_button)
        draw_text("OPTIONS", font, Couleur.BLACK, screen, 540, 365)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos

                if play_button.collidepoint(mouse_pos):
                    print("Lancement du jeu...")
                    retour_button.action() 
                    # Handle game logic here (switch screens, etc.)
                    return "select_player"
                elif options_button.collidepoint(mouse_pos):
                    print("Aller à l'écran des options...")
                    nb = nb + 1
                    print(nb)
                    retour_button.action() 
                    return "option"
                
        pygame.display.update()


if __name__ == "__main__":
    screen, _ = SetupPygame.initialize()
    while True:
        next_screen = main_menu(retour_button)
        if next_screen == "option":
            # Don't restart music here, it's already handled in main_menu
            option_page = OptionPage(screen)
            next_screen = option_page.show_options()
            if next_screen == "home":
                continue  # Retour à la page d'accueil
            break
