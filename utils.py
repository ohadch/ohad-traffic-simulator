import os


class Vector:

    def __init__(self, dx: int, dy: int):
        self.dx = dx
        self.dy = dy

    def speed(self):
        return abs(self.dx) + abs(self.dy)

    def stop(self):
        self.dy = 0
        self.dx = 0

    def __str__(self):
        return f"Vector({self.dx}, {self.dy})"


class Coordinates:

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def __eq__(self, other):
        return self.y == other.y and self.x == other.x

    def __str__(self):
        return f"Coordinates({self.x}, {self.y})"

    def update(self, vector: Vector):
        self.x += vector.dx
        self.y += vector.dy

    def clone(self) -> "Coordinates":
        return Coordinates(self.x, self.y)


def clear_screen():
    """
    Clears the screen
    """
    os.system('cls' if os.name == 'nt' else 'clear')