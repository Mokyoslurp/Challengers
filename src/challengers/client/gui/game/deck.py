import pygame

from challengers.client.gui.components.gui_element import GUIElement
from .constants import CARD_WIDTH

from . import CardSpace, CardFront, Cross


class Deck(GUIElement):
    def __init__(self, x: int, y: int, **kwargs):
        super().__init__(x=x, y=y, **kwargs)

        self.cards = [
            CardSpace(x, y),
            CardSpace(x + (CARD_WIDTH + 10), y),
            CardSpace(x + 2 * (CARD_WIDTH + 10), y),
            CardSpace(x + 3 * (CARD_WIDTH + 10), y),
            CardSpace(x + 4 * (CARD_WIDTH + 10), y),
            CardSpace(x + 5 * (CARD_WIDTH + 10), y),
        ]

        self.crosses = {i: Cross(self.cards[i].x, self.cards[i].y) for i in range(len(self.cards))}

    def draw(self, window: pygame.Surface):
        for card in self.cards:
            card.draw(window)

        for cross in self.crosses.values():
            cross.draw(window)

    def add_card(self, card: CardFront):
        for i, deck_card in enumerate(self.cards):
            if type(deck_card) is CardSpace:
                card.x = deck_card.x
                card.y = deck_card.y
                self.cards[i] = card
                self.crosses[i].show()
                self.crosses[i].set_active()
                break

    def remove_card(self, i: int):
        card_space = CardSpace(self.cards[i].x, self.cards[i].y)
        self.cards[i] = card_space
        self.crosses[i].unset_active()
        self.crosses[i].hide()

    def reset(self):
        for i, card in enumerate(self.cards):
            if type(card) is CardFront:
                self.remove_card(i)
