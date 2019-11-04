from src.models import Detail
from src.game_logic import GameLogic
from copy import deepcopy
from typing import List, Iterator, Tuple
from uuid import uuid1


'''
Should be

root
- detail a - possible position
    - detail b - possible position
        - detail c - possible position
        - detail c - possible position
        - detail c - possible position
    - detail b - possible position
    - detail b - possible position
    - detail b - possible position
- detail a - possible combination
- detail a - possible combination
- detail a - possible combination

'''


class TreeElement(object):

    def __init__(self, game: GameLogic, parent: int):
        self._game = game
        self._parent = parent
        self._id = uuid1().int
        self._visited = False

    @property
    def game(self):
        return self._game

    @property
    def id(self):
        return self._id

    @property
    def parent(self):
        return self._parent

    @property
    def visited(self):
        return self._visited

    def mark_as_visited(self):
        self._visited = True

    def try_to_put_detail(self, detail: Detail) -> Iterator[GameLogic]:
        for coordinates in self._game.board.get_coordinates():
            for side in detail.sides:
                detail.chose_side(side)
                for i in range(4):
                    detail.rotate()
                    try:
                        _game = deepcopy(self._game)
                        _game.put_detail_on_board(detail, coordinates)
                        yield _game
                    except Exception as ex:
                        continue
                        # print('Can\'t put detail on board')


def generate_children(element: TreeElement) -> Iterator[TreeElement]:
    if not len(element.game.details):
        return

    for _game_logic in element.try_to_put_detail(element.game.first_detail):
        _element = TreeElement(_game_logic, element.id)
        yield _element
