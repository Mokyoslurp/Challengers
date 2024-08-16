from pathlib import Path

from ..game import (
    Card,
    Level,
    Set,
    CardSerializer,
)

JSON_CARD_FILE_NAME = "cards.json"
JSON_CARD_FILE_PATH = Path(__file__).parent / "game" / JSON_CARD_FILE_NAME


def generate_cards_to_dump():
    cards = [
        Card(1, "Test1", Set.CITY, Level.A, power=3, amount=4),
        Card(2, "Test2", Set.HAUNTED_HOUSE, Level.A, power=5, amount=4),
        Card(3, "Test3", Set.OUTER_SPACE, Level.A, power=4, amount=3),
        Card(4, "Test4", Set.SHIPWRECK, Level.A, power=1, amount=5),
        Card(5, "Test5", Set.CASTLE, Level.A, power=2, amount=2),
        Card(6, "Test6", Set.FILM_STUDIO, Level.A, power=2, amount=3),
        Card(7, "Test7", Set.FUNFAIR, Level.A, power=3, amount=3),
        Card(8, "Test8", Set.SHIPWRECK, Level.A, power=4, amount=4),
        Card(9, "Test8", Set.CITY, Level.A, power=4, amount=2),
        Card(10, "Test8", Set.CASTLE, Level.A, power=2, amount=7),
        Card(11, "Test8", Set.OUTER_SPACE, Level.A, power=2, amount=3),
        Card(12, "Test8", Set.OUTER_SPACE, Level.A, power=3, amount=2),
        Card(13, "Test8", Set.FILM_STUDIO, Level.A, power=5, amount=3),
        Card(14, "Test8", Set.FUNFAIR, Level.A, power=6, amount=3),
    ]
    return cards


if __name__ == "__main__":
    cards = generate_cards_to_dump()

    CardSerializer.dump_cards_into_file(cards, JSON_CARD_FILE_PATH)
