from .trophy import Trophy
from .card import Card, CardList
from .tray import Tray


class Player:
    """
    A player defined by an id and a name, who has a deck of cards
    """

    def __init__(self, id: int, name: str = "", is_robot: bool = False):
        """
        Player initialization

        :param id: player unique id
        :param name: player name, defaults to ""
        :param is_robot: True if the player is not a human and will play automatically, defaults to False
        """
        self.id = id
        self.name = name

        self.is_robot: bool = is_robot

        self.is_ready: bool = False
        self.has_played: bool = True
        self.has_managed_cards: bool = True

        self.deck = CardList()
        self.exhaust = CardList()

        self.trophies: list[Trophy] = []
        self.fans = 0

        self.played_cards = CardList()
        self.used_cards = CardList()
        self.bench: dict[Card, int] = {}

    def __str__(self):
        return self.name

    def to_string(self):
        string = (
            " P"
            + str(self.id)
            + ", "
            + self.name
            + ":\n\t"
            + "Total fans: "
            + str(self.get_total_fans())
            + "\n"
            + "\n\tDeck:\n\t\t"
            + str(self.deck).replace("\n", "\n\t\t")
            + "\n\t\t"
            + "\n\tExhaust:\n\t\t"
            + str(self.exhaust).replace("\n", "\n\t\t")
            + "\n\t\t"
            + "\n\tBench:\n\t\t"
        )
        for card in self.bench:
            string += (
                str(card).replace("\n", "\n\t\t") + ", (x" + str(self.bench[card]) + ")" + "\n\t\t"
            )
        return string

    def get_total_fans(self) -> int:
        """
        Calculates the player total fans, with the bonus fans and the fans obtained with the trophies

        :return: total fans number
        """
        total_fans = self.fans
        for trophy in self.trophies:
            total_fans += trophy.fans
        return total_fans

    def get_starter_cards(self, tray: Tray):
        """
        Draws starter cards for the player, and shuffles the deck

        :param tray: the starter tray to draw from
        """
        for card in tray.pile:
            if card not in self.deck:
                self.deck.append(card)

        for card in self.deck:
            tray.pile.remove(card)

        self.shuffle_deck()

    def get_higher_round_win(self) -> int:
        """
        Gets the higher round won by the player

        :return: the higher round won by the player
        """
        if not self.trophies:
            return 0
        else:
            return self.trophies[-1].round

    def draw(self, tray: Tray, amount: int):
        """
        Draws a card from a tray and adds it to the player deck

        :param tray: to tray to draw from
        :param amount: amount of cards to draw
        """
        if not self.has_managed_cards:
            for _ in range(amount):
                card = tray.draw()
                if card:
                    self.deck.append(card)

    def discard(self, card: Card, tray: Tray):
        """
        Discards the chosen card from the player deck into a tray's discard

        :param card: discarded card
        :param tray: tray in which to discard
        """
        if not self.has_managed_cards and card in self.deck:
            tray.discard.append(card)
            self.deck.remove(card)

    def shuffle_deck(self):
        """
        Shuffles the player deck
        """
        self.deck.shuffle()

    def play(self) -> Card:
        """
        Adds a card from deck to played cards

        :return: the played card
        """
        if not self.has_played:
            played_card = self.deck.draw()
            if played_card:
                self.played_cards.append(played_card)
                self.has_played = True
                return True
        return False

    def get_power(self) -> int:
        """
        Gets total power of the played cards

        :return: _description_
        """
        total_power = 0
        for card in self.played_cards:
            total_power += card.power
        return total_power

    def get_score(self) -> int:
        """
        Gets the player total score based on its number of trophies, fans and maximum round won.

        The score is in format XXYZ, XX being the total number of fans, Y the number of trophies
        won, and Z the number of the latest round won.

        :return: the score of the player
        """
        # Factors 1, 10, 100 are to have a coherent score that reflects independently all this criteria in one integer
        fans = self.get_total_fans() * 100
        max_trophies = len(self.trophies) * 10
        # 0 is added in case the player did not win any round, to avoid error with 'max' method
        max_round = max([trophy.round + 1 for trophy in self.trophies] + [0])

        return fans + max_trophies + max_round

    def bench_cards(self):
        """
        Moves cards from the played and used cards of the player to its bench
        """
        for card in self.played_cards + self.used_cards:
            if card in self.bench:
                self.bench[card] += 1
            else:
                self.bench[card] = 1

        self.played_cards.clear()
        self.used_cards.clear()

    def set_defense(self):
        """
        Moves all the played cards to used cards, except the last one,
        to set the player in defense phase
        """
        for card in self.played_cards[:-1]:
            self.used_cards.append(card)
            self.played_cards.remove(card)

    def reset_deck(self):
        """
        Moves all played, used, and benched cards to the deck, and shuffles it
        """
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
