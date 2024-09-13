from .components import (
    Interface,
    Button,
)
from .game import (
    ParkBoard,
    CardBack,
)


class BattleScreen(Interface):
    def __init__(self):
        self.park = ParkBoard(5, 5)

        self.player_deck = CardBack(1400, 100)
        self.draw_card_button = Button(1400, 300, "Draw")

        self.opponent_deck = CardBack(1400, 500)

        super().__init__([self.park, self.player_deck, self.draw_card_button, self.opponent_deck])
