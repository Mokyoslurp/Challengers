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
    current_set = Set.CITY
    cards_S = (
        3 * [Card(1, "Recrue", current_set, Level.S, power=1)]
        + [Card(2, "Capitaine", current_set, Level.S, power=2)]
        + [Card(3, "Chien", current_set, Level.S, power=3)]
        + [Card(4, "Championne", current_set, Level.S, power=4)]
    )

    city_deck = (
        4 * [Card(11, "Journaliste", current_set, Level.A, power=2)]
        + 3 * [Card(12, "Capitaine", current_set, Level.A, power=2, text="Rare 3x")]
        + 4 * [Card(13, "Mascotte", current_set, Level.B, power=2)]
        + 3 * [Card(14, "Chien", current_set, Level.B, power=3, text="Rare 3x")]
        + 4 * [Card(15, "Autobus", current_set, Level.C, power=6)]
        + 2 * [Card(16, "Championne", current_set, Level.C, power=4, text="Rare 2x")]
    )

    current_set = Set.CASTLE
    castle_deck = (
        4 * [Card(20, "Bouffon", current_set, Level.A, power=1)]
        + 4 * [Card(21, "Hermite", current_set, Level.A, power=2)]
        + 4 * [Card(22, "Garçon d'écurie", current_set, Level.A, power=2)]
        + 3 * [Card(23, "Cochon", current_set, Level.A, power=3, text="Rare 3x")]
        + 4 * [Card(24, "Chevalier", current_set, Level.B, power=3)]
        + 4 * [Card(25, "Forgeronne", current_set, Level.B, power=3)]
        + 4 * [Card(26, "Sorcier", current_set, Level.B, power=4)]
        + 3 * [Card(27, "Cheval", current_set, Level.B, power=5, text="Rare 3x")]
        + 4 * [Card(28, "Barde", current_set, Level.C, power=4)]
        + 4 * [Card(29, "Prince", current_set, Level.C, power=5)]
        + 2 * [Card(30, "Dragon", current_set, Level.C, power=7, text="Rare 2x")]
    )

    current_set = Set.SHIPWRECK
    shipwreck_deck = (
        4 * [Card(40, "M.Sirène", current_set, Level.A, power=1)]
        + 4 * [Card(41, "Matelot", current_set, Level.A, power=2)]
        + 4 * [Card(42, "Trésor", current_set, Level.A, power=2)]
        + 3 * [Card(43, "Perroquet", current_set, Level.A, power=3, text="Rare 3x")]
        + 4 * [Card(44, "Cuistot", current_set, Level.B, power=2)]
        + 4 * [Card(45, "Navigateur", current_set, Level.B, power=4)]
        + 4 * [Card(46, "Sauveteuse", current_set, Level.B, power=4)]
        + 3 * [Card(47, "Requin", current_set, Level.B, power=5, text="Rare 3x")]
        + 4 * [Card(48, "Corne de brume", current_set, Level.C, power=6)]
        + 2 * [Card(49, "Kraken", current_set, Level.C, power=7, text="Rare 2x")]
        + 4 * [Card(50, "Sous-marin", current_set, Level.C, power=9)]
    )

    current_set = Set.FILM_STUDIO
    film_deck = (
        4 * [Card(60, "Maquilleur", current_set, Level.A, power=1)]
        + 4 * [Card(61, "Gangster", current_set, Level.A, power=2)]
        + 4 * [Card(62, "Star du cinéma", current_set, Level.A, power=2)]
        + 3 * [Card(63, "Chat", current_set, Level.A, power=3, text="Rare 3x")]
        + 4 * [Card(64, "Cowboy", current_set, Level.B, power=3)]
        + 4 * [Card(65, "Tic tac", current_set, Level.B, power=4)]
        + 4 * [Card(66, "Réalisatrice", current_set, Level.B, power=4)]
        + 3 * [Card(67, "Lion", current_set, Level.B, power=5, text="Rare 3x")]
        + 4 * [Card(68, "Héroïne", current_set, Level.C, power=5)]
        + 2 * [Card(69, "T-rex", current_set, Level.C, power=7, text="Rare 2x")]
        + 4 * [Card(70, "Super vilain", current_set, Level.C, power=10)]
    )

    current_set = Set.HAUNTED_HOUSE
    haunted_deck = (
        4 * [Card(80, "Majordome", current_set, Level.A, power=1)]
        + 8 * [Card(81, "Squelette", current_set, Level.A, power=2, text="Commune 8x")]
        + 3 * [Card(82, "Araignée", current_set, Level.A, power=3, text="Rare 3x")]
        + 4 * [Card(83, "Fantôme", current_set, Level.B, power=1)]
        + 4 * [Card(84, "Ado", current_set, Level.B, power=2)]
        + 4 * [Card(85, "Nécromancienne", current_set, Level.B, power=3)]
        + 3 * [Card(86, "Chauve-souris", current_set, Level.B, power=5, text="Rare 3x")]
        + 4 * [Card(87, "Vampire", current_set, Level.C, power=4)]
        + 4 * [Card(88, "Aspirateur", current_set, Level.C, power=5)]
        + 2 * [Card(89, "Loup-garou", current_set, Level.C, power=7, text="Rare 2x")]
    )

    current_set = Set.OUTER_SPACE
    space_deck = (
        4 * [Card(100, "Capsule", current_set, Level.A, power=1)]
        + 3 * [Card(101, "I.A.", current_set, Level.A, power=2, text="Rare 3x")]
        + 4 * [Card(102, "Métaforme", current_set, Level.A, power=2)]
        + 3 * [Card(103, "Vache", current_set, Level.A, power=3, text="Rare 3x")]
        + 4 * [Card(104, "Ovni", current_set, Level.B, power=3)]
        + 4 * [Card(105, "Fanfare", current_set, Level.B, power=3)]
        + 5 * [Card(106, "Clones", current_set, Level.B, power=4, text="Commune 5x")]
        + 3 * [Card(107, "E.T.", current_set, Level.B, power=5, text="Rare 3x")]
        + 4 * [Card(108, "Hologramme", current_set, Level.C, power=4)]
        + 4 * [Card(109, "Geek", current_set, Level.C, power=6)]
        + 2 * [Card(110, "Blob", current_set, Level.C, power=7, text="Rare 2x")]
    )

    current_set = Set.FUNFAIR
    funfair_deck = (
        4 * [Card(120, "Clown", current_set, Level.A, power=1)]
        + 4 * [Card(121, "Vendeuse", current_set, Level.A, power=2)]
        + 4 * [Card(122, "Jongleur", current_set, Level.A, power=2)]
        + 3 * [Card(123, "Poney", current_set, Level.A, power=3, text="Rare 3x")]
        + 4 * [Card(124, "Mime", current_set, Level.B, power=1)]
        + 4 * [Card(125, "Clairvoyante", current_set, Level.B, power=4)]
        + 4 * [Card(126, "Pyrotechnicienne", current_set, Level.B, power=4)]
        + 3 * [Card(127, "Canard géant", current_set, Level.B, power=5, text="Rare 3x")]
        + 4 * [Card(128, "Illusionniste", current_set, Level.C, power=5)]
        + 4 * [Card(129, "Auto tamponneuse", current_set, Level.C, power=6)]
        + 2 * [Card(130, "Peluche", current_set, Level.C, power=7, text="Rare 2x")]
    )

    cards = (
        cards_S * 8
        + city_deck
        + castle_deck
        + shipwreck_deck
        + film_deck
        + haunted_deck
        + space_deck
        + funfair_deck
    )
    return cards


def _print_cards_file(file_path):
    cards: list[Card] = CardSerializer.load_cards_from_file(file_path)
    for card in cards:
        print(card)


if __name__ == "__main__":
    cards = _generate_cards_to_dump()

    CardSerializer.dump_cards_into_file(cards, JSON_CARD_FILE_PATH)

    _print_cards_file(JSON_CARD_FILE_PATH)
