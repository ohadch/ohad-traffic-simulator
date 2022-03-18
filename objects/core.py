from typing import List

from utils import Coordinates, Vector


class Object:

    def __init__(self, position: Coordinates, char: str):
        self.position = position
        self.vector: Vector = Vector(0, 0)
        self.char: str = char

    def speed(self):
        return self.vector.speed()

    def stop(self):
        self.vector.stop()

    def update(self):
        self._update_vector()
        self.position.update(self.vector)

    def _update_vector(self) -> Vector:
        return Vector(0, 0)


class ObjectsGroup:

    def __init__(self, objects: List[Object]):
        self.objects = objects

