import pygame
import sys
import serial
from assets.couleur import Couleur
from assets.couleur import SetupPygame
from select_player import SelectPersoPage
from option_page import OptionPage
from retourbutton import RetourButton

# Initialiser la connexion série
ser = serial.Serial('/dev/tty.usbmodem11201', 230400, timeout=1)  # Remplace par le port série correct

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

# Define button rectangles
play_button = pygame.Rect(500, 250, 200, 50)
options_button = pygame.Rect(500, 350, 200, 50)

# Define states
STATE_HOME = "home"
STATE_SELECT_PLAYER = "select_player"
STATE_OPTIONS = "options"
current_state = STATE_HOME

# Variable to track the selected button
selected_button = "play"

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

def read_joystick_data():
    try:
        data = ser.readline().decode('utf-8').strip()
        if data:
            x1, y1, x2, y2, btn1, btn2, btn3, btn4, btn5, btn6 = map(int, data.split(','))
            return x1, y1, x2, y2, btn1, btn2, btn3, btn4, btn5, btn6
    except:
        return None


def main_menu(retour_button):
    global music_loaded, nb, selected_button, current_state
    
    load_music()  # Ensure music is loaded
    
    if nb == 0:
        play_music()  # Start or resume music playback

    running = True
    while running:
        screen.blit(background_image, (0, 0))
        
        draw_text("Meilleur score: 1000", font, Couleur.WHITE, screen, SCREEN_WIDTH - 300, 650)

        # Highlight the selected button
        if selected_button == "play":
            pygame.draw.rect(screen, Couleur.BLACK, play_button)
            pygame.draw.rect(screen, Couleur.GRIS, options_button)
            draw_text("PLAY", font, Couleur.RED, screen, 560, 265)
            draw_text("OPTIONS", font, Couleur.RED, screen, 540, 365)
        elif selected_button == "options":
            pygame.draw.rect(screen, Couleur.GRIS, play_button)
            pygame.draw.rect(screen, Couleur.BLACK, options_button)
            draw_text("PLAY", font, Couleur.RED, screen, 560, 265)
            draw_text("OPTIONS", font, Couleur.RED, screen, 540, 365)

        joystick_data = read_joystick_data()
        if joystick_data:
            x1, y1, x2, y2, btn1, btn2, btn3, btn4, btn5, btn6 = joystick_data
            # Utilise les données du joystick ici
            if y1 > 600:  # Joystick down
                if selected_button == "play":
                    selected_button = "options"
            elif y1 < 400:  # Joystick up
                if selected_button == "options":
                    selected_button = "play"
            if btn1 == 0:  # Joystick button pressed
                if selected_button == "play":
                    print("Lancement du jeu...")
                    return STATE_SELECT_PLAYER
                elif selected_button == "options":
                    print("Aller à l'écran des options...")
                    nb = nb + 1
                    return STATE_OPTIONS

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                if play_button.collidepoint(pos):
                    print("Lancement du jeu...")
                    return STATE_SELECT_PLAYER
                elif options_button.collidepoint(pos):
                    print("Aller à l'écran des options...")
                    nb = nb + 1
                    return STATE_OPTIONS
        
        pygame.display.update()

if __name__ == "__main__":
    screen, _ = SetupPygame.initialize()
    option_page = OptionPage(screen, ser)  # Créer une instance de la page d'options en dehors de la boucle principale
    
    while True:
        if current_state == STATE_HOME:
            next_state = main_menu(retour_button)
            if next_state == STATE_SELECT_PLAYER:
                current_state = STATE_SELECT_PLAYER
            elif next_state == STATE_OPTIONS:
                current_state = STATE_OPTIONS
        
        elif current_state == STATE_SELECT_PLAYER:
            select_perso_page = SelectPersoPage(screen, background_image, ser)
            next_state = select_perso_page.run()
            if next_state == STATE_HOME:
                current_state = STATE_HOME
        
        elif current_state == STATE_OPTIONS:
            next_state = option_page.show_options()  # Afficher la page des options
            if next_state == STATE_HOME:
                current_state = STATE_HOME
