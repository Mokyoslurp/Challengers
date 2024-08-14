from .player import Player
from .park import Park
from .tray import Tray
from .card import Level
from .trophy import Trophy


DEBUG = True


NUMBER_OF_ROUNDS = 7
MAX_NUMBER_OF_PLAYERS = 8


ROBOT_PLAYER_NAME = "IA"


class Tournament:
    def __init__(self, number_of_players: int):
        if 0 < number_of_players <= MAX_NUMBER_OF_PLAYERS:
            self.number_of_players = number_of_players

            self.players: list[Player] = []
            self.parks: list[Park] = [Park(i) for i in range((self.number_of_players + 1) // 2)]

            self.trays: dict[Level, Tray] = {}

            self.scores: dict[Player, int] = {}
        else:
            raise ValueError

    def initialize_trays(self) -> list[Tray]:
        for level in [Level.A, Level.B, Level.C]:
            tray = Tray(level)
            tray.prepare()
            self.trays[level] = tray

        if DEBUG:
            for tray in self.trays.values():
                print(tray)

        return self.trays

    def set_new_player(self, player: Player) -> list[Player]:
        if len(self.players) < self.number_of_players:
            self.players.append(player)
            return self.players

        return None

    def get_scores(self) -> dict[Player, int]:
        for player in self.players:
            self.scores[player] = player.get_score()

        return self.scores.copy()

    def print_scores(self):
        scores = self.get_scores()

        for player in self.players:
            print(player, "\nScore = ", scores[player], "\n")

    def get_finalists(self) -> list[Player]:
        scores = self.get_scores()

        finalists: list[Player] = []
        for _ in range(2):
            max_score = max(scores.values())
            finalists.append([player for player in self.players if scores[player] == max_score][0])
            # Avoid having the first finalist counted to be also the second finalist
            scores[finalists[-1]] = -1

        return finalists

    def play(self) -> Player:
        # Set a robot player if there is an odd number of players
        if len(self.players) % 2 == 1:
            self.set_new_player(Player(0, ROBOT_PLAYER_NAME))

        if DEBUG:
            for player in self.players:
                print(player)

        for round in range(NUMBER_OF_ROUNDS):
            winners: list[Player] = [-1] * len(self.parks)
            for park in self.parks:
                # TODO: Make appropriate players assignments in parks
                park.assign_players(self.players[2 * park.id], self.players[2 * park.id + 1])

                # TODO: Launch threads for each game
                if DEBUG:
                    print("\nRound ", round, ", park ", park.id, " started.")

                winners[park.id] = park.play_game()

            for winner in winners:
                # TODO: Have a prepared list of trophies with different number of fans
                winner.trophies.append(Trophy(round, round))

            for player in self.players:
                player.reset_deck()

            # TODO: Add tray draw and deck management

        finalists = self.get_finalists()

        park = self.parks[0]
        park.assign_players(finalists[0], finalists[1])
        winner = park.play_game()

        if DEBUG:
            print(winner, " won the tournament!")

        return winner
