import pygame


from .components import Button, TextField


class MenuScreen:
    def __init__(self):
        self.enter_server_button: Button = Button(10, 10, "Enter server")
        self.leave_server_button: Button = Button(300, 10, "leave server")
        self.ready_button: Button = Button(10, 300, "Ready")
        self.player_name_text_field: TextField = TextField(300, 300, "Type your name here")

        self.buttons: list[Button] = [
            self.enter_server_button,
            self.leave_server_button,
            self.ready_button,
            self.player_name_text_field,
        ]

    def draw(self, window: pygame.Surface):
        for button in self.buttons:
            button.draw(window)
