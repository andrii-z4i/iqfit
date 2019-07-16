from unittest import TestCase
from models import Side, Detail

class ModelsTest(TestCase):

    def test_fill_wrong_data(self):
        a = Side(2, 3)

        self.assertEqual(a.height, 2)
        self.assertEqual(a.width, 3)
        
        with self.assertRaises(Exception) as ex:
            a.fill([[1, 0, 3], [1, 1, 1]])
        
        self.assertTrue(ex.exception.args[0].find("Wrong data") != -1,
                ex.exception.args[0])

    def test_fill_ok(self):
        a = Side(2, 3)
        self.assertEqual(a.height, 2)
        self.assertEqual(a.width, 3)
        a.fill([[1, 0, 0], [1, 1, 1]])
        self.assertListEqual(a.value, [[1, 0, 0], [1, 1, 1]])

    def test__rotate_left(self):
        a = Side(2, 3)
        a.fill([[1, 0, 0], [1, 1, 1]])
        a.rotate()
        self.assertListEqual(a.value, [[0, 1], [0, 1], [1, 1]])

    def test__rotate_right(self):
        a = Side(2, 3)
        a.fill([[1, 0, 0], [1, 1, 1]])
        a.rotate(direction=-1)
        self.assertListEqual(a.value, [[1, 1], [1, 0], [1, 0]])

    def test_detail_fill(self):
        a = Detail(4, 2, 2)
        self.assertEqual(a.height, 4)
        self.assertEqual(a.width, 2)
        self.assertEqual(a.depth, 2)
        self.assertListEqual(a.value, [[[0, 0], [0, 0]], [[0, 0], [0, 0]], [[0,
            0], [0, 0]], [[0, 0], [0, 0]]])
    
    def test_detail_fill_copy(self):
        a = Detail(4, 2, 2)
        a.fill([[[0, 1], [0, 1]], [[0, 1], [0, 1]], [[0,
            1], [0, 1]], [[0, 1], [0, 1]]])
        self.assertListEqual(a.value, [[[0, 1], [0, 1]], [[0, 1], [0, 1]], [[0,
            1], [0, 1]], [[0, 1], [0, 1]]])

    def test_detail_side(self):
        a = Detail(4, 2, 2)
        a.fill([[[1, 1], [0, 0]], [[1, 1], [1, 0]], [[1, 0], [0, 0]], [[1, 0], [0, 0]]])
        a.rotate(1)
        a.rotate(1)
        a.rotate(1)
        a.rotate(1)
        a.chose_side(3)
        self.assertListEqual(a.get_side(0).value, [[1, 1], [0, 0]])
        self.assertListEqual(a.get_side(1).value, [[0, 0], [1, 0]])
        self.assertListEqual(a.get_side(2).value, [[0, 0], [1, 0], [0, 0], [0, 0]])
        self.assertListEqual(a.get_side(3).value, [[0, 1], [0, 1], [0, 0], [0, 0]])
        self.assertListEqual(a.get_side(4).value, [[1, 1], [1, 1], [0, 1], [0, 1]])
        self.assertListEqual(a.get_side(5).value, [[1, 0], [1, 1], [1, 0], [1, 0]])
        a.rotate(-1)
        a.rotate(-1)
        a.rotate(-1)
        a.rotate(-1)
        a.rotate(-1)
        self.assertListEqual(a.get_current_side().value, [[0, 0, 0, 0], [0, 0, 1, 1]])
