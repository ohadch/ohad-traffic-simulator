import time
from typing import List

from board import Board
from objects.car import CarObject
from objects.core import ObjectsGroup, Object
from objects.road import RoadObject, RoadObjectsGroup
from objects.wall import WallObject
from utils import Coordinates, clear_screen, Direction


class Game:

    def __init__(self, board: Board, frame_rate_sec: float):
        self.frame_rate_sec = frame_rate_sec
        self.board = board
        self.static_classes = [WallObject, RoadObject]

        self.__create_initial_objects()

    def __create_initial_objects(self):
        self.board.single_objects.extend(self.__create_borders())
        self.board.objectGroups.extend(self.__create_roads())
        self.board.single_objects.extend(self.__create_cars())

    def __create_borders(self) -> List[Object]:
        upper_wall = [
            WallObject(Coordinates(x, 0)) for x in range(self.board.map_size_x)
        ]

        lower_wall = [
            WallObject(Coordinates(x, self.board.map_size_y - 1)) for x in range(self.board.map_size_x)
        ]

        left_wall = [
            WallObject(Coordinates(0, y)) for y in range(self.board.map_size_y)
        ]

        right_wall = [
            WallObject(Coordinates(self.board.map_size_x - 1, y)) for y in range(self.board.map_size_y)
        ]

        return [*upper_wall, *lower_wall, *left_wall, *right_wall]

    def __create_roads(self) -> List[ObjectsGroup]:
        center_horizontal_road = RoadObjectsGroup([
            RoadObject(Coordinates(x, self.board.map_size_y // 2), Direction.RIGHT) for x in range(1, self.board.map_size_x - 1)
        ])

        return [center_horizontal_road]

    def __create_cars(self):
        roads = [group for group in self.board.objectGroups if isinstance(group, RoadObjectsGroup)]
        return [
            CarObject(roads[0].start.position.clone(), "red"),
        ]

    def __draw(self):
        for y in range(self.board.map_size_y):
            for x in range(self.board.map_size_x):
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
            for obj in self.board.all_objects:
                if any([isinstance(obj, cls) for cls in self.static_classes]):
                    continue

                obj.update()

            clear_screen()
            self.__draw()

            print("\n")
            self.__print_meta()

            time.sleep(self.frame_rate_sec)
