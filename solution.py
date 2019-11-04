from game_logic import GameLogic
from board import Board
from typing import List, Iterator
from tree import TreeElement, generate_children


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


def find_solutions(game_logic: GameLogic) -> Iterator[Board]:
    _elements: List[TreeElement] = []
    _processed: List[TreeElement] = []
    # generate tree
    _tree_element = TreeElement(game_logic, 0)
    _elements.append(_tree_element)

    process_element(_elements, _processed, _tree_element)

    while has_not_processed(_elements):
        _current = get_next_not_processed(_elements)
        process_element(_elements, _processed, _current)

    for element in _processed:
        # if element.game.board.is_complete() and not len(element.game.details):
        #if not len(element.game.details):
        yield element.game.board