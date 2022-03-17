import os
import random
import time
from typing import List

from utils import Coordinates, Vector, Direction


class Object:

    def __init__(self, coordinates: Coordinates, vector: Vector):
        self.coordinates = coordinates
        self.vector = vector

    def move(self):
        self.coordinates.column += self.vector.cols
        self.coordinates.row += self.vector.rows

    def can_advance_in_direction(self, direction: Direction, board: "Board") -> bool:
        next_coordinates = self.coordinates.get_next_by_direction(direction, self.vector.speed())

        if next_coordinates.row < 0 or next_coordinates.row >= board.num_rows:
            return False

        if next_coordinates.column < 0 or next_coordinates.column >= board.num_cols:
            return False

        if board.get_object_at(next_coordinates) is not None:
            return False

        return True

    def __str__(self):
        raise NotImplementedError

    def update(self):
        raise NotImplementedError


class Board:

    def __init__(self, num_rows: int, num_cols: int, objects: List[Object]):
        self.num_rows = num_rows
        self.num_cols = num_cols
        self.objects = objects

    def get_object_at(self, coordinates: Coordinates) -> [Object, None]:
        for obj in self.objects:
            if obj.coordinates == coordinates:
                return obj

    def draw(self) -> None:
        """
        Draws the board.
        """
        border_str = "+"

        print(" ".join(list(border_str * (self.num_cols + 2))))

        for row_idx in range(self.num_rows):
            row_strs_list = []

            for col_idx in range(self.num_cols):
                obj = self.get_object_at(Coordinates(row_idx, col_idx))
                if obj is None:
                    row_strs_list.append(" ")
                else:
                    row_strs_list.append(str(obj))

            print(" ".join([border_str, *row_strs_list, border_str]))

        print(" ".join(list(border_str * (self.num_cols + 2))))


class RoadsCreatorPlayerObject(Object):

    def __init__(self, coordinates: Coordinates, board: Board):
        Object.__init__(self, coordinates, Vector(0, 0))
        self.board = board
        self.speed = 1

    def get_possible_directions(self) -> List[Direction]:
        possible_directions: List[Direction] = []

        if self.can_advance_in_direction(Direction.UP, self.board):
            possible_directions.append(Direction.UP)
        if self.can_advance_in_direction(Direction.DOWN, self.board):
            possible_directions.append(Direction.DOWN)
        if self.can_advance_in_direction(Direction.LEFT, self.board):
            possible_directions.append(Direction.LEFT)
        if self.can_advance_in_direction(Direction.RIGHT, self.board):
            possible_directions.append(Direction.RIGHT)

        return possible_directions

    def update(self):
        direction = self.vector.get_direction()
        possible_directions = self.get_possible_directions()

        if direction == Direction.UP:
            directions_pool = [Direction.LEFT, Direction.RIGHT, Direction.UP]
        elif direction == Direction.DOWN:
            directions_pool = [Direction.LEFT, Direction.RIGHT, Direction.DOWN]
        elif direction == Direction.LEFT:
            directions_pool = [Direction.UP, Direction.DOWN, Direction.LEFT]
        elif direction == Direction.RIGHT:
            directions_pool = [Direction.UP, Direction.DOWN, Direction.RIGHT]
        elif direction is None:
            return
        else:
            raise ValueError("Direction not supported")

        filtered_directions_pool = [foo for foo in directions_pool if foo in possible_directions]
        if len(filtered_directions_pool) == 0:
            self.vector.stop()
            return

        new_direction = random.choice(filtered_directions_pool)
        next_coordinates = self.coordinates.get_next_by_direction(new_direction, self.speed)
        obj_at_coordinate = self.board.get_object_at(next_coordinates)

        if obj_at_coordinate is not None:
            self.vector.stop()
        else:
            self.board.objects.append(RoadObject(self.coordinates.clone()))

        self.vector.set_by_speed_and_direction(self.speed, new_direction)

    def __str__(self):
        return "C"


class RoadObject(Object):
    def __init__(self, coordinates: Coordinates):
        Object.__init__(self, coordinates, Vector(0, 0))

    def update(self):
        pass

    def __str__(self):
        return 'R'


class Game:

    def __init__(self, board: Board, frame_rate_sec: float):
        self.frame_rate_sec = frame_rate_sec
        self.board = board
        self.draw_roads()

    def draw_roads(self):
        row = self.board.num_rows // 2

        for col in range(self.board.num_cols):
            self.board.objects.append(RoadObject(Coordinates(row, col)))

    def spawn_roads_creator_player(self):
        should_start_from_row = random.choice([True, False])

        if should_start_from_row:
            start_coordinates: Coordinates = Coordinates(
                row=random.choice([0, self.board.num_rows - 1]),
                column=random.randint(0, self.board.num_cols - 1)
            )

            if start_coordinates.row == 0:
                direction = Direction.DOWN
            else:
                direction = Direction.UP
        else:
            start_coordinates: Coordinates = Coordinates(
                row=random.randint(0, self.board.num_rows - 1),
                column=random.choice([0, self.board.num_cols - 1])
            )

            if start_coordinates.column == 0:
                direction = Direction.RIGHT
            else:
                direction = Direction.LEFT

        creator_object = RoadsCreatorPlayerObject(start_coordinates, self.board)
        creator_object.vector.set_by_speed_and_direction(1, direction)

        self.board.objects.append(creator_object)

    def clear_screen(self):
        os.system('cls' if os.name == 'nt' else 'clear')

    def run(self):
        while True:
            for obj in self.board.objects:
                obj.update()
                obj.move()

            self.clear_screen()
            self.board.draw()

            print("\n")
            print(f"Frame rate: {1 / self.frame_rate_sec}")
            print(f"Number of objects: {len(self.board.objects)}")

            time.sleep(self.frame_rate_sec)
