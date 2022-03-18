import os
from enum import Enum


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


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


def clear_screen():
    """
    Clears the screen
    """
    os.system('cls' if os.name == 'nt' else 'clear')