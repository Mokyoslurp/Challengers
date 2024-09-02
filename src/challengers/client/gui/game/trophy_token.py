import pygame

from challengers.client.gui.util import BLACK, WHITE
from challengers.game import Trophy


class TrophyToken:
    RADIUS = 50

    def __init__(
        self,
        x: int,
        y: int,
        fans: int = 0,
        round: int = 0,
        trophy: Trophy = None,
    ):
        self.x = x
        self.y = y

        self.fans = str(fans)
        self.round = str(round)

        if trophy:
            self.fans = str(trophy.fans)
            self.round = str(trophy.round)

        self.font = "comicsans"

    def draw(self, window: pygame.Surface):
        # Background
        pygame.draw.circle(
            window,
            color=WHITE,
            center=(self.x, self.y),
            radius=TrophyToken.RADIUS,
        )

        # Border
        pygame.draw.circle(
            window,
            color=BLACK,
            center=(self.x, self.y),
            radius=TrophyToken.RADIUS,
            width=5,
        )

        # Delimiter
        line_length = (4 * 1.4 / 3) * TrophyToken.RADIUS
        pygame.draw.line(
            window,
            color=BLACK,
            start_pos=(self.x - line_length / 2, self.y + TrophyToken.RADIUS / 3),
            end_pos=(self.x + line_length / 2, self.y + TrophyToken.RADIUS / 3),
            width=5,
        )

        # Fans text
        font = pygame.font.SysFont(self.font, 40)
        text = font.render(self.fans, 1, BLACK)
        window.blit(
            text,
            (
                self.x - text.get_width() / 2,
                self.y - TrophyToken.RADIUS * (1 / 3) - text.get_height() / 2,
            ),
        )

        # Round text
        font = pygame.font.SysFont(self.font, 20)
        text = font.render(self.round, 1, BLACK)
        window.blit(
            text,
            (
                self.x - text.get_width() / 2,
                self.y + TrophyToken.RADIUS * (2 / 3) - text.get_height() / 2,
            ),
        )
