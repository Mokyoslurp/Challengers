from .components import (
    Interface,
)
from .game import (
    ParkBoard,
)


class BattleScreen(Interface):
    def __init__(self):
        self.park = ParkBoard(5, 5)

        super().__init__([self.park])
