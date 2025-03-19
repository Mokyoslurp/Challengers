import pygame

from challengers.client.gui.components import GUIElement
from challengers.client.gui.util import BLACK
from .constants import CARD_WIDTH


class Cross(GUIElement):
    def __init__(
        self,
        x: int,
        y: int,
        **kwargs,
    ):
        super().__init__(x=x, y=y, **kwargs)

        self.font = "comicsans"

        self.hide()
        self.unset_active()

    def draw(self, window: pygame.Surface):
        circle = pygame.draw.rect(
            window,
            color=BLACK,
            rect=(
                self.x,
                self.y,
                CARD_WIDTH / 4,
                CARD_WIDTH / 4,
            ),
            width=5,
            border_radius=(round(CARD_WIDTH / 8)),
        )

        # X
        font = pygame.font.SysFont(self.font, 30)
        text = font.render("X", 1, BLACK)
        window.blit(
            text,
            (
                self.x + circle.width / 2 - text.get_width() / 2,
                self.y + circle.height / 2 - text.get_height() / 2,
            ),
        )
