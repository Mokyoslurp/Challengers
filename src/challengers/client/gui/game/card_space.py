import pygame

from challengers.client.gui.util import BLACK, WHITE


class CardSpace:
    HEIGHT = 300
    WIDTH = 200

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
            rect=(self.x, self.y, CardSpace.WIDTH, CardSpace.HEIGHT),
            border_radius=(round(CardSpace.WIDTH / 9)),
        )

        # Border
        pygame.draw.rect(
            window,
            color=BLACK,
            rect=(self.x, self.y, CardSpace.WIDTH, CardSpace.HEIGHT),
            width=5,
            border_radius=(round(CardSpace.WIDTH / 9)),
        )
