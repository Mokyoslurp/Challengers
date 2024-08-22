from pathlib import Path

from challengers.game import (
    Card,
    Level,
    Set,
    CardSerializer,
)

JSON_CARD_FILE_NAME = "cards.json"
JSON_CARD_FILE_PATH = Path(__file__).parent.parent / "game" / "data" / JSON_CARD_FILE_NAME


def _generate_cards_to_dump():
    cards_A = [
        Card(1, "Test1", Set.CITY, Level.A, power=3),
        Card(2, "Test2", Set.HAUNTED_HOUSE, Level.A, power=5),
        Card(3, "Test3", Set.OUTER_SPACE, Level.A, power=4),
        Card(4, "Test4", Set.SHIPWRECK, Level.A, power=1),
        Card(5, "Test5", Set.CASTLE, Level.A, power=2),
        Card(6, "Test6", Set.FILM_STUDIO, Level.A, power=2),
        Card(7, "Test7", Set.FUNFAIR, Level.A, power=3),
        Card(8, "Test8", Set.SHIPWRECK, Level.A, power=4),
        Card(9, "Test9", Set.CITY, Level.A, power=4),
        Card(10, "Test10", Set.CASTLE, Level.A, power=2),
        Card(11, "Test11", Set.OUTER_SPACE, Level.A, power=2),
        Card(12, "Test12", Set.OUTER_SPACE, Level.A, power=3),
        Card(13, "Test13", Set.FILM_STUDIO, Level.A, power=5),
        Card(14, "Test14", Set.FUNFAIR, Level.A, power=6),
    ]

    cards_B = [
        Card(1, "Test15", Set.CITY, Level.B, power=3),
        Card(16, "Test16", Set.HAUNTED_HOUSE, Level.B, power=5),
        Card(17, "Test17", Set.OUTER_SPACE, Level.B, power=4),
        Card(18, "Test18", Set.SHIPWRECK, Level.B, power=1),
        Card(19, "Test19", Set.CASTLE, Level.B, power=2),
        Card(20, "Test20", Set.FILM_STUDIO, Level.B, power=2),
        Card(21, "Test21", Set.FUNFAIR, Level.B, power=3),
        Card(22, "Test22", Set.SHIPWRECK, Level.B, power=4),
        Card(23, "Test23", Set.CITY, Level.B, power=4),
        Card(24, "Test24", Set.CASTLE, Level.B, power=2),
        Card(25, "Test25", Set.OUTER_SPACE, Level.B, power=2),
        Card(26, "Test26", Set.OUTER_SPACE, Level.B, power=3),
        Card(27, "Test27", Set.FILM_STUDIO, Level.B, power=5),
        Card(28, "Test28", Set.FUNFAIR, Level.B, power=6),
        Card(15, "Test15", Set.CITY, Level.B, power=3),
        Card(16, "Test16", Set.HAUNTED_HOUSE, Level.B, power=5),
        Card(17, "Test17", Set.OUTER_SPACE, Level.B, power=4),
        Card(18, "Test18", Set.SHIPWRECK, Level.B, power=1),
        Card(19, "Test19", Set.CASTLE, Level.B, power=2),
        Card(20, "Test20", Set.FILM_STUDIO, Level.B, power=2),
        Card(21, "Test21", Set.FUNFAIR, Level.B, power=3),
        Card(22, "Test22", Set.SHIPWRECK, Level.B, power=4),
        Card(23, "Test23", Set.CITY, Level.B, power=4),
        Card(24, "Test24", Set.CASTLE, Level.B, power=2),
        Card(25, "Test25", Set.OUTER_SPACE, Level.B, power=2),
        Card(26, "Test26", Set.OUTER_SPACE, Level.B, power=3),
        Card(27, "Test27", Set.FILM_STUDIO, Level.B, power=5),
        Card(28, "Test28", Set.FUNFAIR, Level.B, power=6),
    ]

    cards_C = [
        Card(29, "Test29", Set.CITY, Level.C, power=3),
        Card(30, "Test30", Set.HAUNTED_HOUSE, Level.C, power=5),
        Card(31, "Test31", Set.OUTER_SPACE, Level.C, power=4),
        Card(32, "Test32", Set.SHIPWRECK, Level.C, power=1),
        Card(33, "Test33", Set.CASTLE, Level.C, power=2),
        Card(34, "Test34", Set.FILM_STUDIO, Level.C, power=2),
        Card(35, "Test35", Set.FUNFAIR, Level.C, power=3),
        Card(36, "Test36", Set.SHIPWRECK, Level.C, power=4),
        Card(37, "Test37", Set.CITY, Level.C, power=4),
        Card(38, "Test38", Set.CASTLE, Level.C, power=2),
        Card(39, "Test39", Set.OUTER_SPACE, Level.C, power=2),
        Card(40, "Test40", Set.OUTER_SPACE, Level.C, power=3),
        Card(41, "Test41", Set.FILM_STUDIO, Level.C, power=5),
        Card(42, "Test42", Set.FUNFAIR, Level.C, power=6),
    ]

    cards_S = [
        Card(43, "Start1", Set.CITY, Level.S, power=3),
        Card(44, "Start2", Set.CITY, Level.S, power=3),
        Card(45, "Start3", Set.CITY, Level.S, power=3),
        Card(46, "Start4", Set.CITY, Level.S, power=3),
        Card(47, "Start5", Set.CITY, Level.S, power=3),
        Card(48, "Start6", Set.CITY, Level.S, power=3),
    ]

    cards = cards_A + cards_B + cards_C + cards_S
    return cards


def _print_cards_file(file_path):
    cards: list[Card] = CardSerializer.load_cards_from_file(file_path)
    for card in cards:
        print(card)


def manage_cards():
    cards = _generate_cards_to_dump()

    CardSerializer.dump_cards_into_file(cards, JSON_CARD_FILE_PATH)

    _print_cards_file(JSON_CARD_FILE_PATH)
