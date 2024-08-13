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

    def __init__(self, id: int, name: str, set: Set, level: Level):
        self.id = id
        self.name = name
        self.set = set
        self.level = level

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
        )

    @classmethod
    def create(
        cls,
        id: int,
        name: str,
        set: Set,
        level: Level,
        amount: int = 1,
    ):
        cards = []
        for _ in range(amount):
            cards.append(Card(id, name, set, level))
        cls.cards += cards
        return cards
