from models import Detail, Side
from typing import List, Generator


class Board(object):

    def __init__(self, height: int, width: int):
        self.__height = height
        self.__width = width
        self.__board = [[0 for y in range(width)] for x in range(height)]
        self.__str_board = [['-' for y in range(width)] for x in range(height)]
        self.__objects = {}  # key - Detail, value (tuple) most left coordinate

    @property
    def board(self) -> List[List[int]]:
        return self.__board

    def __repr__(self):
        _str_board = [' '.join([self.__str_board[x][y] for y in range(self.__width)]) for x in range(self.__height)]
        return "\nObjects on board: %d\n%s" % (len(self.__objects), "\n".join(_str_board))

    def __str__(self):
        return self.__repr__()

    @property
    def objects(self) -> dict:
        return self.__objects

    def add_object(self, detail: Detail, x: int, y: int) -> None:
        if not self._check_if_detail_can_fit(detail, x, y):
            raise Exception("Doesn't fit")

        self.__objects[detail] = tuple([x, y])
        self._update_board(self.__objects)

    def is_complete(self) -> bool:
       _side = Side(self.__height, self.__width)
       _side.fill(self.__board)
       return _side.calculate_square() == (self.__height * self.__width)

    def get_coordinates(self) -> Generator[tuple, tuple, None]:
        for y in range(len(self.__board)):
            for x in range(len(self.__board[0])):
                if not self.__board[y][x]:
                    yield (y, x)

    def _check_if_detail_can_fit(self, detail: Detail, x: int, y: int) -> bool:
        _side_index = detail.side_index
        if detail.get_current_side().calculate_square() < \
                detail.get_opposite_side().calculate_square():
            raise Exception("Rotate detail")

        _side = detail.get_current_side()
        _y_position = y + _side.height - 1 - _side.get_height_offset()
        _x_position = x + _side.width - 1 - _side.get_width_offset()
        if (y - _side.get_height_offset()) < 0 or _y_position > self.__height or \
                (x - _side.get_width_offset()) < 0 or _x_position > self.__width:
            raise Exception("Detail is out of boundaries")

        i = 0
        for row in _side.value:
            j = 0
            for value in row:
                if value and self.__board[y + i - _side.get_height_offset()][x + j - _side.get_width_offset()] :
                    return False
                j += 1
            i += 1

        return True 

    def _update_board(self, objects: dict) -> None:
        _new_board = [[0 for x in range(self.__width)] for y in range(self.__height)]
        _new_str_board = [['-' for x in range(self.__width)] for y in range(self.__height)]

        for detail in self.__objects:
            _coordinates = self.__objects[detail]
            _side = detail.get_current_side()
            self._fill_coordinates_from_side(_new_board, _side, _coordinates)
            self._fill_str_coordinates_from_side(_new_str_board, _side, _coordinates, detail.symbol)
        
        self.__board = _new_board
        self.__str_board = _new_str_board

    def _fill_coordinates_from_side(self, board: List[List[int]], side: Side, coordinates: tuple) -> None:
        i = 0
        for row in side.value:
            j = 0
            for value in row:
                if value:
                    board[coordinates[1] + i - side.get_height_offset()][coordinates[0] + j - side.get_width_offset()] = value
                j += 1
            i += 1

    def _fill_str_coordinates_from_side(self, board: List[List[chr]], side: Side, coordinates: tuple, symbol: chr) -> None:
        i = 0
        for row in side.value:
            j = 0
            for value in row:
                if value:
                    board[coordinates[1] + i - side.get_height_offset()][coordinates[0] + j - side.get_width_offset()] = symbol 
                j += 1
            i += 1
