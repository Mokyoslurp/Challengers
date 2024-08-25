from .button import Button


class MenuScreen:
    def __init__(self):
        self.enter_server_button = Button(10, 10, "Enter server")

    def draw(self):
        self.enter_server_button.draw()
