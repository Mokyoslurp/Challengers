import random
import asyncio

from .player import Player

from .data import DEBUG


BENCH_SIZE = 6


class Duel:
    """
    Duel between two players
    """

    def __init__(self):
        self.flag_owner: Player = None
        self.attacking_player: Player = None
        self.player_1: Player = None
        self.player_2: Player = None

    def assign_players(self, player_1: Player, player_2: Player):
        """
        Adds the players to the competing players in the duel

        :param player_1: player 1
        :param player_2: player 2
        """
        self.player_1 = player_1
        self.player_2 = player_2

    def set_starting_player(self):
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

    async def play(self) -> Player:
        """
        Plays duel

        :return: the player that won the battle
        """
        self.set_starting_player()

        # Play initial card
        played_card = await self.flag_owner.let_play()
        if DEBUG:
            print(self.flag_owner.name + ", Defending: " + str(played_card))

        # Rest of the match
        while (
            len(self.attacking_player.deck) > 0
            and len(self.player_1.bench) < 6
            and len(self.player_2.bench) < 6
        ):
            while (
                len(self.attacking_player.deck) > 0
                and self.attacking_player.get_power() < self.flag_owner.get_power()
            ):
                played_card = await self.attacking_player.let_play()
                if DEBUG:
                    print(self.attacking_player.name + ": " + str(played_card))

            if self.attacking_player.get_power() >= self.flag_owner.get_power():
                await asyncio.sleep(1)
                # Switch attack and defense roles
                self.switch_flag_owner()

        if DEBUG:
            print(self.flag_owner.name + " won!")

        return self.flag_owner
