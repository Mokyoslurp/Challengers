from pathlib import Path

import asyncio

from challengers.game import Tournament, Player
from challengers.server import Server


GAME_DATA_PATH = Path(__file__).parent / "game" / "data"
CARD_DATA_FILE = "cards.json"
TROPHY_DATA_FILE = "trophies.json"

CARD_DATA_FILE_PATH = GAME_DATA_PATH / CARD_DATA_FILE
TROPHY_DATA_FILE_PATH = GAME_DATA_PATH / TROPHY_DATA_FILE


async def main():
    tournament = Tournament(1)
    tournament.load_game_cards(CARD_DATA_FILE_PATH)
    tournament.load_game_trophies(TROPHY_DATA_FILE_PATH)

    player = Player(0, "TestP")
    tournament.set_new_player(player)

    winner = await tournament.play()

    if winner:
        print("Winner is " + winner)

        tournament.print_scores()


def server_main(self):
    server = Server(Tournament(1))

    server.tournament.load_game_cards(CARD_DATA_FILE_PATH)
    server.tournament.load_game_trophies(TROPHY_DATA_FILE_PATH)

    server.run()


if __name__ == "__main__":
    asyncio.run(main())
