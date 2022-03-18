from typing import List

from objects.core import Object, ObjectsGroup
from utils import Coordinates, Direction

ASCII_ARROW_UP = '\u2191'
ASCII_ARROW_DOWN = '\u2193'
ASCII_ARROW_LEFT = '\u2190'
ASCII_ARROW_RIGHT = '\u2192'


class RoadObject(Object):

    def update(self):
        pass

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

    def _update(self) -> Coordinates:
        return self.position


class RoadObjectsGroup(ObjectsGroup):

    def __init__(self, objects: List[RoadObject], direction: Direction):
        super().__init__(objects)
        self.direction = direction

    @property
    def start(self) -> RoadObject:
        return self.objects[0]

    def get_intersections(self, other: "RoadObjectsGroup") -> List[Coordinates]:
        intersections = []
        other_positions = [obj.position for obj in other.objects]

        for obj in self.objects:
            if obj.position in other_positions:
                intersections.append(obj.position)

        return intersections

    @property
    def end(self) -> RoadObject:
        return self.objects[-1]

    def get_next_position(self, current: Coordinates) -> [Coordinates, None]:
        for idx, obj in enumerate(self.objects):
            if obj.position == current:
                next_idx = (idx + 1) % len(self.objects)
                return self.objects[next_idx].position

        return None
