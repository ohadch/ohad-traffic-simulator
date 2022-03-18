from termcolor import colored

import game_globals
from objects.core import Object
from objects.junction import JunctionTrafficLightColor
from objects.road import RoadObject, RoadObjectsGroup
from utils import Coordinates


class CarObject(Object):

    def __init__(self, center: Coordinates, color: str):
        super().__init__(center, colored("@", color))
        self.active_road: [RoadObjectsGroup, None] = None

    def __get_neighbors(self):
        """
        Returns a list of tuples with the coordinates and the object in the cell of the neighbors
        @return: A list of tuples with the coordinates and the object in the cell of the neighbors
        """
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
        """
        Returns True if the car is in a junction
        @return: True if the car is in a junction, False otherwise
        """
        neighbors = self.__get_neighbors()
        return len([cors for cors, obj in neighbors if isinstance(obj, RoadObject)]) > 2

    def update(self):
        """
        Updates the car's position
        """
        if not self.active_road:
            return

        roads_next_position = self.active_road.get_next_position(self.position)

        junction = game_globals.GAME.get_junction(roads_next_position)
        if junction:
            if junction.direction != self.active_road.direction:
                return
            elif junction.color != JunctionTrafficLightColor.GREEN:
                return
            
        car = game_globals.GAME.get_car(roads_next_position)
        if car:
            return

        self.position = roads_next_position

