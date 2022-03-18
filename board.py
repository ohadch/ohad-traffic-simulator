from functools import reduce
from typing import List

from objects.core import Object, ObjectsGroup
from utils import Coordinates


class Board:

    def __init__(self, map_size_x: int, map_size_y: int):
        self.map_size_x = map_size_x
        self.map_size_y = map_size_y
        self.single_objects: List[Object] = []
        self.objectGroups: List[ObjectsGroup] = []

    @property
    def all_objects(self):
        return [
            *reduce(lambda x, y: x + y, [foo.objects for foo in self.objectGroups]),
            *[foo for foo in self.single_objects],
        ]

    def get_object_at(self, coordinates: Coordinates) -> [Object, None]:
        for obj in self.all_objects[::-1]:
            if coordinates == obj.position:
                return obj
        return None

