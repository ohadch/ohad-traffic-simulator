from typing import List

from objects.core import Object, ObjectsGroup
from utils import Coordinates, Direction

ASCII_ARROW_UP = '\u2191'
ASCII_ARROW_DOWN = '\u2193'
ASCII_ARROW_LEFT = '\u2190'
ASCII_ARROW_RIGHT = '\u2192'


class RoadObject(Object):

    def __init__(self, center: Coordinates, direction: Direction):
        self.direction = direction
        super().__init__(center, self.__get_char())

    def __get_char(self) -> str:
        return {
            Direction.UP: ASCII_ARROW_UP,
            Direction.DOWN: ASCII_ARROW_DOWN,
            Direction.LEFT: ASCII_ARROW_LEFT,
            Direction.RIGHT: ASCII_ARROW_RIGHT
        }[self.direction]

    def _update_vector(self) -> Coordinates:
        return self.position


class RoadObjectsGroup(ObjectsGroup):

    def __init__(self, objects: List[RoadObject]):
        super().__init__(objects)

    @property
    def start(self) -> RoadObject:
        return self.objects[0]

    @property
    def end(self) -> RoadObject:
        return self.objects[-1]
