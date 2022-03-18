import time
from typing import List

from board import Board
from objects import WallObject, RoadObject, CarObject
from utils import Coordinates, clear_screen


class Game:

    def __init__(self, board: Board, frame_rate_sec: float):
        self.frame_rate_sec = frame_rate_sec
        self.board = board
        self.static_classes = [WallObject, RoadObject]

        self.__create_initial_objects()

    def __create_initial_objects(self):
        self.roads: List[RoadObject] = self.__create_roads()

        self.board.objects.extend(self.__create_borders())
        self.board.objects.extend(self.roads)
        self.board.objects.extend(self.__create_cars())

    def __create_borders(self) -> List[WallObject]:
        upper_wall = WallObject(Coordinates(0, 0), [Coordinates(0, x) for x in range(self.board.map_size_y)])
        lower_wall = WallObject(Coordinates(self.board.map_size_y - 1, 0), [Coordinates(self.board.map_size_y - 1, x) for x in range(self.board.map_size_y)])
        left_wall = WallObject(Coordinates(0, 0), [Coordinates(x, 0) for x in range(self.board.map_size_x)])
        right_wall = WallObject(Coordinates(0, self.board.map_size_x - 1), [Coordinates(x, self.board.map_size_x - 1) for x in range(self.board.map_size_x)])

        return [upper_wall, lower_wall, left_wall, right_wall]

    def __create_roads(self) -> List[RoadObject]:
        center_horizontal_road = RoadObject(Coordinates(self.board.map_size_y // 2, 0), [Coordinates(x, self.board.map_size_y // 2) for x in range(1, self.board.map_size_x - 1)], "*")
        center_vertical_road = RoadObject(Coordinates(0, self.board.map_size_x // 2), [Coordinates(self.board.map_size_y // 2, x) for x in range(1, self.board.map_size_y - 1)], "*")

        return [center_horizontal_road, center_vertical_road]

    def __create_cars(self):
        return [
            CarObject(self.roads[0].span[0], "red"),
        ]

    def __draw(self):
        for x in range(self.board.map_size_x):
            for y in range(self.board.map_size_y):
                obj = self.board.get_object_at(Coordinates(x, y))
                if obj is None:
                    print(" ", end=" ")
                else:
                    print(obj.char, end=" ")
            print()

    def __print_meta(self):
        print("Map size: {}x{}".format(self.board.map_size_x, self.board.map_size_y))
        print("Frame rate: {}s".format(self.frame_rate_sec))

    def run(self):
        while True:
            for obj in self.board.objects:
                if any([isinstance(obj, cls) for cls in self.static_classes]):
                    continue

                obj.update()

            clear_screen()
            self.__draw()

            print("\n")
            self.__print_meta()

            time.sleep(self.frame_rate_sec)
