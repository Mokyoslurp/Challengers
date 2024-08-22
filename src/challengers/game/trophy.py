import random
import json


class Trophy:
    def __init__(self, round: int, fans: int):
        self.round = round
        self.fans = fans


class TrophyDict:
    def __init__(self):
        self.elements: dict[int, list[Trophy]] = {}

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
    def load_trophy(dict_trophy: dict) -> Trophy:
        try:
            round = int(dict_trophy["round"])
            fans = int(dict_trophy["fans"])

            return Trophy(round, fans)

        except ValueError as error:
            print(error, ": Wrong json object or wrong types used")

    @staticmethod
    def load_trophies(list_trophies: list[dict]) -> TrophyDict:
        trophies_dict = TrophyDict()
        for dict_trophy in list_trophies:
            trophies_dict.append(TrophySerializer.load_trophy(dict_trophy))

        return trophies_dict

    @staticmethod
    def load_trophies_from_file(file_path: str) -> TrophyDict:
        file = open(file_path, "r")
        list_trophies = json.load(file)
        file.close()
        return TrophySerializer.load_trophies(list_trophies)

    @staticmethod
    def dump_trophy(trophy: Trophy) -> dict:
        dict_trophy = {
            "round": trophy.round,
            "fans": trophy.fans,
        }
        return dict_trophy

    @staticmethod
    def dump_trophies(trophies: TrophyDict) -> list[dict]:
        list_trophies = []
        for round in trophies:
            for trophy in trophies[round]:
                print(trophy)
                list_trophies.append(TrophySerializer.dump_trophy(trophy))
        return list_trophies

    @staticmethod
    def dump_trophies_into_file(trophies: TrophyDict, file_path: str):
        list_trophies = TrophySerializer.dump_trophies(trophies)
        file = open(file_path, "w")
        json.dump(list_trophies, file)
        file.close()
