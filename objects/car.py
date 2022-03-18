from termcolor import colored

import game_globals
from objects.core import Object
from objects.junction import JunctionState
from objects.road import RoadObject, RoadObjectsGroup
from utils import Coordinates


class CarObject(Object):

    def __init__(self, center: Coordinates, color: str):
        super().__init__(center, colored("@", color))
        self.active_road: [RoadObjectsGroup, None] = None

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

    def __get_possible_moves(self):
        if not self.active_road:
            return

        if self.position == self.active_road.end.position:
            return self.active_road.start

    def update(self):
        if not self.active_road:
            return

        roads_next_position = self.active_road.get_next_position(self.position)

        junction = game_globals.GAME.get_junction(roads_next_position)
        if junction:
            if junction.state == JunctionState.RED:
                return

        car = game_globals.GAME.get_car(roads_next_position)
        if car:
            return

        self.position = roads_next_position

