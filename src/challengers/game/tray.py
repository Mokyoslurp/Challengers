import random

from .card import Card, Level


class Tray:
    def __init__(self, level: Level):
        self.level = level

        self.pile: list[Card] = []
        self.discard: list[Card] = []

    def prepare(self):
        self.pile = []
        for card in Card.cards:
            if card.level == self.level:
                self.pile.append(card)
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.pile)

    def draw(self):
        return self.pile.pop()
