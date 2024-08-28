import pygame


class Text:
    def __init__(
        self,
        text: str = "",
        color=(255, 255, 255),
        font: str = "comicsans",
        font_size: str = 20,
    ):
        self.text = text
        self.color = color
        self.font = font
        self.font_size = font_size

    def draw(self, window: pygame.Surface):
        font = pygame.font.SysFont(self.font, self.font_size)
        text = font.render(self.text, 1, self.color)
        # Center text
        window.blit(
            text,
            (
                window.get_width() / 2 - text.get_width() / 2,
                window.get_height() / 2 - text.get_height() / 2,
            ),
        )
