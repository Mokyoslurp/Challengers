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
        3 * [Card("Recrue", current_set, Level.S, power=1)]
        + [Card("Capitaine", current_set, Level.S, power=2)]
        + [Card("Chien", current_set, Level.S, power=3)]
        + [Card("Championne", current_set, Level.S, power=4)]
    )

    city_deck = (
        4 * [Card("Journaliste", current_set, Level.A, power=2)]
        + 3 * [Card("Capitaine", current_set, Level.A, power=2, text="Rare 3x")]
        + 4 * [Card("Mascotte", current_set, Level.B, power=2)]
        + 3 * [Card("Chien", current_set, Level.B, power=3, text="Rare 3x")]
        + 4 * [Card("Autobus", current_set, Level.C, power=6)]
        + 2 * [Card("Championne", current_set, Level.C, power=4, text="Rare 2x")]
    )

    current_set = Set.CASTLE
    castle_deck = (
        4 * [Card("Hermite", current_set, Level.A, power=2)]
        + 3 * [Card("Cochon", current_set, Level.A, power=3, text="Rare 3x")]
        + 4 * [Card("Bouffon", current_set, Level.A, power=1)]
        + 4 * [Card("Garçon d'écurie", current_set, Level.A, power=2)]
        + 4 * [Card("Chevalier", current_set, Level.B, power=3)]
        + 4 * [Card("Prince", current_set, Level.C, power=5)]
        + 4 * [Card("Forgeronne", current_set, Level.B, power=3)]
        + 4 * [Card("Sorcier", current_set, Level.B, power=4)]
        + 3 * [Card("Cheval", current_set, Level.B, power=5, text="Rare 3x")]
        + 2 * [Card("Dragon", current_set, Level.C, power=7, text="Rare 2x")]
        + 4 * [Card("Barde", current_set, Level.C, power=4)]
    )

    current_set = Set.SHIPWRECK
    shipwreck_deck = (
        4 * [Card("M.Sirène", current_set, Level.A, power=1)]
        + 3 * [Card("Requin", current_set, Level.B, power=5, text="Rare 3x")]
        + 4 * [Card("Matelot", current_set, Level.A, power=2)]
        + 4 * [Card("Navigateur", current_set, Level.B, power=4)]
        + 4 * [Card("Trésor", current_set, Level.A, power=2)]
        + 4 * [Card("Cuistot", current_set, Level.B, power=2)]
        + 4 * [Card("Corne de brume", current_set, Level.C, power=6)]
        + 3 * [Card("Perroquet", current_set, Level.A, power=3, text="Rare 3x")]
        + 4 * [Card("Sauveteuse", current_set, Level.B, power=4)]
        + 4 * [Card("Sous-marin", current_set, Level.C, power=9)]
        + 2 * [Card("Kraken", current_set, Level.C, power=7, text="Rare 2x")]
    )

    current_set = Set.FILM_STUDIO
    film_deck = (
        2 * [Card("T-rex", current_set, Level.C, power=7, text="Rare 2x")]
        + 3 * [Card("Chat", current_set, Level.A, power=3, text="Rare 3x")]
        + 4 * [Card("Star du cinéma", current_set, Level.A, power=2)]
        + 4 * [Card("Gangster", current_set, Level.A, power=2)]
        + 4 * [Card("Maquilleur", current_set, Level.A, power=1)]
        + 4 * [Card("Héroïne", current_set, Level.C, power=5)]
        + 4 * [Card("Cowboy", current_set, Level.B, power=3)]
        + 4 * [Card("Réalisatrice", current_set, Level.B, power=4)]
        + 4 * [Card("Tic tac", current_set, Level.B, power=4)]
        + 3 * [Card("Lion", current_set, Level.B, power=5, text="Rare 3x")]
        + 4 * [Card("Super vilain", current_set, Level.C, power=10)]
    )

    current_set = Set.HAUNTED_HOUSE
    haunted_deck = (
        4 * [Card("Majordome", current_set, Level.A, power=1)]
        + 3 * [Card("Araignée", current_set, Level.A, power=3, text="Rare 3x")]
        + 8 * [Card("Squelette", current_set, Level.A, power=2, text="Commune 8x")]
        + 4 * [Card("Ado", current_set, Level.B, power=2)]
        + 4 * [Card("Nécromancienne", current_set, Level.B, power=3)]
        + 3 * [Card("Chauve-souris", current_set, Level.B, power=5, text="Rare 3x")]
        + 4 * [Card("Fantôme", current_set, Level.B, power=1)]
        + 4 * [Card("Vampire", current_set, Level.C, power=4)]
        + 4 * [Card("Aspirateur", current_set, Level.C, power=5)]
        + 2 * [Card("Loup-garou", current_set, Level.C, power=7, text="Rare 2x")]
    )

    current_set = Set.OUTER_SPACE
    space_deck = (
        3 * [Card("I.A.", current_set, Level.A, power=2, text="Rare 3x")]
        + 3 * [Card("Vache", current_set, Level.A, power=3, text="Rare 3x")]
        + 4 * [Card("Métaforme", current_set, Level.A, power=2)]
        + 4 * [Card("Capsule", current_set, Level.A, power=1)]
        + 4 * [Card("Ovni", current_set, Level.B, power=3)]
        + 2 * [Card("Blob", current_set, Level.C, power=7, text="Rare 2x")]
        + 3 * [Card("E.T.", current_set, Level.B, power=5, text="Rare 3x")]
        + 4 * [Card("Fanfare", current_set, Level.B, power=3)]
        + 5 * [Card("Clones", current_set, Level.B, power=4, text="Commune 5x")]
        + 4 * [Card("Geek", current_set, Level.C, power=6)]
        + 4 * [Card("Hologramme", current_set, Level.C, power=4)]
    )

    current_set = Set.FUNFAIR
    funfair_deck = (
        2 * [Card("Peluche", current_set, Level.C, power=7, text="Rare 2x")]
        + 3 * [Card("Canard géant", current_set, Level.B, power=5, text="Rare 3x")]
        + 4 * [Card("Mime", current_set, Level.B, power=1)]
        + 4 * [Card("Clairvoyante", current_set, Level.B, power=4)]
        + 4 * [Card("Pyrotechnicienne", current_set, Level.B, power=4)]
        + 4 * [Card("Illusionniste", current_set, Level.C, power=5)]
        + 4 * [Card("Clown", current_set, Level.A, power=1)]
        + 4 * [Card("Vendeuse", current_set, Level.A, power=2)]
        + 4 * [Card("Jongleur", current_set, Level.A, power=2)]
        + 3 * [Card("Poney", current_set, Level.A, power=3, text="Rare 3x")]
        + 4 * [Card("Auto tamponneuse", current_set, Level.C, power=6)]
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
