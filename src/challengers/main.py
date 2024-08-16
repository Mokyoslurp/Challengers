from pathlib import Path


from challengers.game import (
    Level,
    Player,
    Tournament,
    Trophy,
    CardSerializer,
)


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
    CardSerializer.load_cards_from_file(CARD_DATA_FILE_PATH)

    tournament = Tournament(8)

    load_trophies(tournament)

    for player in PLAYERS:
        tournament.set_new_player(player)

    tournament.initialize_trays()

    for player in tournament.players:
        for _ in range(6):
            player.draw_card(tournament.trays[Level.A])
            player.shuffle_deck()

    winner = tournament.play()

    tournament.print_scores()
