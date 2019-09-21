from models import Detail, Side
from typing import List, Generator, Tuple


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
        for x in range(self.__width):
            for y in range(self.__height):
                # if not self.__board[y][x]:
                yield (x, y)

    def _check_if_detail_can_fit(self, detail: Detail, x: int, y: int) -> bool:
        _side_index = detail.side_index
        if detail.get_current_side().calculate_square() < \
                detail.get_opposite_side().calculate_square():
            return False

        _side = detail.get_current_side()
        try:
            _detail_matrix = self._generate_matrix_with_detail(_side, (x, y))
        except Exception as ex:
            return False

        for x in range(self.__width):
            for y in range(self.__height):
                if _detail_matrix.value[y][x] + self.__board[y][x] > 1:
                    return False

        return True

    def _generate_matrix_with_detail(self, side: Side, coordinates: Tuple[int, int]) -> Side:
        _empty_side: Side = Side(self.__height, self.__width)  # filled by '0'
        _x = coordinates[0]
        _y = coordinates[1]

        if (_x >= _empty_side.width) or (_x + side.width) > _empty_side.width:
            raise Exception('Can\'t fit by width')
        if (_y >= _empty_side.height) or (_y + side.height) > _empty_side.height:
            raise Exception('Can\'t fit by height')

        for x in range(side.width):
            for y in range(side.height):
                _empty_side.value[y + _y][x + _x] = side.value[y][x]

        return _empty_side

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

    def _fill_coordinates_from_side(self, board: List[List[int]], side: Side, coordinates: Tuple[int, int]) -> None:
        _detail_matrix = self._generate_matrix_with_detail(side, coordinates)

        for x in range(self.__width):
            for y in range(self.__height):
                board[y][x] += _detail_matrix.value[y][x]
                if board[y][x] > 1:
                    raise Exception('Something went wrong')

    def _fill_str_coordinates_from_side(self, board: List[List[chr]], side: Side, coordinates: Tuple[int, int], symbol: chr) -> None:
        _detail_matrix = self._generate_matrix_with_detail(side, coordinates)

        for x in range(self.__width):
            for y in range(self.__height):
                if _detail_matrix.value[y][x] == 1:
                    if board[y][x] != '-':
                        raise Exception('Occupied')
                    else:
                        board[y][x] = symbol
