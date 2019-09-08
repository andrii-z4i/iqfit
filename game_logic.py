from models import Detail, create_detail_from_data
from board import Board
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


def find_solutions2(game_logic: GameLogic) -> Generator[Board, Board, None]:
    _map = dict()
    for detail in game_logic.details:
        _map[detail.name] = []
        for (current_state_of_detail, coordinates) in try_to_put_detail(detail, game_logic.board):
            _map[detail.name].append((current_state_of_detail, coordinates))
        print("Detail '%s' -> positions -> %d" % (detail.name, len(_map[detail.name])))

    params = [_map[detail_name] for detail_name in _map]

    s = SolutionChecker('S1', game_logic, params)
    for solution in s.run():
        yield solution


class SolutionChecker(object):

    def __init__(self, name_of_thread: str, game_logic: GameLogic, _combinations: List):
        threading.Thread.__init__(self)
        self._name_of_thread = name_of_thread
        self._game_logic = game_logic
        self._combinations = _combinations

    def run(self) -> Generator[Board, None, None]:
        for _combination in product(*self._combinations):
            _copy_of_game_logic = deepcopy(self._game_logic)
            i = 0
            for (_detail, _coordinates) in _combination:
                try:
                    _copy_of_game_logic.put_detail_on_board(_detail, _coordinates)
                    i += 1
                except Exception:
                    break

            if _copy_of_game_logic.board.is_complete():
                yield _copy_of_game_logic.board


def try_to_put_detail(detail: Detail, board: Board) -> Generator[Tuple[Detail, Tuple], bool, bool]:
    j = 0
    for coordinates in board.get_coordinates():
        for side in detail.sides:
            detail.chose_side(side)
            for i in range(4):
                detail.rotate()
                try:
                    _board = deepcopy(board)
                    _board.add_object(detail, coordinates[1], coordinates[0])
                    yield (deepcopy(detail), (coordinates[1], coordinates[0]))
                except Exception as ex:
                    j += 1
    return False
