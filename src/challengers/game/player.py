from .trophy import Trophy
from .card import Card, CardList
from .tray import Tray


class Player:
    def __init__(self, id: int, name: str = ""):
        self.id = id
        self.name = name

        self.deck = CardList()
        self.exhaust = CardList()

        self.trophies: list[Trophy] = []
        self.fans = 0

        self.tournament_plan: list[int] = []

        self.played_cards = CardList()
        self.used_cards = CardList()
        self.bench: dict[Card, int] = {}

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

    def get_starter_cards(self, tray: Tray) -> CardList:
        for card in tray.pile:
            if card not in self.deck:
                self.deck.append(card)

        for card in self.deck:
            tray.pile.remove(card)

        self.shuffle_deck()
        return self.deck

    def get_higher_round_win(self) -> int:
        if not self.trophies:
            return 0
        else:
            return self.trophies[-1].round

    def draw(self, tray: Tray) -> Card:
        card = tray.draw()
        if card:
            self.deck.append(card)
        return card

    def discard(self, card: Card, tray: Tray) -> Card:
        if card in self.deck:
            tray.discard.append(card)
            self.deck.remove(card)
            return card

    def shuffle_deck(self):
        self.deck.shuffle()

    def play(self) -> Card:
        played_card = self.deck.draw()
        if played_card:
            self.played_cards.append(played_card)
            return played_card

    def get_power(self) -> int:
        total_power = 0
        for card in self.played_cards:
            total_power += card.power
        return total_power

    def get_score(self) -> int:
        # Factors 1, 10, 100 are to have a coherent score that reflects independently all this criteria in one integer
        fans = self.get_total_fans() * 100
        max_trophies = len(self.trophies) * 10
        # 0 is added in case the player did not win any round, to avoid error with 'max' method
        max_round = max([trophy.round for trophy in self.trophies] + [0])

        return fans + max_trophies + max_round

    def bench_cards(self):
        for card in self.played_cards + self.used_cards:
            if card in self.bench:
                self.bench[card] += 1
            else:
                self.bench[card] = 1

        self.played_cards.clear()
        self.used_cards.clear()

    def set_defense(self):
        for card in self.played_cards[:-1]:
            self.used_cards.append(card)
            self.played_cards.remove(card)

    def reset_deck(self) -> CardList:
        list_bench = CardList()
        for card in self.bench:
            for _ in range(self.bench[card]):
                list_bench.append(card)

        for card in self.exhaust + self.used_cards + self.played_cards + list_bench:
            self.deck.append(card)

        self.exhaust.clear()
        self.used_cards.clear()
        self.played_cards.clear()
        self.bench = {}

        self.shuffle_deck()
        return self.deck
