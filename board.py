from functools import reduce
from typing import List

from objects.core import Object, ObjectsGroup
from utils import Coordinates


class Board:

    def __init__(self, map_size_x: int, map_size_y: int):
        self.map_size_x = map_size_x
        self.map_size_y = map_size_y
        self.single_objects: List[Object] = []
        self.object_groups: List[ObjectsGroup] = []

    @property
    def all_objects(self):
        """
        Returns all objects on the board, whether they are single or belonging to a group.
        @return: All objects on the board.
        """
        return [
            *reduce(lambda x, y: x + y, [foo.objects for foo in self.object_groups]),
            *[foo for foo in self.single_objects],
        ]

    def get_object_at(self, coordinates: Coordinates) -> [Object, None]:
        """
        Returns the object at the given coordinates.
        @param coordinates: The coordinates of the object.
        @return: The object at the given coordinates or None if there is no object at the given coordinates.
        """
        for obj in self.all_objects[::-1]:
            if coordinates == obj.position:
                return obj
        return None

