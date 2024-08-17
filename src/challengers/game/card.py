import json
from typing import Self
from enum import Enum
import random


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

    def __eq__(self, other: Self) -> bool:
        # TODO: Put other attributes too ?
        return self.id == other.id

    def copy(self):
        new_card = Card(self.id, self.name, self.set, self.level, self.power)
        return new_card


class CardList:
    def __init__(self, card_list: list[Card] = None):
        if card_list:
            self.elements: list[Card] = card_list
        else:
            self.elements = []

    def __str__(self):
        string = ""
        for card in self.elements:
            string += str(card) + "\n"
        return string

    def __add__(self, other: Self) -> Self:
        return CardList(self.elements + other.elements)

    def __iter__(self):
        self.i = 0
        return self

    def __next__(self):
        if self.i < len(self.elements):
            card = self.elements[self.i]
            self.i += 1
            return card
        else:
            raise StopIteration

    def __len__(self):
        return len(self.elements)

    def __getitem__(self, key):
        return self.elements[key]

    def append(self, card: Card, amount: int = 1):
        if amount < 1:
            return ValueError

        self.elements.append(card)
        for _ in range(amount - 1):
            self.elements.append(card.copy())

    def clear(self):
        self.elements = []

    def shuffle(self):
        random.shuffle(self.elements)

    def draw(self):
        if self.elements:
            return self.elements.pop()
        return None

    def remove(self, card: Card):
        self.elements.remove(card)


class CardSerializer:
    @staticmethod
    def load_card(dict_card: dict, use_serialized_amount: bool = True, amount: int = 1) -> CardList:
        try:
            if use_serialized_amount:
                amount = int(dict_card["amount"])

            id = int(dict_card["id"])
            name = dict_card["name"]
            set = Set[dict_card["set"]]
            level = Level[dict_card["level"]]
            power = int(dict_card["power"])

            loaded_cards = CardList()
            loaded_cards.append(Card(id, name, set, level, power), amount)
            return loaded_cards

        except ValueError as error:
            print(error, ": Wrong json object or wrong types used")

    @staticmethod
    def load_cards(list_cards: list[dict]) -> CardList:
        cards = CardList()
        for dict_card in list_cards:
            cards += CardSerializer.load_card(dict_card)
        return cards

    @staticmethod
    def load_cards_from_file(file_path: str) -> CardList:
        file = open(file_path, "r")
        list_cards = json.load(file)
        file.close()
        return CardSerializer.load_cards(list_cards)

    @staticmethod
    def dump_card(card: Card, amount: int = 1) -> dict:
        dict_card = {
            "id": card.id,
            "name": card.name,
            "set": card.set.name,
            "level": card.level.name,
            "power": card.power,
            "amount": amount,
        }
        return dict_card

    @staticmethod
    def dump_cards(cards: CardList, amounts: list[int] = None) -> list[dict]:
        if not amounts or len(cards) != len(amounts):
            amounts = [1] * len(cards)
        list_cards = []
        for i in range(len(cards)):
            list_cards.append(CardSerializer.dump_card(cards[i], amounts[i]))
        return list_cards

    @staticmethod
    def dump_cards_into_file(cards: CardList, file_path: str):
        list_cards = CardSerializer.dump_cards(cards)
        file = open(file_path, "w")
        json.dump(list_cards, file)
        file.close()
