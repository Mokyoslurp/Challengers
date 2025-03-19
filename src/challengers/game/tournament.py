import random
from typing import Self
from enum import Enum
import threading

from .player import Player
from .duel import Duel
from .tray import Tray
from .card import Level
from .trophy import TrophyDict, TrophySerializer
from .card import CardList, CardSerializer

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

            self.game_cards: CardList
            self.game_trophies = TrophyDict()

            self.ended = threading.Event()

        else:
            raise ValueError

    def is_ended(self):
        return self.ended.is_set()

    def reset(self):
        self.players = []
        self.winners = [[]]
        self.winner = None
        self.round = -1
        self.trays = {}
        self.scores = {}
        self.game_cards = CardList()
        self.game_trophies = TrophyDict()

    def load_game_cards(self, game_cards_file_path: str):
        self.game_cards = CardSerializer.load_cards_from_file(game_cards_file_path)

    def load_game_trophies(self, game_trophies_file_path: str):
        self.game_trophies = TrophySerializer.load_trophies_from_file(game_trophies_file_path)

    def initialize_trays(self) -> list[Tray]:
        for level in [Level.A, Level.B, Level.C, Level.S]:
            tray = Tray(level)
            tray.prepare(self.game_cards)
            self.trays[level] = tray

        return self.trays

    def add_player(self, player: Player) -> list[Player]:
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
            if len(self.players) == self.number_of_players:
                # Set a robot player if there is an odd number of players
                if len(self.players) % 2 == 1:
                    self.players.append(Player(len(self.players), ROBOT_PLAYER_NAME, is_robot=True))

            TournamentPlan.generate(self.number_of_players, self.players)

            self.initialize_trays()
            for player in self.players:
                player.get_starter_cards(self.trays[Level.S])
                if not player.is_robot:
                    player.is_ready = False
                else:
                    player.is_ready = True

            self.status = Tournament.Status.PREPARE

            if DEBUG:
                print("All players have to be ready\n")

            # Wait for all players to be ready
            while not all([player.is_ready for player in self.players]) and not self.is_ended():
                pass

            self.status = Tournament.Status.ROUND

            if DEBUG:
                print("Tournament started")

    def make_draw(self, player: Player, level: Level) -> CardList:
        return player.draw(self.trays[level], self.available_draws[level])

    def manage_robot_players_cards(self, player: Player):
        """Randomizes the card draw and discard for the bots

        :param player: The robot player
        """

        if player.is_robot:
            # random draw choice
            chosen_tray_level = random.choice(list(self.available_draws.keys()))

            self.make_draw(player, chosen_tray_level)

            player.shuffle_deck()

            # Random discard
            for card in player.deck[:]:
                if random.uniform(0, 1) <= 1 / (40 - len(player.deck)):
                    player.discard(card, self.trays[chosen_tray_level])

    def manage_cards(self):
        if self.status == Tournament.Status.DECK:
            for player in self.players:
                player.has_managed_cards = False
                player.has_drawn = False

            self.available_draws = TournamentPlan.get_available_draws(self.round)

            if DEBUG:
                print(f"Available draws : {self.available_draws}")

            human_players: list[Player] = []
            for player in self.players:
                player.reset_deck()
                if player.is_robot:
                    self.manage_robot_players_cards(player)
                    player.has_managed_cards = True
                else:
                    human_players.append(player)

            if DEBUG:
                print("Players have to manage cards !")

            while not self.is_ended() and not all(
                [player.has_managed_cards for player in human_players]
            ):
                pass

            for player in self.players:
                player.shuffle_deck()

            if DEBUG:
                print("Cards management done")

            if self.round == NUMBER_OF_ROUNDS - 1:
                self.status = Tournament.Status.FINAL
            else:
                self.status = Tournament.Status.ROUND

    def play_round(self):
        if self.status == Tournament.Status.ROUND:
            self.round += 1
            self.duels = []

            duel_threads: list[threading.Thread] = []

            for duel_id in [i for i in range((self.number_of_players + 1) // 2)]:
                players = TournamentPlan.get_players(self.round, duel_id)
                duel = Duel(players[0], players[1])
                self.duels.append(duel)

                duel_thread = threading.Thread(target=duel.play)
                duel_threads.append(duel_thread)
                duel_thread.start()

                if DEBUG:
                    print(f"\nRound {self.round + 1}, duel {players[0]} VS {players[1]} started.")

            for duel_thread in duel_threads:
                duel_thread.join()

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
            self.play_round()

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
