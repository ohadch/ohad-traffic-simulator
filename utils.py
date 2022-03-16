from enum import Enum


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

    def speed(self):
        return abs(self.rows) + abs(self.cols)

    def stop(self):
        self.rows = 0
        self.cols = 0

    def set_by_speed_and_direction(self, speed: int, direction: Direction):
        if direction == Direction.UP:
            self.rows = -speed
            self.cols = 0
        elif direction == Direction.DOWN:
            self.rows = speed
            self.cols = 0
        elif direction == Direction.LEFT:
            self.rows = 0
            self.cols = -speed
        elif direction == Direction.RIGHT:
            self.rows = 0
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

    def clone(self) -> "Coordinates":
        return Coordinates(self.row, self.column)

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
