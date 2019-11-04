from .models import Detail, create_detail_from_data
from .board import Board
from typing import List, Generator, Tuple
from copy import deepcopy
from random import shuffle
from itertools import product
import threading
from time import sleep


class GameLogic(object):

    def __init__(self):
        green = create_detail_from_data('GREEN', 'G', [[[0, 0], [1, 0]], [[1, 0], [1, 1]],
                                                       [[0, 0], [1, 1]]])
        pink = create_detail_from_data('PINK', 'P', [[[0, 0], [1, 0]], [[0, 0], [1, 0]],
                                                     [[1, 0], [1, 1]], [[0, 0], [1, 1]]])
        blue = create_detail_from_data('BLUE', 'B', [[[0, 0], [1, 0]], [[1, 0], [1, 0]],
                                                     [[0, 0], [1, 0]], [[1, 0], [1, 1]]])
        yellow = create_detail_from_data('YELLOW', 'Y', [[[0, 0], [1, 1]], [[0, 0], [1, 0]],
                                                         [[1, 0], [1, 0]], [[1, 0], [1, 0]]])
        red = create_detail_from_data('RED', 'R', [[[1, 0], [1, 1]], [[0, 0], [1, 0]],
                                                   [[0, 0], [1, 0]], [[0, 0], [1, 1]]])
        fox_red = create_detail_from_data('FOXRED', 'F', [[[0, 0], [1, 0]], [[1, 0], [1, 1]],
                                                          [[0, 0], [1, 0]], [[0, 0], [1, 1]]])
        light_blue = create_detail_from_data('LIGHTBLUE', 'L', [[[0, 0], [1, 0]], [[1, 0], [1, 1]],
                                                                [[0, 0], [1, 1]], [[0, 0], [1, 0]]])
        violet = create_detail_from_data('VIOLET', 'V', [[[0, 0], [1, 1]], [[1, 0], [1, 0]],
                                                         [[1, 0], [1, 0]]])
        light_green = create_detail_from_data('LIGHTGREEN', 'S', [[[1, 0], [1, 1]], [[0, 0], [1, 0]],
                                                                  [[0, 0], [1, 1]]])
        dark_blue = create_detail_from_data('DARKBLUE', 'C', [[[0, 0], [1, 1]], [[1, 0], [1, 0]],
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
            'DARKBLUE': dark_blue,
            'PINK': pink
        }
        self.__details = [red, green, blue, yellow, fox_red, light_blue,
                          violet, light_green, dark_blue, pink]
        self.__board = Board(5, 10)

    @property
    def details(self) -> List[Detail]:
        return self.__details

    @property
    def first_detail(self):
        return self.__details[0]

    @property
    def board(self) -> Board:
        return self.__board

    def get_detail_by_name(self, name: str) -> Detail:
        if name in self.__named_details:
            return self.__named_details[name]

        raise Exception('Element not found')

    def put_detail_on_board(
            self, detail: Detail, coordinates: tuple) -> None:
        _detail_by_name = next(x for x in self.__details if detail.name == x.name)
        self.__details.index(_detail_by_name)
        self.__board.add_object(detail, coordinates[0], coordinates[1])
        self.__details.remove(_detail_by_name)






