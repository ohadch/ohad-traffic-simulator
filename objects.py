import random
from typing import List

from termcolor import colored

import game_globals
from utils import Coordinates, Vector


class Object:

    def __init__(self, center: Coordinates, span: List[Coordinates], char: str):
        self.center = center
        self.span = span
        self.vector: Vector = Vector(0, 0)
        self.char: str = char

    def speed(self):
        return self.vector.speed()

    def stop(self):
        self.vector.stop()

    def update(self):
        self._update_vector()

        for cors in self.span:
            cors.update(
                vector=self.vector,
            )

    def _update_vector(self) -> Vector:
        return Vector(0, 0)


class WallObject(Object):

    def __init__(self, center: Coordinates, span: List[Coordinates]):
        super().__init__(center, span, "#")

    def _update_vector(self) -> Coordinates:
        return self.center


class RoadObject(Object):

    def __init__(self, center: Coordinates, span: List[Coordinates], char: str):
        super().__init__(center, span, char)

    def _update_vector(self) -> Coordinates:
        return self.center


class CarObject(Object):

    def __init__(self, center: Coordinates, color: str):
        super().__init__(center, [center], colored("@", color))

    def __get_neighbors(self):
        return [
            [Coordinates(self.center.x + 1, self.center.y), game_globals.BOARD.get_object_at(
                Coordinates(self.center.x + 1, self.center.y))],
            [Coordinates(self.center.x - 1, self.center.y), game_globals.BOARD.get_object_at(
                Coordinates(self.center.x - 1, self.center.y))],
            [Coordinates(self.center.x, self.center.y + 1), game_globals.BOARD.get_object_at(
                Coordinates(self.center.x, self.center.y + 1))],
            [Coordinates(self.center.x, self.center.y - 1), game_globals.BOARD.get_object_at(
                Coordinates(self.center.x, self.center.y - 1))],
        ]

    def get_next_by_vector(self):
        if self.vector.speed() == 0:
            return self.center
        else:
            return Coordinates(self.center.x + self.vector.dx, self.center.y + self.vector.dy)

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
                dx=destination.x - self.center.x,
                dy=destination.y - self.center.y
            )
        else:
            next_by_vector = self.get_next_by_vector()

            if next_by_vector not in coordinates_of_neighboring_roads:
                self.vector = Vector(0, 0)
