import time

from board import Board
from objects import WallObject, RoadObject
from utils import Coordinates, clear_screen


class Game:

    def __init__(self, board: Board, frame_rate_sec: float):
        self.frame_rate_sec = frame_rate_sec
        self.board = board

        self.__create_initial_objects()

    def __create_initial_objects(self):
        self.board.objects.extend(self.__create_borders())
        self.board.objects.extend(self.__create_roads())

    def __create_borders(self):
        upper_wall = WallObject(Coordinates(0, 0), [Coordinates(0, x) for x in range(self.board.map_size_y)])
        lower_wall = WallObject(Coordinates(self.board.map_size_y - 1, 0), [Coordinates(self.board.map_size_y - 1, x) for x in range(self.board.map_size_y)])
        left_wall = WallObject(Coordinates(0, 0), [Coordinates(x, 0) for x in range(self.board.map_size_x)])
        right_wall = WallObject(Coordinates(0, self.board.map_size_x - 1), [Coordinates(x, self.board.map_size_x - 1) for x in range(self.board.map_size_x)])

        return [upper_wall, lower_wall, left_wall, right_wall]

    def __create_roads(self):
        center_horizontal_road = RoadObject(Coordinates(self.board.map_size_y // 2, 0), [Coordinates(x, self.board.map_size_y // 2) for x in range(self.board.map_size_x)], "*")
        center_vertical_road = RoadObject(Coordinates(0, self.board.map_size_x // 2), [Coordinates(self.board.map_size_y // 2, x) for x in range(self.board.map_size_y)], "*")

        return [center_horizontal_road, center_vertical_road]

    def __draw(self):
        for x in range(self.board.map_size_x):
            for y in range(self.board.map_size_y):
                obj = self.board.get_object_at(Coordinates(x, y))
                if obj is None:
                    print(" ", end=" ")
                else:
                    print(obj.char, end=" ")
            print()

    def run(self):
        while True:
            for obj in self.board.objects:
                obj.update()

            clear_screen()
            self.__draw()

            print("\n")
            print(f"Frame rate: {1 / self.frame_rate_sec}")
            print(f"Number of objects: {len(self.board.objects)}")

            time.sleep(self.frame_rate_sec)
