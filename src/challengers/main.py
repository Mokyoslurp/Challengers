from pathlib import Path


from challengers.game import Tournament
from challengers.server import Server


GAME_DATA_PATH = Path(__file__).parent / "game" / "data"
CARD_DATA_FILE = "cards.json"
TROPHY_DATA_FILE = "trophies.json"

CARD_DATA_FILE_PATH = GAME_DATA_PATH / CARD_DATA_FILE
TROPHY_DATA_FILE_PATH = GAME_DATA_PATH / TROPHY_DATA_FILE


if __name__ == "__main__":
    server = Server(Tournament(8))

    server.tournament.load_game_cards(CARD_DATA_FILE_PATH)
    server.tournament.load_game_trophies(TROPHY_DATA_FILE_PATH)

    server.run()
    # winner = tournament.play()

    # tournament.print_scores()
