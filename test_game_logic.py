from unittest import TestCase
from game_logic import GameLogic, find_solutions 


class GameLogicTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_game_logic_init(self):
        g = GameLogic()
        self.assertEqual(len(g.details), 10)
        detail = g.get_detail_by_name('VIOLET')
        g.put_detail_on_board(detail, (0, 0))
        self.assertEqual(len(g.details), 9)

    def _test_find_solutions(self):
        g = GameLogic()
        self.assertEqual(len(g.details), 10)
        detail = g.get_detail_by_name('GREEN')
        detail.chose_side(5)
        detail.rotate()
        detail.rotate()
        g.put_detail_on_board(detail, (0, 0))
        detail = g.get_detail_by_name('VIOLET')
        detail.chose_side(5)
        detail.rotate()
        g.put_detail_on_board(detail, (0, 1))
        detail = g.get_detail_by_name('BLUE')
        detail.rotate()
        g.put_detail_on_board(detail, (1, 1))
        print('')
        print(g.board)
        self.assertEqual(len(g.details), 7)
        for solution in find_solutions(g, 0):
            print(solution)
