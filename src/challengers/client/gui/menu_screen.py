import pygame


from .components.button import Button


class MenuScreen:
    def __init__(self):
        self.enter_server_button: Button = Button(10, 10, "Enter server")
        self.leave_server_button: Button = Button(300, 10, "leave server")
        self.test_button: Button = Button(10, 300, "Test")
        self.launch_button: Button = Button(300, 300, "Launch")

        self.add_bench_1_button: Button = Button(10, 500, "Bench 1")
        self.add_bench_2_button: Button = Button(300, 500, "Bench 2")
        self.add_played_1_button: Button = Button(10, 700, "Play 1")
        self.add_played_2_button: Button = Button(300, 700, "Play 2")

        self.reset_button: Button = Button(150, 400, "Reset")

        self.buttons: list[Button] = [
            self.enter_server_button,
            self.leave_server_button,
            self.test_button,
            self.launch_button,
            self.add_bench_1_button,
            self.add_bench_2_button,
            self.add_played_1_button,
            self.add_played_2_button,
            self.reset_button,
        ]

    def draw(self, window: pygame.Surface):
        for button in self.buttons:
            button.draw(window)
