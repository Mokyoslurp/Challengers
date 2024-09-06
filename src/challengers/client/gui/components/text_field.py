import pygame


from .button import Button

CHAR_LIMIT = 8


class TextField(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.is_active_typing = False
        self.is_empty = True
        self.empty_text = self.text

    def add_char(self, char: str):
        if len(self.text) < CHAR_LIMIT and self.is_active_typing:
            self.text += char
            self.is_empty = False

    def del_char(self):
        if len(self.text) > 0 and self.is_active_typing:
            self.text = self.text[:-1]
        if self.text == "":
            self.is_empty = True

    def click(self, position) -> bool:
        is_clicked = super().click(position)
        if is_clicked:
            self.is_active_typing = True
            if self.is_empty:
                self.text = ""
        else:
            self.is_active_typing = False
            if self.is_empty:
                self.text = self.empty_text
        return is_clicked

    def handle_event(self, event: pygame.event.Event):
        super().handle_event(event)
        if self.is_active and self.is_active_typing:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    self.del_char()
                else:
                    self.add_char(event.unicode)
            return True
        return False
