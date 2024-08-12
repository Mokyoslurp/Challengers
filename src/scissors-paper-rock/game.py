class Moves:
    SCISSORS = "Scissors"
    PAPER = "Paper"
    ROCK = "Rock"

    # Utility constant to compute the winner
    _CYCLE = {(SCISSORS, 0), (ROCK, 1), (PAPER, 2)}

    def win(move1: str, move2: str):
        """Tells the winner of a Scissors Paper Rock game

        :param move1: p1 move ("Rock", "Scissors" or "Paper")
        :param move2: p2 move ("Rock", "Scissors" or "Paper")
        :return: 0 if p1 is the winner, 1 if p2 is the winner, -1 if their is
            a tie
        """
        if move1 == move2:
            return -1
        else:
            win = (Moves._CYCLE[move1] - Moves._CYCLE[move2]) % 2
            if Moves._CYCLE[move1] > Moves._CYCLE[move2]:
                return abs(win - 1)
            else:
                return win


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
        if player_id == 1:
            self.player1_played = True
        else:
            self.player2_played = True

    def connected(self):
        return self.ready

    def both_played(self):
        return self.player1_played and self.player2_played

    def winner(self):
        if self.both_played():
            # Get the first letter of the word instead of the whole
            player1_move = self.get_player_move(0)
            player2_move = self.get_player_move(1)

            winner = Moves.win(player1_move, player2_move)

            if winner == -1:
                self.ties += 1
            else:
                self.wins[winner] += 1

            return winner

    def reset_moves(self):
        self.player1_played = False
        self.player2_played = False
        self.moves = [None, None]
