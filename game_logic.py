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
        green = create_detail_from_data('GREEN', 'G',[[[0, 0], [1, 0]], [[1, 0], [1, 1]],
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

    def has_details(self) -> bool:
        return len(self.__details)

    @property
    def first_detail(self):
        return self.__details[0]

    def shuffle_details(self):
        shuffle(self.__details)

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


def find_solutions(game_logic: GameLogic, attempt: int) -> Generator[Board, Board, bool]:
    attempt += 1
    _game_logic = deepcopy(game_logic)
    while _game_logic.has_details():
        detail = _game_logic.first_detail
        (can_do_it, coordinates) = try_to_put_detail(detail, board)
        if can_do_it:
            _game_logic.put_detail_on_board(detail, coordinates)
        else:
            break
    if not _game_logic.has_details():
        yield _game_logic.board
    else:
        _game_logic = deepcopy(game_logic)
        _game_logic.shuffle_details()
        yield from find_solutions(_game_logic, attempt)

from multiprocessing import Process

def find_solutions2(game_logic: GameLogic) -> Generator[Board, Board, bool]:
    _map = dict()
    for detail in game_logic.details:
        _map[detail.name] = []
        for (current_state_of_detail, coordinates) in try_to_put_detail(detail, game_logic.board):
            _map[detail.name].append((current_state_of_detail, coordinates))
        print("Detail '%s' -> positions -> %d" % (detail.name, len(_map[detail.name])))


    params = [_map[detail_name] for detail_name in _map]

    _list_of_possible_combinations = [path for path in product(*params)] 
    print(len(_list_of_possible_combinations))
    shuffle(_list_of_possible_combinations)

    i = 0
    quarter = int(len(_list_of_possible_combinations)/4)
    print(quarter)

    _real_solutions_map = dict() 
    for thread in range(4):
        _real_solutions_map[thread] = []


    s = SolutionCheckerThread('S1', game_logic, _list_of_possible_combinations, _real_solutions_map[0])
    s.run()    

    for _solution_result in _real_solutions_map:
        for _solution in _real_solutions_map[_solution_result]:
            yield _solution



class SolutionCheckerThread(object):

    def __init__(self, name_of_thread: str, game_logic: GameLogic, _combinations: List, result: List):
        threading.Thread.__init__(self) 
        self._name_of_thread = name_of_thread
        self._game_logic = game_logic
        self._combinations = _combinations
        self._result = result

    def run(self):
        print(self._name_of_thread)
        for _combination in self._combinations:
            _copy_of_game_logic = deepcopy(self._game_logic)
            i = 0
            for (_detail, _coordinates) in _combination:
                try:
                    _copy_of_game_logic.put_detail_on_board(_detail, _coordinates)
                    i += 1
                except Exception:
                    if (len(_combination) - i)  == 0:
                        print("Left details: %s\nBoard: %s" % (len(_combination) - i, _copy_of_game_logic.board))
                    break

            if _copy_of_game_logic.board.is_complete():
                self._result.append(_copy_of_game_logic.board)


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
