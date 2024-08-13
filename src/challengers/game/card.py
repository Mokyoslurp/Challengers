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
