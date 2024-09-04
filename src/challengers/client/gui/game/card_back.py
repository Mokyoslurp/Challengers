import pygame

from challengers.client.gui.util import BLACK, WHITE
from .constants import CARD_HEIGHT, CARD_WIDTH


class CardBack:
    def __init__(
        self,
        x: int,
        y: int,
    ):
        self.x = x
        self.y = y

    def draw(self, window: pygame.Surface):
        # Background
        pygame.draw.rect(
            window,
            color=WHITE,
            rect=(self.x, self.y, CARD_WIDTH, CARD_HEIGHT),
            border_radius=(round(CARD_WIDTH / 9)),
        )

        # Border
        pygame.draw.rect(
            window,
            color=BLACK,
            rect=(self.x, self.y, CARD_WIDTH, CARD_HEIGHT),
            width=5,
            border_radius=(round(CARD_WIDTH / 9)),
        )

        # Drawing
        pygame.draw.polygon(
            window,
            color=BLACK,
            points=[
                (self.x + CARD_WIDTH / 2, self.y),
                (self.x + self.WIDTH, self.y + CARD_HEIGHT / 2),
                (self.x + CARD_WIDTH / 2, self.y + self.HEIGHT),
                (self.x, self.y + CARD_HEIGHT / 2),
            ],
        )
