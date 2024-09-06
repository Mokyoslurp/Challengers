from .components import (
    Button,
    TextField,
    Interface,
)


class MenuScreen(Interface):
    def __init__(self):
        self.enter_server_button = Button(10, 10, "Enter server")
        self.leave_server_button = Button(300, 10, "leave server")
        self.ready_button = Button(10, 300, "Ready")
        self.player_name_text_field = TextField(300, 300, "Type your name here")

        super().__init__(
            [
                self.enter_server_button,
                self.leave_server_button,
                self.ready_button,
                self.player_name_text_field,
            ]
        )
