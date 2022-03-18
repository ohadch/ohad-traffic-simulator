import os
import random
from enum import Enum
from typing import List


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    UP_LEFT = "UP_LEFT"
    UP_RIGHT = "UP_RIGHT"
    DOWN_LEFT = "DOWN_LEFT"
    DOWN_RIGHT = "DOWN_RIGHT"


class Coordinates:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

    def __str__(self):
        return f"Coordinates({self.x}, {self.y})"

    def clone(self) -> "Coordinates":
        return Coordinates(self.x, self.y)

    def get_direction_to(self, other: "Coordinates") -> Direction:
        """
        Returns the direction to the other coordinate
        :param other: The other coordinate
        :return: The direction to the other coordinate
        """
        if self.x == other.x:
            if self.y < other.y:
                return Direction.DOWN
            else:
                return Direction.UP
        elif self.y == other.y:
            if self.x < other.x:
                return Direction.RIGHT
            else:
                return Direction.LEFT
        elif self.x < other.x and self.y < other.y:
            return Direction.DOWN_RIGHT
        elif self.x < other.x and self.y > other.y:
            return Direction.UP_RIGHT
        elif self.x > other.x and self.y < other.y:
            return Direction.DOWN_LEFT
        elif self.x > other.x and self.y > other.y:
            return Direction.UP_LEFT
        else:
            raise Exception("This should never happen")

    def get_path_to(self, other: "Coordinates") -> List["Coordinates"]:
        """
        Returns a list of coordinates from self to other
        :param other: The other coordinate
        :return: The list of coordinates from self to other
        """
        full_path: List[Coordinates] = [
            self.clone()
        ]

        while full_path[-1] != other:
            last_coordinate = full_path[-1]

            if last_coordinate.x < other.x:
                full_path.append(Coordinates(last_coordinate.x + 1, last_coordinate.y))
            elif last_coordinate.x > other.x:
                full_path.append(Coordinates(last_coordinate.x - 1, last_coordinate.y))
            elif last_coordinate.y < other.y:
                full_path.append(Coordinates(last_coordinate.x, last_coordinate.y + 1))
            elif last_coordinate.y > other.y:
                full_path.append(Coordinates(last_coordinate.x, last_coordinate.y - 1))
            else:
                raise Exception("This should never happen")

        return full_path


def clear_screen():
    """
    Clears the screen
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def get_random_color_name() -> str:
    """
    Returns a random color name
    """
    return random.choice([
        'red',
        'green',
        'yellow',
        'blue',
        'magenta',
        'cyan',
    ])
