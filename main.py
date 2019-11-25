from python.src.models import Detail
from python.src.game_logic import GameLogic


class ShapeDataCollector(object):
    def __init__(self):
        self.__name = ""
        self.__coordinates = [-1, -1]
        self.__side = None
        self.__rotation = None
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
        # this class member is planned for future method "remove_detail_from_board"
        self.__shapes_on_board = []

    def ask_for_shape_name(self) -> str:
        self.__name = ""
        while self.__name not in self.__available_shapes:
            print("Choose one of the shapes: " + str(self.__available_shapes))
            self.__name = input().upper()
        return self.__name

    def ask_for_shape_side(self) -> int:
        self.__side = None
        while self.__side not in [2, 5]:
            print("Choose shape side [allowed only 2 and 5 side]: ")
            try:
                self.__side = int(input())
            except Exception as ex:
                print("Input shape side must be an integer!")
        return self.__side

    def ask_for_shape_coordinates(self) -> tuple:
        self.__coordinates = [-1, -1]
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

    def ask_for_shape_rotation(self) -> int:
        self.__rotation = None
        while self.__rotation not in [-1, 1]:
            print("Choose shape rotation [\"-1\" -- left rotation, \"1\" -- right rotation]: ")
            try:
                self.__rotation = int(input())
            except Exception as ex:
                print("Input shape side must be an integer!")
        return self.__rotation

    def add_current_shape_on_board(self) -> None:
        self.__shapes_on_board.append(self.__name)
        self.__available_shapes.remove(self.__name)


def show_possible_shape_sides(shape: Detail) -> None:
    for side in range(0, 6):
        shape.chose_side(side)
        print(shape)


def main():
    game_logic = GameLogic()
    shape_data_collector = ShapeDataCollector()
    print(str(game_logic.board))
    while "-" in str(game_logic.board):
        shape_name = shape_data_collector.ask_for_shape_name()
        current_shape = game_logic.get_detail_by_name(shape_name)

        show_possible_shape_sides(current_shape)
        shape_side = shape_data_collector.ask_for_shape_side()
        current_shape.chose_side(shape_side)

        while True:
            print("Do you need to rotate shape? For canceling type \"NO\"")
            if input().upper() == "NO":
                break
            shape_rotation = shape_data_collector.ask_for_shape_rotation()
            current_shape.rotate(shape_rotation)
            print(current_shape)

        shape_coordinates = shape_data_collector.ask_for_shape_coordinates()
        try:
            game_logic.put_detail_on_board(current_shape, shape_coordinates)
            shape_data_collector.add_current_shape_on_board()
        except Exception as ex:
            print(ex)
        print(game_logic.board)


if __name__ == "__main__":
    main()
