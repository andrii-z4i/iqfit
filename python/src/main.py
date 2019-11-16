from python.src.game_logic import *


class ShapeDataCollector(object):
    def __init__(self):
        self.__name = ""
        self.__side = None
        self.__rotation = None
        self.__coordinates = [-1, -1]
        self.__available_shapes = [
            'RED',
            'GREEN',
            'BLUE',
            'YELLOW',
            'FOXRED',
            'LIGHTBLUE',
            'VIOLET',
            'LIGHTGREEN',
            'DARKBLUE',
            'PINK'
        ]
        self.__shapes_on_board = []

    def ask_for_shape_name(self) -> str:
        while self.__name not in self.__available_shapes:
            print("Choose one of the shapes: " + str(self.__available_shapes))
            self.__name = input().upper()
        return self.__name

    def ask_for_shape_side(self) -> int:
        while self.__side not in [2, 5]:
            print("Choose shape side [allowed only 2 and 5 side]: ")
            try:
                self.__side = int(input())
            except Exception as ex:
                print("Input shape side must be an integer!")
        return self.__side

    def ask_for_shape_coordinates(self) -> tuple:
        while (self.__coordinates[0] not in range(0, 10)) or (self.__coordinates[1] not in range(0, 5)):
            print("Input shape coordinates:")
            print("\tx [0..9]: ")
            try:
                self.__coordinates[0] = int(input())
            except Exception as ex:
                print("Input shape coordinates must be an integer!")
                continue
            print("\ty [0..4]: ")
            try:
                self.__coordinates[1] = int(input())
            except Exception as ex:
                print("Input shape coordinates must be an integer!")
        return tuple(self.__coordinates)


def show_possible_shape_sides(shape: Detail) -> None:
    for side in range(0, 6):
        shape.chose_side(side)
        print(shape)


def main():
    game_logic = GameLogic()

    shape_data_collector = ShapeDataCollector()

    shape_name = shape_data_collector.ask_for_shape_name()
    current_shape = game_logic.get_detail_by_name(shape_name)

    show_possible_shape_sides(current_shape)
    shape_side = shape_data_collector.ask_for_shape_side()
    current_shape.chose_side(shape_side)

    shape_coordinates = shape_data_collector.ask_for_shape_coordinates()
    game_logic.put_detail_on_board(current_shape, shape_coordinates)
    print(game_logic.board)


if __name__ == "__main__":
    main()
