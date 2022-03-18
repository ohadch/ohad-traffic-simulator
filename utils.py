import os
from dataclasses import dataclass


class Vector:

    def __init__(self, dy: int, dx: int):
        self.dy = dy
        self.dx = dx

    def speed(self):
        return abs(self.dy) + abs(self.dx)

    def stop(self):
        self.dy = 0
        self.dx = 0

    def __str__(self):
        return f"Vector({self.dy}, {self.dx})"


class Coordinates:

    def __init__(self, y: int, x: int):
        self.y = y
        self.x = x

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

    def __str__(self):
        return f"Coordinates({self.y}, {self.x})"

    def update(self, vector: Vector):
        self.y += vector.dy
        self.x += vector.dx

    def clone(self) -> "Coordinates":
        return Coordinates(self.y, self.x)


@dataclass
class Move:
    origin: Coordinates
    destination: Coordinates


def clear_screen():
    """
    Clears the screen
    """
    os.system('cls' if os.name == 'nt' else 'clear')