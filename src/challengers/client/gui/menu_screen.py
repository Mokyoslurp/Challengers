import pygame


from .button import Button


class MenuScreen:
    def __init__(self):
        self.enter_server_button: Button = Button(10, 10, "Enter server")
        self.leave_server_button: Button = Button(300, 10, "leave server")
        self.test_button: Button = Button(10, 300, "Test")

        self.buttons: list[Button] = [
            self.enter_server_button,
            self.leave_server_button,
            self.test_button,
        ]

    def draw(self, window: pygame.Surface):
        for button in self.buttons:
            button.draw(window)
