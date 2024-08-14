import random

from .card import Card, Level


class Tray:
    def __init__(self, level: Level):
        self.level = level

        self.pile: list[Card] = []
        self.discard: list[Card] = []

    def __str__(self):
        string = "Tray " + self.level.name + ":\n\tPile:\n\t\t"
        for card in self.pile:
            string += str(card).replace("\n", "\n\t\t") + "\n\t\t"
        string += "\n\tDiscard:\n\t\t"
        for card in self.discard:
            string += str(card).replace("\n", "\n\t\t") + "\n\t\t"
        return string

    def prepare(self):
        self.pile = []
        for card in Card.cards:
            if card.level == self.level:
                self.pile.append(card)
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.pile)

    def draw(self):
        if self.pile:
            return self.pile.pop()
        else:
            return None
