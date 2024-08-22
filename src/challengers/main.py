from pathlib import Path


from challengers.game import Player, Tournament


GAME_DATA_PATH = Path(__file__).parent / "game" / "data"
CARD_DATA_FILE = "cards.json"
TROPHY_DATA_FILE = "trophies.json"

CARD_DATA_FILE_PATH = GAME_DATA_PATH / CARD_DATA_FILE
TROPHY_DATA_FILE_PATH = GAME_DATA_PATH / TROPHY_DATA_FILE

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

if __name__ == "__main__":
    tournament = Tournament(8)

    tournament.load_game_cards(CARD_DATA_FILE_PATH)
    tournament.load_game_trophies(TROPHY_DATA_FILE_PATH)

    for player in PLAYERS:
        tournament.set_new_player(player)

    winner = tournament.play()

    tournament.print_scores()
