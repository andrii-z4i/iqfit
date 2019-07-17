from models import Detail, create_detail_from_data
from board import Board
from typing import List, Generator, Tuple 
from copy import deepcopy


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


def find_solutions(game_logic: GameLogic) -> Generator[Board, Board, bool]:
    for detail in game_logic.details:
        _board = deepcopy(game_logic.board)
        (can_do_it, coordinates) = try_to_put_detail(detail, _board)
        if can_do_it:
            print('%s Detail was put to coordinates (%d, %d)' % (detail.name, coordinates[0], coordinates[1]))
            game_logic.put_detail_on_board(detail.name, coordinates)

def try_to_put_detail(detail: Detail, board: Board) -> Tuple[bool, Tuple]:
    j = 0
    for coordinates in board.get_coordinates():
        for side in detail.sides:
            detail.chose_side(side)
            for i in range(4):
                detail.rotate()
                try:
                    board.add_object(detail, coordinates[0], coordinates[1])
                    print('j = %d' % j)
                    return True, coordinates
                except Exception as ex:
                    # print(ex)
                    j += 1
    return False, (0, 0)
