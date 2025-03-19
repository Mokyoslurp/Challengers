from .components import (
    Interface,
)
from .game import (
    CardBack,
    Deck,
)


class DeckManagementScreen(Interface):
    def __init__(self):
        self.self_deck = []

        self.tray_A = CardBack(10, 100)
        self.tray_B = CardBack(210, 100)
        self.tray_C = CardBack(410, 100)

        self.deck = Deck(10, 400)

        super().__init__([self.tray_A, self.tray_B, self.tray_C, self.deck])
