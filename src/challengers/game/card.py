import json
from typing import Self, MutableMapping, Any
from enum import Enum
import random
from dataclasses import dataclass, fields, replace


class Set(Enum):
    CITY = 0
    CASTLE = 1
    FUNFAIR = 2
    OUTER_SPACE = 3
    FILM_STUDIO = 4
    HAUNTED_HOUSE = 5
    SHIPWRECK = 6


SET_COLORS = {
    Set.CITY: "\033[96m",  # Bright Cyan
    Set.CASTLE: "\033[34m",  # Blue
    Set.FUNFAIR: "\033[91m",  # Bright Red
    Set.OUTER_SPACE: "\033[31m",  # Red
    Set.FILM_STUDIO: "\033[92m",  # Bright Green
    Set.HAUNTED_HOUSE: "\033[90m",  # Bright Black
    Set.SHIPWRECK: "\033[36m",  # Cyan
}
END_COLOR = "\033[0m"


class Level(Enum):
    S = 0
    A = 1
    B = 2
    C = 3


@dataclass
class Card:
    name: str = ""
    set: Set = Set.CITY
    level: Level = Level.S
    power: int = 0
    text: str = ""

    drawing = None

    def __str__(self) -> str:
        if not self.drawing:
            first_line = self.name
            second_line = (
                str(self.power)
                + "|"
                + self.level.name
                + "|"
                + self.set.name.replace("_", " ").capitalize()
            )
            max_characters = max(len(first_line), len(second_line))

            first_line = (
                "|"
                + first_line
                + "".join([" " for _ in range(max_characters - len(first_line))])
                + "|\n"
            )
            second_line = (
                "|"
                + second_line
                + "".join([" " for _ in range(max_characters - len(second_line))])
                + "|\n"
            )

            inter_line = "".join(["-" for _ in range(max_characters + 2)])
            self.drawing = (
                SET_COLORS[self.set]
                + inter_line
                + "\n"
                + first_line
                + inter_line
                + "\n"
                + second_line
                + inter_line
                + END_COLOR
            )

        return self.drawing

    def __hash__(self) -> int:
        return hash(self.name)

    @classmethod
    def get_fields(cls):
        return [field for field in fields(cls) if not field.name.startswith("_")]

    def as_dict(self) -> dict:
        data: dict = {}
        for field in Card.get_fields():
            value = getattr(self, field.name)
            if field.type == Set or field.type == Level:
                value = value.name
            else:
                value = str(value)
            data[field.name] = value
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        init_values: MutableMapping[str, Any] = {}
        for field in Card.get_fields():
            value = data[field.name]
            if field.type is int:
                value = int(value)
            elif field.type is Set:
                value = Set[value]
            elif field.type is Level:
                value = Level[value]
            init_values[field.name] = value
        card = Card(**init_values)
        return card


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
            self.elements.append(replace(card))

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
    def load_card(data: dict) -> Card:
        card = Card.from_dict(data)
        return card

    @staticmethod
    def load_cards(data: list[dict]) -> CardList:
        cards = CardList()
        for card_data in data:
            cards.append(CardSerializer.load_card(card_data))
        return cards

    @staticmethod
    def load_cards_from_file(file_path: str) -> CardList:
        file = open(file_path, "r")
        data = json.load(file)
        file.close()
        return CardSerializer.load_cards(data)

    @staticmethod
    def dump_card(card: Card) -> dict:
        data = card.as_dict()
        return data

    @staticmethod
    def dump_cards(cards: CardList) -> list[dict]:
        data = []
        for i in range(len(cards)):
            data.append(CardSerializer.dump_card(cards[i]))
        return data

    @staticmethod
    def dump_cards_into_file(cards: CardList, file_path: str):
        data = CardSerializer.dump_cards(cards)
        file = open(file_path, "w")
        json.dump(data, file)
        file.close()
