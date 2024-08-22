from pathlib import Path

from challengers.game import (
    TrophySerializer,
    TrophyDict,
    Trophy,
)

JSON_TROPHY_FILE_NAME = "trophies.json"
JSON_TROPHY_FILE_PATH = Path(__file__).parent.parent / "game" / "data" / JSON_TROPHY_FILE_NAME


def _generate_trophies_to_dump():
    # Key is the round, and the list following is all the possible fans for a trophy of this round.
    trophies_dict: dict[int, list[int]] = {
        0: [2, 2, 2, 3],
        1: [2, 2, 3, 3],
        2: [3, 3, 4, 4],
        3: [5, 5, 6, 6],
        4: [6, 6, 6, 7],
        5: [7, 7, 7, 8],
        6: [9, 9, 10, 10],
    }

    trophies = {
        round: [Trophy(round, fans) for fans in trophies_dict[round]] for round in trophies_dict
    }

    return trophies


def _print_trophy_file(file_path):
    trophies: TrophyDict = TrophySerializer.load_trophies_from_file(file_path)
    for round in trophies:
        print(trophies[round])


if __name__ == "__main__":
    trophies = _generate_trophies_to_dump()

    TrophySerializer.dump_trophies_into_file(trophies, JSON_TROPHY_FILE_PATH)

    _print_trophy_file(JSON_TROPHY_FILE_PATH)
