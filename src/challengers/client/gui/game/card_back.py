import pygame

from challengers.client.gui.util import BLACK, WHITE


class CardBack:
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
            rect=(self.x, self.y, CardBack.WIDTH, CardBack.HEIGHT),
            border_radius=(round(CardBack.WIDTH / 9)),
        )

        # Border
        pygame.draw.rect(
            window,
            color=BLACK,
            rect=(self.x, self.y, CardBack.WIDTH, CardBack.HEIGHT),
            width=5,
            border_radius=(round(CardBack.WIDTH / 9)),
        )

        # Drawing
        pygame.draw.polygon(
            window,
            color=BLACK,
            points=[
                (self.x + CardBack.WIDTH / 2, self.y),
                (self.x + self.WIDTH, self.y + CardBack.HEIGHT / 2),
                (self.x + CardBack.WIDTH / 2, self.y + self.HEIGHT),
                (self.x, self.y + CardBack.HEIGHT / 2),
            ],
        )
