import itertools
import random
import time
from typing import List

from board import Board
from objects.car import CarObject
from objects.junction import JunctionObject, JunctionTrafficLightColor
from objects.road import RoadObject, RoadObjectsGroup
from objects.wall import WallObject
from utils import Coordinates, clear_screen, Direction, get_random_color_name


class Game:

    def __init__(self, board: Board, frame_rate_sec: float):
        self.ticks_until_next_car_spawn = random.randint(5, 10)
        self.max_cars = 10
        self.frame_rate_sec = frame_rate_sec
        self.board = board
        self.static_classes = [WallObject, RoadObject]

        self.__create_initial_objects()

    def __create_initial_objects(self):
        """
        Creates the initial objects on the board.
        """
        self.board.single_objects.extend(self.__create_borders())

        self.roads = self.__create_roads()
        self.board.object_groups.extend(self.roads)

        self.cars = self.__create_cars()
        self.board.single_objects.extend(self.cars)

        self.junctions = self.__identify_junctions(self.roads)
        self.board.single_objects.extend(self.junctions)

    def __create_borders(self) -> List[WallObject]:
        """
        Creates the borders of the board.
        @return: List of WallObjects
        """
        upper_wall = [
            WallObject(Coordinates(x, 0)) for x in range(self.board.map_size_x)
        ]

        lower_wall = [
            WallObject(Coordinates(x, self.board.map_size_y - 1)) for x in range(self.board.map_size_x)
        ]

        left_wall = [
            WallObject(Coordinates(0, y)) for y in range(self.board.map_size_y)
        ]

        right_wall = [
            WallObject(Coordinates(self.board.map_size_x - 1, y)) for y in range(self.board.map_size_y)
        ]

        return [*upper_wall, *lower_wall, *left_wall, *right_wall]

    def __create_roads(self) -> List[RoadObjectsGroup]:
        """
        Creates the roads of the board.
        @return: List of RoadObjectsGroup
        """
        center_horizontal_road_1 = RoadObjectsGroup([
            RoadObject(Coordinates(x, self.board.map_size_y // 2), Direction.RIGHT) for x in range(1, self.board.map_size_x - 1)
        ], Direction.RIGHT)

        center_vertical_road_1 = RoadObjectsGroup([
            RoadObject(Coordinates(self.board.map_size_x // 2, y), Direction.DOWN) for y in range(1, self.board.map_size_y - 1)
        ], Direction.DOWN)

        return [center_horizontal_road_1, center_vertical_road_1]

    def __create_cars(self) -> List[CarObject]:
        """
        Creates the cars on the board.
        @return: List of CarObjects
        """
        roads = [group for group in self.board.object_groups if isinstance(group, RoadObjectsGroup)]

        red_car = self.__create_car(roads[0])
        blue_car = self.__create_car(roads[1])

        return [red_car, blue_car]

    def __create_car(self, road: RoadObjectsGroup) -> CarObject:
        """
        Creates a car on the board.
        :param road: The road the car is on.
        @return: The created car.
        """
        car = CarObject(road.start.position.clone(), get_random_color_name())
        car.active_road = road

        return car

    def __identify_junctions(self, roads: List[RoadObjectsGroup]) -> List[JunctionObject]:
        """
        Identifies the junctions on the board.
        :param roads: The roads on the board.
        @return: The identified junctions.
        """
        junctions: JunctionObject = []

        for road_a, road_b in itertools.combinations(roads, 2):
            intersections = road_a.get_intersections(road_b)

            for intersection in intersections:
                junctions.append(JunctionObject(intersection.clone(), [road_a.direction, road_b.direction]))

        return junctions

    def __draw(self):
        """
        Draws the board.
        """
        for y in range(self.board.map_size_y):
            for x in range(self.board.map_size_x):
                obj = self.board.get_object_at(Coordinates(x, y))
                if obj is None:
                    print(" ", end=" ")
                else:
                    print(obj.char, end=" ")
            print()

    def __print_meta(self):
        """
        Prints the meta data of the board.
        """
        print("Map size: {}x{}".format(self.board.map_size_x, self.board.map_size_y))
        print("Frame rate: {}s".format(self.frame_rate_sec))

    def get_junction(self, coordinates: Coordinates) -> [JunctionObject, None]:
        """
        Gets the junction at the given coordinates.
        :param coordinates: The coordinates of the junction.
        @return: The junction at the given coordinates or None if there is no junction at the given coordinates.
        """
        junctions_at_coordinate = [junction for junction in self.junctions if junction.position == coordinates]
        if len(junctions_at_coordinate) == 0:
            return None

        return junctions_at_coordinate[0]

    def get_car(self, coordinates: Coordinates) -> [JunctionObject, None]:
        """
        Gets the car at the given coordinates.
        :param coordinates: The coordinates of the car.
        @return: The car at the given coordinates or None if there is no car at the given coordinates.
        """
        cars_at_coordinate = [car for car in self.cars if car.position == coordinates]
        if len(cars_at_coordinate) == 0:
            return None

        return cars_at_coordinate[0]

    def __spawn_cars_if_needed(self):
        """
        Spawns cars if needed.
        """
        if len(self.cars) < self.max_cars:
            if self.ticks_until_next_car_spawn == 0:
                road = random.choice(self.roads)
                occupying_car = self.get_car(road.start.position)
                if occupying_car is None:
                    self.cars.append(self.__create_car(road))
                    self.board.single_objects.append(self.cars[-1])
                    self.ticks_until_next_car_spawn = random.randint(5, 10)
            else:
                self.ticks_until_next_car_spawn -= 1

    def run(self):
        """
        Runs the simulation.
        """
        while True:
            self.__spawn_cars_if_needed()

            for obj in self.board.all_objects:
                if any([isinstance(obj, cls) for cls in self.static_classes]):
                    continue

                obj.update()

            clear_screen()
            self.__draw()

            print("\n")
            self.__print_meta()

            time.sleep(self.frame_rate_sec)
