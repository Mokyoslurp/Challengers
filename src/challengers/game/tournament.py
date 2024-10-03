import random
from typing import Self
from enum import Enum

import asyncio

from .player import Player
from .park import Park
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
        MATCH = 1
        DECK = 2
        FINAL = 3

    def __init__(self, number_of_players: int):
        if 0 < number_of_players <= MAX_NUMBER_OF_PLAYERS:
            self.number_of_players = number_of_players

            self.players: list[Player] = []
            self.parks: list[Park] = [Park(i) for i in range((self.number_of_players + 1) // 2)]
            # winners by parks and by rounds
            self.winners: list[list[Player]] = [[]] * NUMBER_OF_ROUNDS
            self.winner: Player

            self.status = Tournament.Status.NONE
            self.round: int = 0

            self.trays: dict[Level, Tray] = {}

            self.scores: dict[Player, int] = {}

            self.game_cards: CardList
            self.game_trophies = TrophyDict()

        else:
            raise ValueError

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
            # This will avoid the case of 3 or more players with the same score. If the list of
            # possible finalists contain more than 3, only 2 will eventually be chosen, if there
            # is less the code will have the same behavior
            possible_finalists = [player for player in self.players if scores[player] == max_score]
            finalists.append(random.choice(possible_finalists))

            # Avoid having the first finalist counted to be also the second finalist
            scores[finalists[-1]] = -1

        return finalists

    async def prepare(self):
        if self.status == Tournament.Status.NONE:
            if len(self.players) == self.number_of_players:
                # Set a robot player if there is an odd number of players
                if len(self.players) % 2 == 1:
                    self.players.append(Player(len(self.players), ROBOT_PLAYER_NAME, is_robot=True))

                if DEBUG:
                    for player in self.players:
                        print(player)

            TournamentPlan.generate_plans(self.number_of_players, self.players)

            self.initialize_trays()
            for player in self.players:
                player.get_starter_cards(self.trays[Level.S])

            await asyncio.gather(*(player.let_get_ready() for player in self.players))

            self.status = Tournament.Status.MATCH

            if DEBUG:
                print("Tournament started")

    async def play_round(self, park: Park):
        park_players = TournamentPlan.get_players(self.round, park.id)
        park.assign_players(park_players[0], park_players[1])

        if DEBUG:
            print("\nRound ", self.round + 1, ", park ", park.id, " started.")

        return await park.play_game()

    def manage_robot_players_cards(self, player: Player):
        if player.is_robot:
            possible_tray_levels = list(TournamentPlan.CARDS_TO_DRAW[self.round].keys())
            chosen_tray_level = random.choice(possible_tray_levels)

            for _ in range(TournamentPlan.CARDS_TO_DRAW[self.round][chosen_tray_level]):
                player.draw(self.trays[chosen_tray_level])
            player.shuffle_deck()

            for card in player.deck[:]:
                if random.uniform(0, 1) <= 1 / (40 - len(player.deck)):
                    player.discard(card, self.trays[chosen_tray_level])

    async def manage_cards(self):
        if self.status == Tournament.Status.DECK:
            human_players: list[Player] = []
            for player in self.players:
                player.reset_deck()
                if player.is_robot:
                    self.manage_robot_players_cards(player)
                else:
                    human_players.append(player)

            await asyncio.gather(*(player.let_manage_cards() for player in human_players))

            self.status = Tournament.Status.MATCH

    async def play_matches(self):
        if self.status == Tournament.Status.MATCH:
            self.round += 1

            winners = await asyncio.gather(*(self.play_round(park) for park in self.parks))

            for winner in winners:
                winner.trophies.append(self.game_trophies.draw(self.round - 1))
            self.winners[self.round - 1] = winners

            if self.round == NUMBER_OF_ROUNDS:
                self.status = Tournament.Status.FINAL
            else:
                self.status = Tournament.Status.DECK

    async def play_final(self) -> Player:
        if self.status == Tournament.Status.FINAL:
            finalists = self.get_finalists()

            park = self.parks[0]
            park.assign_players(finalists[0], finalists[1])

            if DEBUG:
                print("Final started")

            self.winner = await park.play_game()

            if DEBUG:
                print(self.winner, " won the tournament!")

            for player in finalists:
                player.reset_deck()

    async def play(self) -> Player:
        await self.prepare()

        while self.status != Tournament.Status.FINAL:
            await self.play_matches()

            await self.manage_cards()

        await self.play_final()

        return self.winner


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

    def __init__(self, park_ids: list[int]):
        if len(park_ids) == NUMBER_OF_ROUNDS:
            self.park_ids = park_ids.copy()

    @classmethod
    def get_players(cls, round: int, park_id: int) -> list[Player]:
        players: list[Player] = []
        for player in cls.plans:
            if cls.plans[player].park_ids[round] == park_id:
                players.append(player)

        return players

    @classmethod
    def generate_plans(cls, number_of_players: int, players: list[Player]):
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
