class Moves:
    SCISSORS = "Scissors"
    PAPER = "Paper"
    ROCK = "Rock"


class Game:
    def __init__(self, id):
        self.player1_played = False
        self.player2_played = False
        self.ready = False
        self.id = id
        self.moves = [None, None]
        self.wins = [0, 0]
        self.ties = 0

    def get_player_move(self, player_id):
        """
        :param player_id: 0 for player 1, 1 for player 2
        :return: Scissors, Paper or Rock (string)
        """
        return self.moves[player_id]

    def play(self, player_id, move):
        self.moves[player_id] = move
        if player_id == 0:
            self.player1_played = True
        else:
            self.player2_played = True

    def connected(self):
        return self.ready

    def both_played(self):
        return self.player1_played and self.player2_played

    def winner(self):
        # Get the first letter of the word instead of the whole
        player1_move = self.get_player_move(0)
        player2_move = self.get_player_move(1)

        winner = -1
        if player2_move == player1_move:
            winner = -1
        elif (
            (player1_move == Moves.ROCK and player2_move == Moves.SCISSORS)
            or (player1_move == Moves.PAPER and player2_move == Moves.ROCK)
            or (player1_move == Moves.SCISSORS and player2_move == Moves.PAPER)
        ):
            winner = 0
        else:
            winner = 1

        if winner == -1:
            self.ties += 1
        else:
            self.wins[winner] += 1

        return winner

    def reset_moves(self):
        self.player1_played = False
        self.player2_played = False
