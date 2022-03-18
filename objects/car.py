import random

from termcolor import colored

import game_globals
from objects.core import Object
from objects.road import RoadObject
from utils import Coordinates, Vector


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
