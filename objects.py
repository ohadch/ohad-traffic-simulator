import random
from typing import List

from termcolor import colored

import game_globals
from utils import Coordinates, Vector, Move


class Object:

    def __init__(self, center: Coordinates, span: List[Coordinates], char: str):
        self.moves: List[Move] = []
        self.center = center
        self.span = span
        self.vector: Vector = Vector(0, 0)
        self.char: str = char

    def speed(self):
        return self.vector.speed()

    def stop(self):
        self.vector.stop()

    def update(self):
        current_position = self.center
        new_position = self._get_next_position()

        if new_position == current_position:
            return

        self.moves.append(Move(current_position, new_position))
        self.center = new_position

    def _get_next_position(self) -> Coordinates:
        return self.center


class WallObject(Object):

    def __init__(self, center: Coordinates, span: List[Coordinates]):
        super().__init__(center, span, "#")

    def _get_next_position(self) -> Coordinates:
        return self.center


class RoadObject(Object):

    def __init__(self, center: Coordinates, span: List[Coordinates], char: str):
        super().__init__(center, span, char)

    def _get_next_position(self) -> Coordinates:
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

    def __start_movement(self):
        neighbors = self.__get_neighbors()
        coordinates_of_neighboring_roads = [cors for cors, obj in neighbors if isinstance(obj, RoadObject)]
        return random.choice(coordinates_of_neighboring_roads)

    def __continue_movement(self):
        next_by_vector = self.get_next_by_vector()

        neighbors = self.__get_neighbors()
        coordinates_of_neighboring_roads = [cors for cors, obj in neighbors if isinstance(obj, RoadObject)]

        if next_by_vector in coordinates_of_neighboring_roads:
            return next_by_vector
        else:
            self.stop()

    def _get_next_position(self) -> Coordinates:
        if self.speed() == 0:
            return self.__start_movement()
        else:
            return self.__continue_movement()
