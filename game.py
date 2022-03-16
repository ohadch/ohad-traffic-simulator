import os
import random
import time
from enum import Enum
from typing import List


class Direction(Enum):
    """
    Enum for the four directions
    """
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class Vector:

    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols

    def stop(self):
        self.rows = 0
        self.cols = 0

    def set_by_speed_and_direction(self, speed: int, direction: Direction):
        if direction == Direction.UP:
            self.rows = -speed
        elif direction == Direction.DOWN:
            self.rows = speed
        elif direction == Direction.LEFT:
            self.cols = -speed
        elif direction == Direction.RIGHT:
            self.cols = speed
        else:
            raise ValueError("Invalid direction")

    def __str__(self):
        return f"Vector({self.rows}, {self.cols})"

    def get_direction(self) -> [Direction, None]:
        if self.rows == 0 and self.cols > 0:
            return Direction.RIGHT
        elif self.rows == 0 and self.cols < 0:
            return Direction.LEFT
        elif self.rows > 0 and self.cols == 0:
            return Direction.DOWN
        elif self.rows < 0 and self.cols == 0:
            return Direction.UP
        elif self.rows == 0 and self.cols == 0:
            return None
        else:
            raise ValueError(f"Invalid vector: {self}")


class Coordinates:

    def __init__(self, row: int, column: int):
        self.row = row
        self.column = column

    def __eq__(self, other):
        return self.row == other.row and self.column == other.column

    def __str__(self):
        return f"({self.row}, {self.column})"

    def get_next_by_direction(self, direction: Direction, num_steps: int = 1) -> "Coordinates":
        """
        Returns the next coordinates in the given direction
        """
        if direction == Direction.UP:
            return Coordinates(self.row - num_steps, self.column)
        elif direction == Direction.DOWN:
            return Coordinates(self.row + num_steps, self.column)
        elif direction == Direction.LEFT:
            return Coordinates(self.row, self.column - num_steps)
        elif direction == Direction.RIGHT:
            return Coordinates(self.row, self.column + num_steps)
        elif direction is None:
            return self
        else:
            raise ValueError(f"Direction not supported: {direction}")


class Object:

    def __init__(self, coordinates: Coordinates, vector: Vector):
        self.coordinates = coordinates
        self.vector = vector

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

    def update(self):
        obj_at_coordinate = self.board.get_object_at(self.coordinates)
        if obj_at_coordinate is not None:
            self.vector.stop()
        else:
            self.board.objects.append(RoadObject(self.coordinates))

        direction = self.vector.get_direction()

        while True:
            if direction == Direction.UP:
                new_direction = random.choice([Direction.LEFT, Direction.RIGHT, Direction.UP])
            elif direction == Direction.DOWN:
                new_direction = random.choice([Direction.LEFT, Direction.RIGHT, Direction.DOWN])
            elif direction == Direction.LEFT:
                new_direction = random.choice([Direction.UP, Direction.DOWN, Direction.LEFT])
            elif direction == Direction.RIGHT:
                new_direction = random.choice([Direction.UP, Direction.DOWN, Direction.RIGHT])
            elif direction is None:
                continue
            else:
                raise ValueError("Direction not supported")

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
        self.spawn_roads_creator_player()

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

            self.clear_screen()
            self.board.draw()

            print("\n")
            print(f"Frame rate: {1 / self.frame_rate_sec}")
            print(f"Number of objects: {len(self.board.objects)}")
            for obj in self.board.objects:
                print(f"Object: {obj.__class__.__name__}: {obj.coordinates}")

            time.sleep(self.frame_rate_sec)
