from unittest import TestCase
from game_logic import GameLogic
from solution import find_solutions


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

    def test_find_solutions(self):
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
        g.put_detail_on_board(detail, (1, 0))
        detail = g.get_detail_by_name('BLUE')
        detail.rotate()
        g.put_detail_on_board(detail, (1, 1))
        detail = g.get_detail_by_name('LIGHTBLUE')
        detail.chose_side(5)
        detail.rotate()
        g.put_detail_on_board(detail, (4, 0))
        detail = g.get_detail_by_name('PINK')
        detail.rotate(-1)
        g.put_detail_on_board(detail, (0, 3))
        detail = g.get_detail_by_name('FOXRED')
        detail.chose_side(5)
        detail.rotate(-1)
        g.put_detail_on_board(detail, (2, 3))
        detail = g.get_detail_by_name('RED')
        detail.chose_side(5)
        detail.rotate(-1)
        g.put_detail_on_board(detail, (6, 3))
        print('')
        print(g.board)
        self.assertEqual(len(g.details), 3)
        # self.assertEqual(len(g.details), 4)

        for solution in find_solutions(g):
            print(solution)

    # def test_solution_3(self):
    #      g = GameLogic()
    #      find_solutions3(g)


    # def test_find_all_solutions(self):
    #     g = GameLogic()
    #     self.assertEqual(len(g.details), 10)
    #     for solution in find_solutions2(g):
    #         print(solution)

