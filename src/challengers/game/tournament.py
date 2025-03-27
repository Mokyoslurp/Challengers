import random
from typing import Self
from enum import Enum
import threading

from .player import Player
from .duel import Duel
from .tray import Tray
from .card import Level
from .trophy import TrophyDict, TrophySerializer
from .card import CardList, CardSerializer, Card

from .data import DEBUG

NUMBER_OF_ROUNDS = 7
MAX_NUMBER_OF_PLAYERS = 8


ROBOT_PLAYER_NAME = "IA"


class Tournament:
    class Status(Enum):
        NONE = 0
        ROUND = 1
        DECK = 2
        FINAL = 3
        PREPARE = 4

    def __init__(self, number_of_players: int):
        if 0 < number_of_players <= MAX_NUMBER_OF_PLAYERS:
            self.number_of_players = number_of_players

            self.players: list[Player] = []
            self.duels: list[Duel] = []
            # winners by duels and by rounds
            self.winners: list[list[Player]] = [[]] * NUMBER_OF_ROUNDS
            self.winner: Player

            self.status = Tournament.Status.NONE
            self.round: int = -1

            self.trays: dict[Level, Tray] = {}
            # Possible combinations of tray to draw from and number of cards
            self.available_draws: dict[Level, int] = {}

            self.scores: dict[Player, int] = {}

            self.unique_cards_list: dict[int, Card]
            self.game_cards: CardList
            self.game_trophies = TrophyDict()

            self.ended = threading.Event()

        else:
            raise ValueError

    def is_ended(self):
        return self.ended.is_set()

    def check_all_players_connected(self):
        # Addition of a robot player is possible, having then number_of_players + 1 player
        return len(self.players) >= self.number_of_players

    def check_all_players_ready(self):
        return all([player.is_ready for player in self.players])

    def check_all_duels_ended(self):
        return all([duel.is_ended() for duel in self.duels])

    def check_all_players_managed_cards(self):
        return all([player.has_managed_cards for player in self.players])

    def reset(self):
        self.players = []
        self.winners = [[]]
        self.winner = None
        self.round = -1
        self.trays = {}
        self.scores = {}
        self.game_cards = CardList()
        self.unique_cards_list = {}
        self.game_trophies = TrophyDict()

    def load_game_cards(self, game_cards_file_path: str):
        self.game_cards = CardSerializer.load_cards_from_file(game_cards_file_path)
        self.unique_cards_list = CardList.get_unique_cards_list(game_cards_file_path)

    def load_game_trophies(self, game_trophies_file_path: str):
        self.game_trophies = TrophySerializer.load_trophies_from_file(game_trophies_file_path)

    def initialize_trays(self) -> list[Tray]:
        for level in [Level.A, Level.B, Level.C, Level.S]:
            tray = Tray(level)
            tray.prepare(self.game_cards)
            self.trays[level] = tray

        return self.trays

    def add_player(self, player: Player):
        """Adds a new player to the tournament. If the last player is added
            a robot player is added if the number of players is odd.

        :param player: the player to add
        """
        if not self.check_all_players_connected():
            self.players.append(player)

            if self.check_all_players_connected():
                # Set a robot player if there is an odd number of players
                if len(self.players) % 2 == 1:
                    robot_player = Player(len(self.players), ROBOT_PLAYER_NAME, is_robot=True)
                    robot_player.is_ready = True
                    self.players.append(robot_player)

    def get_scores(self) -> dict[Player, int]:
        for player in self.players:
            self.scores[player] = player.get_score()

        return self.scores.copy()

    def print_scores(self):
        scores = self.get_scores()

        for player in self.players:
            print(player, "\nScore = ", scores[player], "\n")

    def get_duel(self, player: Player) -> Duel:
        if self.round <= NUMBER_OF_ROUNDS:
            duel_id = TournamentPlan.plans[player].duel_ids[self.round]
            duel = self.duels[duel_id]
        else:
            duel = self.duels[0]

        return duel

    def get_opponent(self, player: Player) -> Player:
        duel = self.get_duel(player)

        if duel.player_1 and duel.player_2:
            players = [duel.player_1, duel.player_2]
            if player in players:
                players.remove(player)
                return players[0]

    def get_finalists(self) -> list[Player]:
        scores = self.get_scores()

        finalists: list[Player] = []
        for _ in range(2):
            max_score = max(scores.values())
            # This will avoid the case of 3 or more players with the same score. If the list of
            # possible finalists contain more than 3, only 2 will eventually be chosen, if there
            # is less the code will have the same behavior
            possible_finalists = [player for player in self.players if scores[player] == max_score]
            finalists.append(random.choice(possible_finalists))

            # Avoid having the first finalist counted to be also the second finalist
            scores[finalists[-1]] = -1

        return finalists

    def prepare(self):
        if self.status == Tournament.Status.NONE:
            TournamentPlan.generate(self.number_of_players, self.players)

            self.initialize_trays()
            for player in self.players:
                player.get_starter_cards(self.trays[Level.S])

            self.status = Tournament.Status.ROUND

            if DEBUG:
                print("Tournament started")

    def make_draw(self, player: Player, level: Level) -> CardList:
        return player.draw(self.trays[level], self.available_draws[level])

    def prepare_cards_management(self):
        if self.status == Tournament.Status.DECK:
            self.available_draws = TournamentPlan.get_available_draws(self.round)

            if DEBUG:
                print(f"Available draws : {self.available_draws}")

            for player in self.players:
                player.reset_deck()
                player.has_managed_cards = False
                player.has_drawn = False

            if DEBUG:
                print("Players have to manage cards !")

    def end_card_management(self):
        if DEBUG:
            print("Cards management done")

        if self.round == NUMBER_OF_ROUNDS - 1:
            self.status = Tournament.Status.FINAL
        else:
            self.status = Tournament.Status.ROUND

        for player in self.players:
            player.shuffle_deck()

    def prepare_round(self):
        if self.status == Tournament.Status.ROUND:
            self.round += 1
            self.duels = []

            for duel_id in [i for i in range((self.number_of_players + 1) // 2)]:
                players = TournamentPlan.get_players(self.round, duel_id)
                duel = Duel(players[0], players[1])
                self.duels.append(duel)
                duel.choose_starting_player()

                if DEBUG:
                    print(f"\nRound {self.round + 1}, duel {players[0]} VS {players[1]} started.")

    def get_round_winners(self):
        if self.check_all_duels_ended():
            for duel in self.duels:
                winner = duel.winner
                winner.trophies.append(self.game_trophies.draw(self.round))
                self.winners[self.round].append(winner)

            if DEBUG:
                print(f"\nRound {self.round + 1} ended.")

            self.status = Tournament.Status.DECK

    def play_final(self) -> Player:
        if self.status == Tournament.Status.FINAL:
            finalists = self.get_finalists()

            for player in finalists:
                player.reset_deck()

            duel = Duel(finalists[0], finalists[1])
            self.duels = [duel]

            if DEBUG:
                print("Final started")

            duel.play()
            self.winner = duel.winner

            if DEBUG:
                print(self.winner, " won the tournament!")

    def play(self) -> Player:
        self.prepare()

        while self.status != Tournament.Status.FINAL and not self.is_ended():
            # self.play_round()

            self.manage_cards()

        self.play_final()
        self.ended.set()


class TournamentPlan:
    CARDS_TO_DRAW = {
        0: {Level.A: 2},
        1: {Level.A: 2},
        2: {Level.A: 2, Level.B: 1},
        3: {Level.A: 2, Level.B: 2},
        4: {Level.B: 2},
        5: {Level.B: 2, Level.C: 1},
        6: {Level.C: 2},
    }

    plans: dict[Player, Self] = {}

    def __init__(self, duel_ids: list[int]):
        self.duel_ids = duel_ids.copy()

    @classmethod
    def get_players(cls, round: int, duel_id: int) -> list[Player]:
        players: list[Player] = []
        for player in cls.plans:
            if cls.plans[player].duel_ids[round] == duel_id:
                players.append(player)

        return players

    @classmethod
    def generate(cls, number_of_players: int, players: list[Player]):
        plans: list[Self] = []

        plans.append(TournamentPlan([0, 0, 0, 0, 0, 0, 0]))

        if 1 <= number_of_players <= 2:
            plans.append(TournamentPlan([0, 0, 0, 0, 0, 0, 0]))

        elif 3 <= number_of_players <= 4:
            plans.append(TournamentPlan([1, 0, 1, 1, 0, 1, 1]))
            plans.append(TournamentPlan([1, 1, 0, 1, 1, 0, 1]))
            plans.append(TournamentPlan([0, 1, 1, 0, 1, 1, 0]))

        elif 5 <= number_of_players <= 6:
            plans.append(TournamentPlan([0, 2, 2, 1, 0, 1, 1]))
            plans.append(TournamentPlan([1, 0, 1, 1, 1, 2, 2]))
            plans.append(TournamentPlan([1, 1, 2, 2, 1, 1, 0]))
            plans.append(TournamentPlan([2, 2, 0, 2, 2, 0, 2]))
            plans.append(TournamentPlan([2, 1, 1, 0, 2, 2, 1]))

        elif 7 <= number_of_players <= 8:
            plans.append(TournamentPlan([3, 3, 0, 1, 1, 2, 2]))
            plans.append(TournamentPlan([1, 3, 3, 0, 3, 3, 3]))
            plans.append(TournamentPlan([1, 1, 2, 2, 1, 1, 0]))
            plans.append(TournamentPlan([2, 1, 1, 1, 0, 3, 1]))
            plans.append(TournamentPlan([2, 2, 2, 3, 3, 0, 2]))
            plans.append(TournamentPlan([0, 2, 1, 2, 2, 2, 3]))
            plans.append(TournamentPlan([3, 0, 3, 3, 2, 1, 1]))

        else:
            return ValueError

        # Random plan assignment
        for player in players:
            plan = random.choice(plans)
            cls.plans[player] = plan
            plans.remove(plan)

        return cls.plans

    @classmethod
    def get_available_draws(cls, round: int):
        available_draws: dict[Level, int] = {}

        possible_tray_levels = list(TournamentPlan.CARDS_TO_DRAW[round].keys())
        for tray_level in possible_tray_levels:
            available_draws[tray_level] = TournamentPlan.CARDS_TO_DRAW[round][tray_level]

        return available_draws
