from button import Button

class SoundButton(Button):
    def __init__(self, x, y, width, height, text, text_color, button_color):
        super().__init__(x, y, width, height, text, text_color, button_color)

    def action(self):
        print("Action: Gestion du son")