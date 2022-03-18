import time
from typing import List


from utils import Coordinates, Vector, clear_screen


class Object:

    def __init__(self, center: Coordinates, span: List[Coordinates], char: str):
        self.center = center
        self.span = span
        self.vector: Vector = Vector(0, 0)
        self.char: str = char

    def move(self):
        self.center.x += self.vector.dx
        self.center.y += self.vector.dy

    def update(self):
        raise NotImplementedError


class WallObject(Object):

    def __init__(self, center: Coordinates, span: List[Coordinates]):
        super().__init__(center, span, "#")

    def update(self):
        pass


class RoadObject(Object):

    def __init__(self, center: Coordinates, span: List[Coordinates], char: str):
        super().__init__(center, span, char)

    def update(self):
        pass


class Board:

    def __init__(self, map_size_x: int, map_size_y: int):
        self.map_size_x = map_size_x
        self.map_size_y = map_size_y
        self.objects: List[Object] = []

    def get_object_at(self, coordinates: Coordinates) -> [Object, None]:
        for obj in self.objects:
            if coordinates in obj.span:
                return obj
        return None


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
            # for obj in self.board.objects:
            #     obj.update()
            #     obj.move()

            clear_screen()
            self.__draw()

            print("\n")
            print(f"Frame rate: {1 / self.frame_rate_sec}")
            print(f"Number of objects: {len(self.board.objects)}")

            time.sleep(self.frame_rate_sec)
