import random

from .trophy import Trophy
from .card import Card
from .tray import Tray


class Player:
    def __init__(self, id: int, name: str = ""):
        self.id = id
        self.name = name

        self.deck: list[Card] = []
        self.exhaust: list[Card] = []

        self.trophies: list[Trophy] = []
        self.fans = 0

        self.tournament_plan: list[int] = []

    def get_total_fans(self) -> int:
        total_fans = self.fans
        for trophy in self.trophies:
            total_fans += trophy.fans
        return total_fans

    def get_starter_cards(self): ...

    def draw_card(self, tray: Tray) -> Card:
        card = tray.draw()
        self.deck.append(card)
        return card

    def shuffle_deck(self):
        random.shuffle(self.deck)
