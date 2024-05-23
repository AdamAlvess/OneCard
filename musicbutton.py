from button import Button

class MusicButton(Button):
    def __init__(self, x, y, width, height, text, text_color, button_color):
        super().__init__(x, y, width, height, text, text_color, button_color)

    def action(self):
        print("Action: Gestion de la musique")
        self.play_sound()  # Joue le son de clic
    
    def update_color(self, button_color, text_color):
        self.button_color = button_color
        self.text_color = text_color