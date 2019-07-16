from models import Detail, Side
from typing import List, Generator


class Board(object):

    def __init__(self, height: int, width: int):
        self.__height = height
        self.__width = width
        self.__board = [[0 for y in range(width)] for x in range(height)]
        self.__objects = {}  # key - Detail, value (tuple) most left coordinate

    @property
    def board(self) -> List[List[int]]:
        return self.__board

    @property
    def objects(self) -> dict:
        return self.__objects

    def add_object(self, detail: Detail, x: int, y: int) -> None:
        if not self._check_if_detail_can_fit(detail, x, y):
            raise Exception("Doesn't fit")

        self.__objects[detail] = tuple([x, y])
        self._update_board(self.__objects)

    def is_complete(self) -> bool:
       _side = Side(5, 10)
       _side.fill(self.__board)
       return _side.calculate_square() == 500
    
    def get_coordinates(self) -> Generator[tuple, tuple, None]:
        for x in range(len(self.__board)):
            for y in range(len(self.__board[0])):
                if not self.__board[x][y]:
                    yield (x, y)

    def _check_if_detail_can_fit(self, detail: Detail, x: int, y: int) -> bool:
        _side_index = detail.side_index
        if detail.get_current_side().calculate_square() < \
                detail.get_opposite_side().calculate_square():
            raise Exception("Rotate detail")

        _side = detail.get_current_side()
        if _side.height + x > self.__height or \
                _side.width + y > self.__width:
            raise Exception("Detail is out of boundaries")

        i = 0
        for row in _side.value:
            j = 0
            for value in row:
                if value and self.__board[x + i][y + j] :
                    return False
                j += 1
            i += 1

        return True 

    def _update_board(self, objects: dict) -> None:
        _new_board = [[0 for y in range(self.__width)] for x in range(self.__height)]

        for detail in self.__objects:
            _coordinates = self.__objects[detail]
            _side = detail.get_current_side()
            self._fill_coordinates_from_side(_new_board, _side, _coordinates)
        
        self.__board = _new_board

    def _fill_coordinates_from_side(self, board: List[List[int]], side: Side, coordinates: tuple) -> None:
        i = 0
        for row in side.value:
            j = 0
            for value in row:
                if value:
                    board[coordinates[0] + i][coordinates[1] + j] = value
                j += 1
            i += 1

