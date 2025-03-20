import pygame

from challengers.client.gui.components import GUIElement
from challengers.client.gui.util import BLACK, WHITE
from .constants import CARD_WIDTH, CARD_HEIGHT
from challengers.game import Card


class CardFront(GUIElement):
    def __init__(
        self,
        x: int,
        y: int,
        power: int = 0,
        name: str = "",
        level: str = "S",
        set: str = "City",
        text: str = "",
        card: Card = None,
        **kwargs,
    ):
        super().__init__(x=x, y=y, height=CARD_HEIGHT, width=CARD_WIDTH, **kwargs)

        self.name = name
        self.power = str(power)
        self.level = level
        self.set = set
        self.text = text

        if card:
            self.name = card.name
            self.power = str(card.power)
            self.level = card.level.name
            self.set = card.set.name.replace("_", " ").capitalize()
            self.text = card.text

        self.font = "comicsans"

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

        # Power border
        power_rect = pygame.draw.rect(
            window,
            color=BLACK,
            rect=(
                self.x + CARD_WIDTH * (3 / 4),
                self.y,
                CARD_WIDTH / 4,
                CARD_WIDTH / 4,
            ),
            width=5,
            border_radius=(round(CARD_WIDTH / 8)),
        )

        # Power text
        font = pygame.font.SysFont(self.font, 30)
        text = font.render(self.power, 1, BLACK)
        window.blit(
            text,
            (
                self.x + CARD_WIDTH * (3 / 4) + power_rect.width / 2 - text.get_width() / 2,
                self.y + power_rect.height / 2 - text.get_height() / 2,
            ),
        )

        # Name text
        font = pygame.font.SysFont(self.font, 20)
        text = font.render(self.name, 1, BLACK)
        window.blit(
            text,
            (
                self.x + CARD_WIDTH / 2 - CARD_WIDTH / 6 - text.get_width() / 2,
                self.y + CARD_HEIGHT / 10 - text.get_height() / 2,
            ),
        )

        # Set border
        set_rect = pygame.draw.rect(
            window,
            color=BLACK,
            rect=(
                self.x,
                self.y + CARD_HEIGHT * (2 / 8),
                CARD_WIDTH,
                CARD_HEIGHT / 8,
            ),
            width=5,
        )

        # Set text
        font = pygame.font.SysFont(self.font, 20)
        text = font.render(self.set, 1, BLACK)
        window.blit(
            text,
            (
                self.x + set_rect.width / 2 - text.get_width() / 2,
                self.y + CARD_HEIGHT * (2 / 8) + set_rect.height / 2 - text.get_height() / 2,
            ),
        )

        # Level border
        level_rect = pygame.draw.rect(
            window,
            color=BLACK,
            rect=(
                self.x + CARD_WIDTH * (2 / 3),
                self.y + CARD_HEIGHT * (3 / 4),
                CARD_WIDTH / 3,
                CARD_HEIGHT / 4,
            ),
            width=5,
            border_radius=(round(CARD_WIDTH / 9)),
        )

        # Level text
        font = pygame.font.SysFont(self.font, 30)
        text = font.render(self.level, 1, BLACK)
        window.blit(
            text,
            (
                self.x + CARD_WIDTH * (2 / 3) + level_rect.width / 2 - text.get_width() / 2,
                self.y + CARD_HEIGHT * (3 / 4) + level_rect.height / 2 - text.get_height() / 2,
            ),
        )

        # Text
        font = pygame.font.SysFont(self.font, 15)
        text = font.render(self.text, 1, BLACK)
        window.blit(
            text,
            pygame.Rect(
                self.x + CARD_WIDTH / 20,
                self.y + CARD_HEIGHT * (3 / 8),
                CARD_WIDTH / 2 - text.get_width() / 2,
                CARD_HEIGHT * (3 / 8)
                + (CARD_HEIGHT * (3 / 4) - CARD_HEIGHT * (3 / 8)) / 2
                - text.get_height() / 2,
            ),
        )
