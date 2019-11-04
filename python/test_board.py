from unittest import TestCase
from board import Board
from models import Side, Detail
from copy import deepcopy


class BoardTest(TestCase): 

    def setUp(self):
        self._empty_board_5_10 = [[0 for y in range(10)] for x in range(5)]

    def test_init(self):
        b = Board(5, 10)

        self.assertListEqual(b.board, self._empty_board_5_10)
        self.assertDictEqual(b.objects, {})

    def test_add_oject(self):
        b = Board(5, 10)
        d = Detail(3, 2, 2)
        d.fill([[[0, 0], [1, 0]], [[1, 0], [1, 1]], [[0, 0], [1, 1]]])
        b.add_object(d, 0, 1)

        _board = [[0 for y in range(10)] for x in range(5)]
        
        # 1 0 0 0 0
        # 1 1 0 0 0
        # 1 1 0 0 0
        # 0 0 0 0 0
        _board[1][0] = 1
        _board[2][0] = 1
        _board[2][1] = 1
        _board[3][0] = 1
        _board[3][1] = 1

        self.assertListEqual(b.board, _board)
        self.assertDictEqual(b.objects, {d: (0, 1)})

    def test_add_oject_out_of_boundaries(self):
        b = Board(5, 10)
        d = Detail(3, 2, 2)
        d.fill([[[0, 0], [1, 0]], [[1, 0], [1, 1]], [[0, 0], [1, 1]]])
        with self.assertRaises(Exception) as ex:
            b.add_object(d, 0, 4)
        
        self.assertTrue(ex.exception.args[0].find("Doesn't fit") != -1,
                ex.exception.args[0])

    def test_add_oject_fail(self):
        b = Board(5, 10)
        d = Detail(3, 2, 2)
        d.fill([[[0, 0], [1, 0]], [[1, 0], [1, 1]], [[0, 0], [1, 1]]])
        b.add_object(d, 0, 0)
        with self.assertRaises(Exception) as ex:
            b.add_object(d, 1, 1)
        
        self.assertTrue(ex.exception.args[0].find("Doesn't fit") != -1,
                ex.exception.args[0])

    def test_add_oject_rotate(self):
        b = Board(5, 10)
        d = Detail(3, 2, 2)
        d.fill([[[0, 0], [1, 0]], [[1, 0], [1, 1]], [[0, 0], [1, 1]]])
        d.rotate(1)
        with self.assertRaises(Exception) as ex:
            b.add_object(d, 8, 0)
        self.assertTrue(ex.exception.args[0].find("Doesn't fit") != -1,
                ex.exception.args[0])

    def test_add_oject_rotate_and_chose_side(self):
        b = Board(5, 10)
        d = Detail(3, 2, 2)
        d.fill([[[0, 0], [1, 0]], [[1, 0], [1, 1]], [[0, 0], [1, 1]]])
        d.rotate(1)
        d.chose_side(5)
        b.add_object(d, 1, 0)

        # 0 0 0 0 0
        # 1 1 1 0 0
        # 0 1 0 0 0
        # 0 0 0 0 0
        self._empty_board_5_10[0][1] = 1
        self._empty_board_5_10[0][2] = 1
        self._empty_board_5_10[0][3] = 1
        self._empty_board_5_10[1][1] = 0
        self._empty_board_5_10[1][2] = 1
        self._empty_board_5_10[1][3] = 0

        self.assertListEqual(b.board, self._empty_board_5_10)
        self.assertDictEqual(b.objects, {d: (1, 0)})

    def test_add_oject_on_the_edge(self):
        b = Board(height=3, width=4)
        d = Detail(3, 2, 2)
        d.fill([[[0, 0], [1, 0]], [[1, 0], [1, 1]], [[0, 0], [1, 1]]])
        d.rotate(1)
        d.rotate(1)
        d.chose_side(5)
        b.add_object(d, 0, 0)
        d1 = deepcopy(d)
        d1.rotate(-1)
        b.add_object(d1, 1, 0)
        d2 = Detail(3, 2, 2)
        d2.fill([[[1, 0], [1, 1]], [[0, 0], [1, 0]],
            [[0, 0], [1, 1]]])
        d2.chose_side(5)
        d2.rotate(-1)
        b.add_object(d2, 1, 1)

        _full_board = [[1 for x in range(4)] for y in range(3)]

        self.assertListEqual(b.board, _full_board)
        self.assertDictEqual(b.objects, {d: (0, 0), d1: (1, 0), d2: (1, 1)})
    
    def test_add_oject_rotate_and_chose_wrong_side(self):
        b = Board(5, 10)
        d = Detail(3, 2, 2)
        d.fill([[[0, 0], [1, 0]], [[1, 0], [1, 1]], [[0, 0], [1, 1]]])
        d.rotate(1)
        d.chose_side(4)
        with self.assertRaises(Exception) as ex:
            b.add_object(d, 1, 1)
        
        self.assertTrue(ex.exception.args[0].find("Doesn't fit") != -1,
                ex.exception.args[0])

    def test_get_coordinates(self):
        b = Board(2, 2)
        coordinates = [(x, y) for (x, y) in b.get_coordinates()]
        self.assertListEqual(coordinates, [(0, 0), (0, 1), (1, 0), (1, 1)])

    def test_get_coordinates_after_detail_set(self):
        b = Board(2, 2)
        d = Detail(2, 2, 2)
        d.fill([[[0, 0], [1, 0]], [[1, 0], [1, 1]]])
        d.rotate()
        b.add_object(d, 0, 0)

        coordinates = [(x, y) for (x, y) in b.get_coordinates()]
        self.assertListEqual(coordinates, [(0, 0)])

    def test__generate_matrix_with_detail(self):
        b = Board(5, 10)
        d = Side(3, 2)
        d.fill([[1, 1], [0, 1], [1, 1]])
        matrix = b._generate_matrix_with_detail(d, (4, 2))
        print(matrix)
        self.assertListEqual(
            [
                10 * [0],
                10 * [0],
                4 * [0] + [1, 1] + 4 * [0],
                5 * [0] + [1] + 4 * [0],
                4 * [0] + [1, 1] + 4 * [0]
            ], matrix.value)


