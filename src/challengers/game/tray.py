from .card import Level, CardList


class Tray:
    def __init__(self, level: Level):
        self.level = level

        self.pile = CardList()
        self.discard = CardList()

    def __str__(self):
        string = (
            "Tray "
            + self.level.name
            + ":\n\tPile:\n\t\t"
            + str(self.pile).replace("\n", "\n\t\t")
            + "\n\t\t"
            + "\n\tDiscard:\n\t\t"
            + str(self.discard).replace("\n", "\n\t\t")
        )
        return string

    def prepare(self, game_cards: CardList):
        for card in game_cards:
            if card.level == self.level:
                self.pile.append(card)
        self.shuffle()

    def shuffle(self):
        self.pile.shuffle()

    def draw(self):
        return self.pile.draw()
