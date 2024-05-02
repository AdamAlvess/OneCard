from button import Button

class CommandButton(Button):
    def __init__(self, x, y, width, height, text, text_color, button_color):
        super().__init__(x, y, width, height, text, text_color, button_color)

    def action(self):
        print("Action: Gestion des commandes")
        # Implémentez la logique pour gérer les commandes...
        self.play_sound()  # Joue le son de clic
