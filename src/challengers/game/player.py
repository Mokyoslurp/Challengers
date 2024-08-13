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

        self.played_cards: list[Card] = []
        self.used_cards: list[Card] = []
        self.bench: dict[int, list[Card]] = {}

    def __str__(self):
        string = "Player " + str(self.id) + ", " + self.name + ":\n\t"
        string += "Total fans: " + str(self.get_total_fans()) + "\n"
        string += "\n\tDeck:\n\t\t"
        for card in self.deck:
            string += str(card).replace("\n", "\n\t\t") + "\n\t\t"
        string += "\n\tExhaust:\n\t\t"
        for card in self.exhaust:
            string += str(card).replace("\n", "\n\t\t") + "\n\t\t"
        string += "\n\tBench:\n\t\t"
        for card in self.bench:
            string += str(card).replace("\n", "\n\t\t") + "\n\t\t"
        return string

    def get_total_fans(self) -> int:
        total_fans = self.fans
        for trophy in self.trophies:
            total_fans += trophy.fans
        return total_fans

    def get_starter_cards(self): ...

    def get_higher_round_win(self) -> int:
        if not self.trophies:
            return 0
        else:
            return self.trophies[-1].round

    def draw_card(self, tray: Tray) -> Card:
        card = tray.draw()
        self.deck.append(card)
        return card

    def shuffle_deck(self):
        random.shuffle(self.deck)

    def play_card(self) -> Card:
        played_card = self.deck.pop()
        self.played_cards.append(played_card)
        return played_card

    def get_power(self) -> int:
        total_power = 0
        for card in self.played_cards:
            total_power += card.power
        return total_power

    def bench_cards(self):
        for card in self.played_cards + self.used_cards:
            if card.id in self.bench:
                self.bench[card.id].append(card)
            else:
                self.bench[card.id] = [card]
        self.played_cards = []

    def set_defense(self):
        for _ in range(len(self.played_cards) - 1):
            self.used_cards.append(self.played_cards.pop(0))

    def reset_deck(self) -> list[Card]:
        list_bench = []
        for card_id in self.bench:
            list_bench += self.bench[card_id]

        for card in self.exhaust + self.used_cards + self.played_cards + list_bench:
            self.deck.append(card)

        self.exhaust = []
        self.used_cards = []
        self.played_cards = []
        self.bench = {}

        self.shuffle_deck()
        return self.deck
