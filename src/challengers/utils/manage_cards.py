from pathlib import Path

from challengers.game import (
    Card,
    Level,
    Set,
    CardSerializer,
)

JSON_CARD_FILE_NAME = "cards.json"
JSON_CARD_FILE_PATH = Path(__file__).parent.parent / "game" / "data" / JSON_CARD_FILE_NAME


def generate_cards_to_dump():
    cards = [
        Card(1, "Test1", Set.CITY, Level.A, power=3),
        Card(2, "Test2", Set.HAUNTED_HOUSE, Level.A, power=5),
        Card(3, "Test3", Set.OUTER_SPACE, Level.A, power=4),
        Card(4, "Test4", Set.SHIPWRECK, Level.A, power=1),
        Card(5, "Test5", Set.CASTLE, Level.A, power=2),
        Card(6, "Test6", Set.FILM_STUDIO, Level.A, power=2),
        Card(7, "Test7", Set.FUNFAIR, Level.A, power=3),
        Card(8, "Test8", Set.SHIPWRECK, Level.A, power=4),
        Card(9, "Test8", Set.CITY, Level.A, power=4),
        Card(10, "Test8", Set.CASTLE, Level.A, power=2),
        Card(11, "Test8", Set.OUTER_SPACE, Level.A, power=2),
        Card(12, "Test8", Set.OUTER_SPACE, Level.A, power=3),
        Card(13, "Test8", Set.FILM_STUDIO, Level.A, power=5),
        Card(14, "Test8", Set.FUNFAIR, Level.A, power=6),
    ]
    return cards


def print_cards_file(file_path):
    cards: list[Card] = CardSerializer.load_cards_from_file(file_path)
    for card in cards:
        print(card)


if __name__ == "__main__":
    cards = generate_cards_to_dump()

    CardSerializer.dump_cards_into_file(cards, JSON_CARD_FILE_PATH)

    print_cards_file(JSON_CARD_FILE_PATH)
