import random
from typing import Self


class Trophy:
    trophies: dict[int, list[Self]] = {}

    def __init__(self, round: int, fans: int):
        self.round = round
        self.fans = fans

    @classmethod
    def create(
        cls,
        round: int,
        fans: int,
    ) -> Self:
        trophy = Trophy(round, fans)

        if cls.trophies.get(round):
            cls.trophies[round].append(trophy)
        else:
            cls.trophies[round] = [trophy]
        return trophy

    @classmethod
    def shuffle_trophies(cls):
        for round in cls.trophies:
            random.shuffle(cls.trophies[round])

    @classmethod
    def draw_trophy(cls, round: int) -> Self:
        if cls.trophies.get(round):
            trophy = cls.trophies[round].pop()
            return trophy

        return None
