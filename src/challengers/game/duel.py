import random
import threading
from time import sleep

from .player import Player

from .data import DEBUG


BENCH_SIZE = 6


class Duel:
    """
    Duel between two players
    """

    def __init__(self, player_1: Player, player_2: Player):
        """
        :param player_1:
        :param player_2:
        """
        self.player_1: Player = player_1
        self.player_2: Player = player_2

        self.flag_owner: Player = None
        self.attacking_player: Player = None

        self.winner: Player = None

        # To trigger when duel is ended
        self.ended = threading.Event()

    def is_ended(self):
        return self.ended.is_set()

    def choose_starting_player(self):
        """
        Sets both the first player who owns the flag, and the player who will attack first.
        """
        player_1_higher_round_win = self.player_1.get_higher_round_win()
        player_2_higher_round_win = self.player_2.get_higher_round_win()

        if player_1_higher_round_win == player_2_higher_round_win:
            self.flag_owner = random.choice([self.player_1, self.player_2])
        else:
            self.flag_owner = (
                self.player_1
                if player_1_higher_round_win > player_2_higher_round_win
                else self.player_2
            )
        self.attacking_player = self.player_1 if self.flag_owner == self.player_2 else self.player_2

    def switch_flag_owner(self):
        self.flag_owner, self.attacking_player = self.attacking_player, self.flag_owner

        self.flag_owner.set_defense()
        self.attacking_player.bench_cards()

    def play(self) -> Player:
        """
        Plays duel

        :return: the player that won the battle
        """
        self.choose_starting_player()

        # Play initial card
        self.flag_owner.has_played = False
        self.flag_owner.play()

        if DEBUG:
            print(f"First card by {self.flag_owner}\n {self.flag_owner.played_cards[-1]}")

        # Rest of the match
        while (
            len(self.attacking_player.deck) > 0
            and len(self.player_1.bench) < BENCH_SIZE
            and len(self.player_2.bench) < BENCH_SIZE
            and not self.is_ended()
        ):
            while (
                len(self.attacking_player.deck) > 0
                and self.attacking_player.get_power() < self.flag_owner.get_power()
                and not self.is_ended()
            ):
                if DEBUG:
                    print(f"\nWaiting for {self.attacking_player} to play\n")

                self.attacking_player.has_played = False
                if self.attacking_player.is_robot:
                    sleep(1.5)
                    self.attacking_player.play()
                while not self.attacking_player.has_played and not self.is_ended():
                    pass

                if DEBUG:
                    print(
                        f"Player {self.attacking_player.name} played\n{self.attacking_player.played_cards[-1]}"
                    )

            if self.attacking_player.get_power() >= self.flag_owner.get_power():
                # Switch attack and defense roles
                self.switch_flag_owner()

        self.winner = self.flag_owner
        self.ended.set()

        if DEBUG:
            print(f"Player {self.winner.name} won duel {self.player_1} VS {self.player_2}")
