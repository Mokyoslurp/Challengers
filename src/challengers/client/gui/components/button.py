import pygame


class Button:
    def __init__(
        self,
        x: int,
        y: int,
        text: str = "",
        color=(0, 0, 0),
        height: int = 150,
        width: int = 150,
        font: str = "comicsans",
        font_size: str = 20,
    ):
        self.text = text
        self.x = x
        self.y = y
        self.color = color
        self.width = width
        self.height = height
        self.font = font
        self.font_size = font_size

    def draw(self, window: pygame.Surface):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height))
        font = pygame.font.SysFont(self.font, self.font_size)
        text = font.render(self.text, 1, (255, 255, 255))
        # Center text
        window.blit(
            text,
            (
                self.x + round(self.width / 2) - round(text.get_width() / 2),
                self.y + round(self.height / 2) - round(text.get_height() / 2),
            ),
        )

    def click(self, position) -> bool:
        x1 = position[0]
        y1 = position[1]
        if self.x <= x1 <= self.x + self.width and self.y <= y1 <= self.y + self.height:
            return True
        else:
            return False
