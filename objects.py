from typing import List

from utils import Coordinates, Vector


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
