import random
from typing import List

from termcolor import colored

import game_globals
from utils import Coordinates, Vector, Direction

ASCII_ARROW_UP = '\u2191'
ASCII_ARROW_DOWN = '\u2193'
ASCII_ARROW_LEFT = '\u2190'
ASCII_ARROW_RIGHT = '\u2192'


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


class WallObject(Object):

    def __init__(self, center: Coordinates):
        super().__init__(center, "#")

    def _update_vector(self) -> Coordinates:
        return self.position


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


class CarObject(Object):

    def __init__(self, center: Coordinates, color: str):
        super().__init__(center, colored("@", color))

    def __get_neighbors(self):
        return [
            [Coordinates(self.position.x + 1, self.position.y), game_globals.BOARD.get_object_at(
                Coordinates(self.position.x + 1, self.position.y))],
            [Coordinates(self.position.x - 1, self.position.y), game_globals.BOARD.get_object_at(
                Coordinates(self.position.x - 1, self.position.y))],
            [Coordinates(self.position.x, self.position.y + 1), game_globals.BOARD.get_object_at(
                Coordinates(self.position.x, self.position.y + 1))],
            [Coordinates(self.position.x, self.position.y - 1), game_globals.BOARD.get_object_at(
                Coordinates(self.position.x, self.position.y - 1))],
        ]

    def is_in_junction(self):
        neighbors = self.__get_neighbors()
        return len([cors for cors, obj in neighbors if isinstance(obj, RoadObject)]) > 2

    def _update_vector(self):
        neighbors = self.__get_neighbors()
        coordinates_of_neighboring_roads = [cors for cors, obj in neighbors if isinstance(obj, RoadObject)]
        speed = self.speed()

        if speed == 0 or self.is_in_junction():
            destination = random.choice(coordinates_of_neighboring_roads)

            self.vector = Vector(
                dx=destination.x - self.position.x,
                dy=destination.y - self.position.y
            )
        else:
            next_by_vector = Coordinates(self.position.x + self.vector.dx, self.position.y + self.vector.dy)

            if next_by_vector not in coordinates_of_neighboring_roads:
                self.vector = Vector(0, 0)
