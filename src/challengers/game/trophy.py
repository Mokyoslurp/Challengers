import random
import json
from typing import Self, MutableMapping, Any
from dataclasses import dataclass, fields


@dataclass
class Trophy:
    round: int = 0
    fans: int = 0

    def __str__(self):
        return "Round: " + self.round + ", " + "Fans: " + self.fans

    @classmethod
    def get_fields(cls):
        return [field for field in fields(cls) if not field.name.startswith("_")]

    def as_dict(self) -> dict:
        data: dict = {}
        for field in Trophy.get_fields():
            data[field.name] = str(getattr(self, field.name))
        return data

    @staticmethod
    def from_dict(data: dict) -> Self:
        init_values: MutableMapping[str, Any] = {}
        for field in Trophy.get_fields():
            init_values[field.name] = int(data[field.name])
        card = Trophy(**init_values)
        return card


class TrophyDict:
    def __init__(self):
        self.elements: dict[int, list[Trophy]] = {}

    def __str__(self):
        string = ""
        for round in self.elements:
            string += "Round " + str(round) + ":"
            for trophy in self.elements[round]:
                string += " " + str(trophy.fans)
            string += "\n"
        return string

    def __iter__(self):
        self.i = 0
        self.j = 0
        return self

    def __next__(self):
        if self.i < len(self.elements):
            if self.j < len(self.elements[self.i]):
                trophy = self.elements[self.i][self.j]
                self.j += 1
                return trophy
            else:
                self.i += 1
                self.j = 0
                return self.__next__()
        else:
            raise StopIteration

    def __len__(self):
        length = 0
        for round in self.elements:
            length += len(self.elements[round])
        return round

    def __getitem__(self, key):
        return self.elements[key]

    def append(self, trophy: Trophy):
        if trophy.round in self.elements:
            self.elements[trophy.round].append(trophy)
        else:
            self.elements[trophy.round] = [trophy]

    def shuffle(self):
        for round in self.elements:
            random.shuffle(self.elements[round])

    def draw(self, round: int) -> Trophy:
        if self.elements.get(round):
            trophy = self.elements[round].pop()
            return trophy


class TrophySerializer:
    @staticmethod
    def load_trophy(data: dict) -> Trophy:
        trophy = Trophy.from_dict(data)
        return trophy

    @staticmethod
    def load_trophies(data: list[dict]) -> TrophyDict:
        trophies_dict = TrophyDict()
        for trophy_data in data:
            trophies_dict.append(TrophySerializer.load_trophy(trophy_data))

        return trophies_dict

    @staticmethod
    def load_trophies_from_file(file_path: str) -> TrophyDict:
        file = open(file_path, "r")
        list_trophies = json.load(file)
        file.close()
        return TrophySerializer.load_trophies(list_trophies)

    @staticmethod
    def dump_trophy(trophy: Trophy) -> dict:
        data = trophy.as_dict()
        return data

    @staticmethod
    def dump_trophies(trophies: TrophyDict) -> list[dict]:
        data = []
        for trophy in trophies:
            data.append(TrophySerializer.dump_trophy(trophy))
        return data

    @staticmethod
    def dump_trophies_into_file(trophies: TrophyDict, file_path: str):
        data = TrophySerializer.dump_trophies(trophies)
        file = open(file_path, "w")
        json.dump(data, file)
        file.close()
