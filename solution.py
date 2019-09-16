import threading
from game_logic import GameLogic
from board import Board
from typing import Generator, List
from tree import TreeElement, generate_children



def find_solutions2(game_logic: GameLogic) -> Generator[Board, Board, None]:
    _map = dict()
    for detail in game_logic.details:
        _map[detail.name] = []
        for (current_state_of_detail, coordinates) in try_to_put_detail(detail, game_logic.board):
            _map[detail.name].append((current_state_of_detail, coordinates))
        print("Detail '%s' -> positions -> %d" % (detail.name, len(_map[detail.name])))

    params = [_map[detail_name] for detail_name in _map]

    s = SolutionChecker('S1', game_logic, params)
    for solution in s.run():
        yield solution


def get_next_not_processed(elements: List[TreeElement]) -> TreeElement:
    _filter = filter(lambda e: e.visited == False, elements)
    return _filter.__next__()


def has_not_processed(elements: List[TreeElement]) -> bool:
    try:
        _next = get_next_not_processed(elements)
        return _next is not None
    except StopIteration:
        return False


def process_element(_elements, _processed, _tree_element):
    for _child in generate_children(_tree_element):
        _elements.append(_child)
    _tree_element.mark_as_visited()
    _processed.append(_tree_element)
    _elements.remove(_tree_element)


def find_solutions3(game_logic: GameLogic) -> Generator[Board, Board, None]:
    _elements: List[TreeElement] = []
    _processed: List[TreeElement] = []
    # generate tree
    _tree_element = TreeElement(game_logic, 0)
    _elements.append(_tree_element)

    process_element(_elements, _processed, _tree_element)

    while has_not_processed(_elements):
        _current = get_next_not_processed(_elements)
        process_element(_elements, _processed, _current)

    print(len(_processed))


class SolutionChecker(threading.Thread):

    def __init__(self, name_of_thread: str, game_logic: GameLogic, _combinations: List):
        threading.Thread.__init__(self)
        self._name_of_thread = name_of_thread
        self._game_logic = game_logic
        self._combinations = _combinations

    def run(self) -> Generator[Board, None, None]:
        for _combination in product(*self._combinations):
            _copy_of_game_logic = deepcopy(self._game_logic)
            i = 0
            for (_detail, _coordinates) in _combination:
                try:
                    _copy_of_game_logic.put_detail_on_board(_detail, _coordinates)
                    i += 1
                except Exception:
                    break

            if _copy_of_game_logic.board.is_complete():
                yield _copy_of_game_logic.board