from . import Button

CHAR_LIMIT = 16


class TextField(Button):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.active_typing = False
        self.is_empty = True
        self.empty_text = self.text

    def add_char(self, char: str):
        if len(self.text) < CHAR_LIMIT and self.active_typing:
            self.text += char
            self.is_empty = False

    def del_char(self):
        if len(self.text) > 0 and self.active_typing:
            self.text = self.text[:-1]
        if self.text == "":
            self.is_empty = True

    def click(self, position) -> bool:
        x1 = position[0]
        y1 = position[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            if self.is_empty:
                self.text = ""
            return True
        else:
            if self.is_empty:
                self.text = self.empty_text
            return False
