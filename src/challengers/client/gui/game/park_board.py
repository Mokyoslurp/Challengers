import pygame

from challengers.client.gui.components.gui_element import GUIElement
from challengers.client.gui.util import BLACK, WHITE
from .constants import PARK_HEIGHT, PARK_WIDTH, CARD_WIDTH, CARD_HEIGHT

from . import CardSpace, CardFront


class ParkBoard(GUIElement):
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x=x, y=y, **kwargs)

        width_spacing = (PARK_WIDTH - 6 * CARD_WIDTH) / 7

        self.benches = {
            1: [
                CardSpace(
                    self.x + width_spacing * (1 + i) + CARD_WIDTH * i,
                    self.y,
                )
                for i in range(6)
            ],
            2: [
                CardSpace(
                    self.x + width_spacing * (1 + i) + CARD_WIDTH * i,
                    self.y + PARK_HEIGHT - CARD_HEIGHT,
                )
                for i in range(6)
            ],
        }

        self.played_cards = {
            1: [
                CardSpace(
                    self.x + PARK_WIDTH / 8 - CARD_WIDTH / 2,
                    self.y + PARK_HEIGHT / 2 - CARD_HEIGHT / 2,
                )
            ],
            2: [
                CardSpace(
                    self.x + PARK_WIDTH * (7 / 8) - CARD_WIDTH / 2,
                    self.y + PARK_HEIGHT / 2 - CARD_HEIGHT / 2,
                )
            ],
        }

    def draw(self, window: pygame.Surface):
        # Background
        pygame.draw.rect(
            window,
            color=WHITE,
            rect=(self.x, self.y + CARD_HEIGHT, PARK_WIDTH, PARK_HEIGHT - 2 * CARD_HEIGHT),
            border_radius=(round(PARK_WIDTH / 9)),
        )

        # Border
        pygame.draw.rect(
            window,
            color=BLACK,
            rect=(self.x, self.y + CARD_HEIGHT, PARK_WIDTH, PARK_HEIGHT - 2 * CARD_HEIGHT),
            width=5,
            border_radius=(round(PARK_WIDTH / 9)),
        )

        for bench in self.benches.values():
            for card in bench:
                card.draw(window)

        for played_cards in self.played_cards.values():
            for card in played_cards:
                card.draw(window)

    def add_bench_card(self, player_id: int, space_id: int, card: CardFront):
        if type(self.benches[player_id][space_id]) is CardSpace:
            card.x = self.benches[player_id][space_id].x
            card.y = self.benches[player_id][space_id].y
            self.benches[player_id][space_id] = card
        else:
            # TODO: Add "x2", "x3", etc
            ...

    def add_played_card(self, player_id: int, card: CardFront):
        if (
            len(self.played_cards[player_id]) == 1
            and type(self.played_cards[player_id][0]) is CardSpace
        ):
            card.x = self.played_cards[player_id][0].x
            card.y = self.played_cards[player_id][0].y
            self.played_cards[player_id][0] = card
        else:
            # Either 1 or -1
            factor = 3 - 2 * player_id
            card.x = self.played_cards[player_id][-1].x + factor * CARD_WIDTH / 4
            card.y = self.played_cards[player_id][-1].y
            self.played_cards[player_id].append(card)

    def stack(self, player_id: int):
        card = self.played_cards[player_id][-1]
        self.played_cards[player_id] = [card]

    def reset_bench(self, player_id: int, space_id: int):
        x = self.benches[player_id][space_id].x
        y = self.benches[player_id][space_id].y
        self.benches[player_id][space_id] = CardSpace(x, y)

    def reset_played_cards(self, player_id: int):
        x = self.played_cards[player_id][0].x
        y = self.played_cards[player_id][0].y
        self.played_cards[player_id] = [CardSpace(x, y)]
