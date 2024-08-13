from .player import Player
from .park import Park


NUMBER_OF_ROUNDS = 8
MAX_NUMBER_OF_PLAYERS = 8


class Tournament:
    def __init__(self, number_of_players: int):
        if 0 < number_of_players <= MAX_NUMBER_OF_PLAYERS:
            self.number_of_players = number_of_players

            self.players: list[Player] = []
            self.parks: list[Park] = [Park(i) for i in range((self.number_of_players + 1) // 2)]

            self.active_round = 0
        else:
            raise ValueError

    def set_new_player(self, player: Player):
        if len(self.players) < self.number_of_players:
            self.players.append(player)
            return self.players
        return None
