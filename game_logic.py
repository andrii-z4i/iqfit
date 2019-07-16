from models import Detail, create_detail_from_data
from board import Board
from typing import List


class GameLogic(object):

    def __init__(self):
        green = create_detail_from_data([[[0, 0], [1, 0]], [[1, 0], [1, 1]],
            [[0, 0], [1, 1]]])
        pink = create_detail_from_data([[[0, 0], [1, 0]], [[0, 0], [1, 0]],
            [[1, 0], [1, 1]], [[0, 0], [1, 1]]])
        blue = create_detail_from_data([[[0, 0], [1, 0]], [[1, 0], [1, 0]],
            [[0, 0], [1, 0]], [[1, 0], [1, 1]]])
        yellow = create_detail_from_data([[[0, 0], [1, 1]], [[0, 0], [1, 0]],
            [[1, 0], [1, 0]], [[1, 0], [1, 0]]])
        red = create_detail_from_data([[[1, 0], [1, 1]], [[0, 0], [1, 0]],
            [[0, 0], [1, 0]], [[0, 0], [1, 1]]])
        fox_red = create_detail_from_data([[[0, 0], [1, 0]], [[1, 0], [1, 1]],
            [[0, 0], [1, 0]], [[0, 0], [1, 1]]])
        light_blue = create_detail_from_data([[[0, 0], [1, 0]], [[1, 0], [1, 1]],
            [[0, 0], [1, 1]], [[0, 0], [1, 0]]])
        violet = create_detail_from_data([[[0, 0], [1, 1]], [[1, 0], [1, 0]],
            [[1, 0], [1, 0]]])
        light_green = create_detail_from_data([[[1, 0], [1, 1]], [[0, 0], [1, 0]],
            [[0, 0], [1, 1]]])
        dark_blue = create_detail_from_data([[[0, 0], [1, 1]], [[1, 0], [1, 0]],
            [[0, 0], [1, 1]]])

        self.__named_details = {
            'RED': red,
            'GREEN': green,
            'BLUE': blue,
            'YELLOW': yellow,
            'FOXRED': fox_red,
            'LIGHTBLUE': light_blue,
            'VIOLET': violet,
            'LIGHTGREEN': light_green,
            'DARKBLUE': dark_blue
        }
        self.__details = [red, green, blue, yellow, fox_red, light_blue,
                violet, light_green, dark_blue]
        self.__board = Board(5, 10)

    @property
    def details(self) -> List[Detail]:
        return self.__details

    @property
    def board(self) -> Board:
        return self.__board

    def get_detail_by_name(self, name: str) -> Detail:
        if name in self.__named_details:
            return self.__named_details[name]

        raise Exception('Element not found')

    def put_detail_on_board(
            self, detail_name: str, coordinates: tuple) -> None:
        _detail = self.get_detail_by_name(detail_name)
        self.__details.index(_detail)
        self.__board.add_object(_detail, coordinates[0], coordinates[1])
        self.__details.remove(_detail)

    def find_solution(self) -> bool:
        for detail in self.__details:
            for coordinates in self.get_coordinates():
                for side in detail.sides():
                    # try to put detail
                    continue

        pass
