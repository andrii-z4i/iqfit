from unittest import TestCase
from game_logic import GameLogic


class GameLogicTest(TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_game_logic_init(self):
        g = GameLogic()
        self.assertEqual(len(g.details), 9)
        g.put_detail_on_board('VIOLET', (0, 0))
        self.assertEqual(len(g.details), 8)
