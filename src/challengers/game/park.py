import random

from .player import Player

from .data import DEBUG


BENCH_SIZE = 6


class Park:
    """
    Park object in which two players will battle
    """

    def __init__(self, id: int):
        """
        :param id: unique id of the park
        """
        self.id = id

        self.flag_owner: Player = None
        self.player_1: Player = None
        self.player_2: Player = None

        self.battle_finished: bool = False

    def assign_players(self, player_1: Player, player_2: Player):
        """
        Adds the players to the competing players in the park

        :param player_1: player 1
        :param player_2: player 2
        """
        self.player_1 = player_1
        self.player_2 = player_2

    def play_game(self) -> Player:
        """
        Plays a round in the park

        :return: the player that won the battle
        """
        attacking_player: Player = None

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

        attacking_player = self.player_1 if self.flag_owner == self.player_2 else self.player_2

        played_card = self.flag_owner.play()
        if DEBUG:
            print(self.flag_owner.name + ", Defending: " + str(played_card))

        while (
            len(attacking_player.deck) > 0
            and len(self.player_1.bench) < 6
            and len(self.player_2.bench) < 6
        ):
            while (
                len(attacking_player.deck) > 0
                and attacking_player.get_power() < self.flag_owner.get_power()
            ):
                if attacking_player.is_robot:
                    played_card = attacking_player.play()
                    if DEBUG:
                        print(attacking_player.name + ": " + str(played_card))

            if attacking_player.get_power() >= self.flag_owner.get_power():
                # Switch attack and defense roles
                self.flag_owner, attacking_player = attacking_player, self.flag_owner

                self.flag_owner.set_defense()
                attacking_player.bench_cards()

        if DEBUG:
            print(self.flag_owner.name + " won!")

        return self.flag_owner
