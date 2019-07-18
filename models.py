from typing import List

from copy import deepcopy

class Side(object):
    def __init__(self, height: int, width: int):
        self.__array = [[0 for i in range(width)] for k in range(height)]
    
    @property
    def value(self) -> List[List[int]]:
        return self.__array

    @property
    def width(self) -> int:
        return len(self.__array[0])

    @property
    def height(self) -> int:
        return len(self.__array)

    def fill(self, side: List) -> any:
        if len(side) != self.height:
            raise Exception("Wrong height")
        if len(side[0]) != self.width:
            raise Exception("Wrong width")

        self._check_data(side)
        self.__array = deepcopy(side)

    def calculate_square(self) -> int:
        _square = 0
        for row in self.__array:
            for value in row:
                _square += value

        return _square

    def _check_data(self, side: List) -> None:
        for x in side:
            for value in x:
                if value != 0 and value != 1:
                    raise Exception("Wrong data")
    
    def rotate(self, direction = 1) -> None: 
        # direction = 1 (left)
        # direction = -1 (Right)
        
        _new_array = [[0 for i in range(self.height)] for k in range(self.width)]

        if direction == 1:
            self._rotate_left(_new_array, self.__array)
        elif direction == -1:
            self._rotate_right(_new_array, self.__array)
        else:
            raise Exception("Wrong direction")
        self.__array = _new_array

    def _rotate_left(self, new_array: List, old_array: List) -> None:
        i = 0
        for row in old_array:
            j = 0
            for new_row in new_array:
                new_array[j][i] = row[len(row) - j - 1]
                j += 1
            i += 1

    def _rotate_right(self, new_array: List, old_array: List) -> None:
        i = 0
        for row in old_array[::-1]:
            j = 0
            for new_row in new_array:
                new_array[j][i] = row[j]
                j += 1
            i += 1


class Detail(object):

    def __init__(self, height: int, width: int, depth: int, name: str = ''):
        self.__object = [[[0 for k in range(depth)] for j in range(width)] for i in range(height)]
        self.__side: int = 2
        self.__rotation_steps: List[int] = []
        self.__name = name

    def __str__(self):
        return self.__name

    def __repr__(self):
        return self.__name

    @property
    def name(self):
        return self.__name
    
    @property
    def value(self) -> List[List[List[int]]]:
        return self.__object

    @property
    def width(self) -> int:
        return len(self.__object[0])

    @property
    def height(self) -> int:
        return len(self.__object)

    @property
    def depth(self) -> int:
        return len(self.__object[0][0])

    @property
    def side_index(self) -> int:
        return self.__side

    def rotate(self, direction = 1) -> None:  
        # direction = 1 - left, 
        # direction = -1 - Right
        if direction != 1 and direction != -1:
            raise Exception("Wrong direction")

        last_step = [self.__rotation_steps[-1]] \
                if len(self.__rotation_steps) else []
        if len(last_step) and last_step[0] != direction:
            self.__rotation_steps = self.__rotation_steps[:-1]
        else:
            self.__rotation_steps.append(direction)

    def chose_side(self, side_index: int) -> None:
        if side_index < 1 or side_index > 5:
            raise Exception("Only 2..5 sides")

        self.__side = side_index

    def fill(self, array: List) -> None:
        if len(array) != self.height:
            raise Exception("Wrong height")
        if len(array[0]) != self.width:
            raise Exception("Wrong width")
        if len(array[0][0]) != self.depth:
            raise Exception("Wrong depth")

        self._check_data(array)
        self.__object = deepcopy(array)

    def _check_data(self, array: List[List[List[int]]]):
        for h in range(self.height):
            for w in range(self.width):
                for d in range(self.width):
                    if array[h][w][d] != 1 \
                        and array[h][w][d] != 0:
                        raise Exception("Wrong data")


    def get_side(self, side: int) -> Side:
        if side < 0 or side > 5:
            raise Exception("Side has to be 0..5")
        _return: Side = None
        if side == 0:
            _return = Side(self.width, self.depth)
            _return.fill(self.__object[0])
        elif side == 1:
            _return = Side(self.depth, self.width)
            _return.fill(self.__object[-1][::-1])
        elif side == 2:
            _return = Side(self.height, self.width)
            _return.fill([el[-1] for el in self.__object])
        elif side == 3:
            _return = Side(self.height, self.depth)
            _return.fill([[side[-1] for side in el[::-1]] for el in self.__object])
        elif side == 4:
            _return = Side(self.height, self.width)
            _return.fill([el[0][::-1] for el in self.__object])
        elif side == 5:
            _return = Side(self.height, self.depth)
            _return.fill([[side[0] for side in el] for el in self.__object])
        if side != 0 and side != 1:
            self._apply_rotation(_return)
        return _return

    def _apply_rotation(self, side: Side) -> None:
        for direction in self.__rotation_steps:
            side.rotate(direction)

    def get_current_side(self) -> Side:
        return self.get_side(self.__side)

    def get_opposite_side(self) -> Side:
        _opposite_sides = {
            0: 1,
            1: 0,
            2: 4,
            3: 5,
            4: 2,
            5: 3
        } 

        return self.get_side(_opposite_sides[self.__side])

    @property
    def sides(self):
        return [2, 3, 4, 5] 
    

        
def create_detail_from_data(name: str, data: List[List[List[int]]]) -> Detail:
    _return = Detail(len(data), len(data[0]), len(data[0][0]), name)
    _return.fill(data)
    return _return
