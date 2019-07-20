from models import Detail, create_detail_from_data
from board import Board
from typing import List, Generator, Tuple 
from copy import deepcopy
from random import shuffle


class GameLogic(object):

    def __init__(self):
        green = create_detail_from_data('GREEN', [[[0, 0], [1, 0]], [[1, 0], [1, 1]],
            [[0, 0], [1, 1]]])
        pink = create_detail_from_data('PINK',[[[0, 0], [1, 0]], [[0, 0], [1, 0]],
            [[1, 0], [1, 1]], [[0, 0], [1, 1]]])
        blue = create_detail_from_data('BLUE', [[[0, 0], [1, 0]], [[1, 0], [1, 0]],
            [[0, 0], [1, 0]], [[1, 0], [1, 1]]])
        yellow = create_detail_from_data('YELLOW', [[[0, 0], [1, 1]], [[0, 0], [1, 0]],
            [[1, 0], [1, 0]], [[1, 0], [1, 0]]])
        red = create_detail_from_data('RED', [[[1, 0], [1, 1]], [[0, 0], [1, 0]],
            [[0, 0], [1, 0]], [[0, 0], [1, 1]]])
        fox_red = create_detail_from_data('FOXRED', [[[0, 0], [1, 0]], [[1, 0], [1, 1]],
            [[0, 0], [1, 0]], [[0, 0], [1, 1]]])
        light_blue = create_detail_from_data('LIGHTBLUE', [[[0, 0], [1, 0]], [[1, 0], [1, 1]],
            [[0, 0], [1, 1]], [[0, 0], [1, 0]]])
        violet = create_detail_from_data('VIOLET', [[[0, 0], [1, 1]], [[1, 0], [1, 0]],
            [[1, 0], [1, 0]]])
        light_green = create_detail_from_data('LIGHTGREEN', [[[1, 0], [1, 1]], [[0, 0], [1, 0]],
            [[0, 0], [1, 1]]])
        dark_blue = create_detail_from_data('DARKBLUE', [[[0, 0], [1, 1]], [[1, 0], [1, 0]],
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
        self.__details.index(detail)
        self.__board.add_object(detail, coordinates[0], coordinates[1])
        self.__details.remove(detail)


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


def find_solutions2(game_logic: GameLogic) -> Generator[Board, Board, bool]:
    _list = list()
    print(game_logic.details[:1])
    for detail in game_logic.details[:1]:
        for (current_state_of_detail, coordinates) in try_to_put_detail(detail, game_logic.board):
            _list.append((current_state_of_detail, coordinates))
    print(len(_list))
    # print(_list)




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
