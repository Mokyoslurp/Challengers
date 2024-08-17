from pathlib import Path


from game import Player, Tournament, Trophy


GAME_DATA_PATH = Path(__file__).parent / "game" / "data"
CARD_DATA_FILE = "cards.json"

CARD_DATA_FILE_PATH = GAME_DATA_PATH / CARD_DATA_FILE

# Key is the round, and the list following is all the possible fans for a trophy of this round.
TROPHIES: dict[int, list[int]] = {
    0: [2, 2, 2, 3],
    1: [2, 2, 3, 3],
    2: [3, 3, 4, 4],
    3: [4, 5, 6, 6],
    4: [6, 6, 6, 7],
    5: [7, 7, 7, 8],
    6: [9, 9, 10, 10],
}

PLAYERS = [
    Player(1, "P1"),
    Player(2, "P2"),
    Player(3, "P3"),
    Player(4, "P4"),
    Player(5, "P5"),
    Player(6, "P6"),
    Player(7, "P7"),
    Player(8, "P8"),
]


def load_trophies(tournament: Tournament):
    for round in TROPHIES:
        for park in range(len(tournament.parks)):
            Trophy.create(round, TROPHIES[round][park])

    Trophy.shuffle_trophies()


if __name__ == "__main__":
    tournament = Tournament(8)

    tournament.load_game_cards(CARD_DATA_FILE_PATH)

    load_trophies(tournament)

    for player in PLAYERS:
        tournament.set_new_player(player)

    winner = tournament.play()

    tournament.print_scores()
