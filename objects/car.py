from termcolor import colored

import game_globals
from objects.core import Object
from objects.junction import JunctionTrafficLightColor
from objects.road import RoadObject, RoadObjectsGroup
from utils import Coordinates, get_random_color_name


class CarObject(Object):

    def __init__(self, center: Coordinates, color: str):
        super().__init__(center, colored("@", color))
        self.active_road: [RoadObjectsGroup, None] = None

    @classmethod
    def create_at_start_of_road(cls, road: RoadObjectsGroup):
        """
        Creates a car at the start of the road
        @param road: The road where the car will be created
        """
        car = cls(road.start.position.clone(), get_random_color_name())
        car.active_road = road
        return car

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
            current_direction = self.active_road.get_direction_at_coordinate(self.position)
            if junction.direction != current_direction:
                return
            elif junction.color != JunctionTrafficLightColor.GREEN:
                return
            
        car = game_globals.GAME.get_car(roads_next_position)
        if car:
            return

        self.position = roads_next_position

