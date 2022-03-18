from typing import List

from objects import Object
from utils import Coordinates


class Board:

    def __init__(self, map_size_x: int, map_size_y: int):
        self.map_size_x = map_size_x
        self.map_size_y = map_size_y
        self.objects: List[Object] = []

    def get_object_at(self, coordinates: Coordinates) -> [Object, None]:
        for obj in self.objects[::-1]:
            if coordinates in obj.span:
                return obj
        return None

