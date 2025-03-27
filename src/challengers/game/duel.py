import random
import threading

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

        self.flag_owner.has_played = False
        self.flag_owner.play()

        if DEBUG:
            print(f"First card by {self.flag_owner}\n {self.flag_owner.played_cards[-1]}")

        self.attacking_player.has_played = False

        # TODO: Put robot play at server level
        if self.attacking_player.is_robot:
            self.play_card(self.attacking_player)

    def switch_flag_owner(self):
        self.flag_owner, self.attacking_player = self.attacking_player, self.flag_owner

        self.flag_owner.set_defense()
        self.attacking_player.bench_cards()

        if (
            len(self.attacking_player.deck) > 0
            and len(self.player_1.bench) < BENCH_SIZE
            and len(self.player_2.bench) < BENCH_SIZE
        ):
            self.attacking_player.has_played = False

            if DEBUG:
                print(f"\nWaiting for {self.attacking_player} to play\n")

    def play_card(self, player: Player):
        played_card = None
        if player == self.attacking_player and not self.attacking_player.has_played:
            played_card = self.attacking_player.play()

            if DEBUG:
                print(
                    f"Player {self.attacking_player.name} played\n{self.attacking_player.played_cards[-1]}"
                )

            if self.attacking_player.get_power() >= self.flag_owner.get_power():
                # Switch attack and defense roles
                self.switch_flag_owner()
            else:
                player.has_played = False

            # TODO: Put robot play at server level
            if self.attacking_player.is_robot:
                self.play_card(self.attacking_player)

        if (
            len(self.attacking_player.deck) <= 0
            or len(self.player_1.bench) >= BENCH_SIZE
            or len(self.player_2.bench) >= BENCH_SIZE
        ):
            self.winner = self.flag_owner
            self.ended.set()

            if DEBUG:
                print(f"Player {self.winner.name} won duel {self.player_1} VS {self.player_2}")

        return played_card
