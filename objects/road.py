from typing import List, Tuple

from objects.core import Object, ObjectsGroup
from utils import Coordinates, Direction

ASCII_ARROW_UP = '\u2191'
ASCII_ARROW_DOWN = '\u2193'
ASCII_ARROW_LEFT = '\u2190'
ASCII_ARROW_RIGHT = '\u2192'
ASCII_ARROW_UP_LEFT = '\u2196'
ASCII_ARROW_UP_RIGHT = '\u2197'
ASCII_ARROW_DOWN_LEFT = '\u2199'
ASCII_ARROW_DOWN_RIGHT = '\u2198'


class RoadObject(Object):

    def update(self):
        pass

    def __init__(self, center: Coordinates, direction: Direction):
        self.direction = direction
        super().__init__(center, self.__get_char())

    def __get_char(self) -> str:
        """
        Returns the character to be displayed on the screen.
        @return: The character to be displayed on the screen.
        """
        return {
            Direction.UP: ASCII_ARROW_UP,
            Direction.DOWN: ASCII_ARROW_DOWN,
            Direction.LEFT: ASCII_ARROW_LEFT,
            Direction.RIGHT: ASCII_ARROW_RIGHT,
            Direction.UP_LEFT: ASCII_ARROW_UP_LEFT,
            Direction.UP_RIGHT: ASCII_ARROW_UP_RIGHT,
            Direction.DOWN_LEFT: ASCII_ARROW_DOWN_LEFT,
            Direction.DOWN_RIGHT: ASCII_ARROW_DOWN_RIGHT
        }[self.direction]

    def _update(self):
        """
        Road objects don't move.
        """
        pass


class RoadObjectsGroup(ObjectsGroup):

    def __init__(self, objects: List[RoadObject]):
        super().__init__(objects)
    
    @classmethod
    def from_coordinates(cls, coordinates_list: List[Coordinates]) -> "RoadObjectsGroup":
        """
        Returns a road objects group from a list of coordinates.
        @param coordinates_list: The list of coordinates.
        @return: The road objects group.
        """
        if len(coordinates_list) < 2:
            raise ValueError("The list of coordinates must have at least two elements.")

        road_objects: List[RoadObject] = []
        segments: List[Tuple[Coordinates, Coordinates]] = []

        for i in range(len(coordinates_list) - 1):
            segments.append((coordinates_list[i], coordinates_list[i + 1]))

        for segment in segments:
            full_path = segment[0].get_path_to(segment[1])

            for i in range(len(full_path) - 1):
                road_objects.append(RoadObject(full_path[i], full_path[i].get_direction_to(full_path[i + 1])))

        return cls(road_objects)
        
    def get_direction_at_coordinate(self, coordinate: Coordinates) -> Direction:
        """
        Returns the direction of the road at the given coordinate.
        @param coordinate: The coordinate.
        @return: The direction of the road at the given coordinate.
        """
        for road_object in self.objects:
            if road_object.position == coordinate:
                return road_object.direction

        raise ValueError("The given coordinate is not on the road.")

    @property
    def start(self) -> RoadObject:
        """
        Returns the beginning of the road.
        @return: The beginning of the road.
        """
        return self.objects[0]

    @property
    def end(self) -> RoadObject:
        """
        Returns the end of the road.
        @return: The end of the road.
        """
        return self.objects[-1]
    
    def get_intersections(self, other: "RoadObjectsGroup") -> List[Coordinates]:
        """
        Returns the intersections between two road objects groups.
        @param other: The other road objects group.
        @return: The intersections between the two road objects groups.
        """
        intersections = []
        other_positions = [obj.position for obj in other.objects]

        for obj in self.objects:
            if obj.position in other_positions:
                intersections.append(obj.position)

        return intersections

    def get_next_position(self, current: Coordinates) -> [Coordinates, None]:
        """
        Returns the next position of the car based on the direction of the road.
        @param current: The current position.
        @return: The next position of the car based on the direction of the road.
        """
        for idx, obj in enumerate(self.objects):
            if obj.position == current:
                next_idx = (idx + 1) % len(self.objects)
                return self.objects[next_idx].position

        return None
