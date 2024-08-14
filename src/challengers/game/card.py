import json
from typing import Self
from enum import Enum


class Set(Enum):
    CITY = 0
    CASTLE = 1
    FUNFAIR = 2
    OUTER_SPACE = 3
    FILM_STUDIO = 4
    HAUNTED_HOUSE = 5
    SHIPWRECK = 6


class Level(Enum):
    S = 0
    A = 1
    B = 2
    C = 3


class Card:
    cards: list[Self] = []

    def __init__(self, id: int, name: str, set: Set, level: Level, power: int = 0):
        self.id = id
        self.name = name
        self.set = set
        self.level = level
        self.power = power

    def __str__(self):
        return (
            "Card "
            + str(self.id)
            + ":\n\t"
            + self.name
            + ", "
            + self.set.name
            + ", "
            + self.level.name
            + "\n\tPower: "
            + str(self.power)
        )

    @classmethod
    def create(
        cls,
        id: int,
        name: str,
        set: Set,
        level: Level,
        power: int = 0,
        amount: int = 1,
    ):
        cards = []
        for _ in range(amount):
            cards.append(Card(id, name, set, level, power))
        cls.cards += cards
        return cards

    @classmethod
    def throw_all_cards(cls) -> list[Self]:
        cards = cls.cards.copy()
        cls.cards = []
        return cards


class CardSerializer:
    @staticmethod
    def load_card(
        dict_card: dict, use_serialized_amount: bool = True, amount: int = 1
    ) -> list[Card]:
        try:
            if use_serialized_amount:
                amount = dict_card["amount"]

            id = dict_card["id"]
            name = dict_card["name"]
            set = dict_card["set"]
            level = dict_card["level"]
            power = dict_card["power"]

            cards = Card.create(id, name, set, level, power, amount)
            return cards

        except ValueError as error:
            print(error, ": Wrong json object or wrong types used")

    @staticmethod
    def load_cards(list_cards: list[dict]) -> list[Card]:
        cards = []
        for dict_card in list_cards:
            cards += CardSerializer.load_card(dict_card)
        return cards

    @staticmethod
    def load_cards_from_file(file_path: str) -> list[Card]:
        list_cards = json.load(file_path)
        return CardSerializer.load_cards(list_cards)

    @staticmethod
    def dump_card(card: Card, amount: int = 1) -> dict:
        dict_card = {
            "id": str(card.id),
            "name": card.name,
            "set": card.set.name,
            "level": card.level.name,
            "power": str(card.power),
            "amount": str(amount),
        }
        return dict_card

    @staticmethod
    def dump_cards(cards: list[Card], amounts: list[int] = None) -> list[dict]:
        if not amounts or len(cards) != len(amounts):
            amounts = [1] * len(cards)
        list_cards = []
        for i in range(len(cards)):
            list_cards += CardSerializer.dump_card(cards[i], amounts[i])
        return list_cards

    @staticmethod
    def dump_cards_into_file(cards: list[Card], file_path: str):
        list_cards = CardSerializer.dump_cards(cards)
        json.dump(list_cards, file_path)
