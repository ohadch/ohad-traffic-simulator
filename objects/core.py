from typing import List

from utils import Coordinates


class Object:

    def __init__(self, position: Coordinates, char: str):
        self.position = position
        self.char: str = char

    def update(self):
        """
        Update the object's position.
        """
        raise NotImplementedError


class ObjectsGroup:

    def __init__(self, objects: List[Object]):
        self.objects = objects

