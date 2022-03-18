import random
from enum import Enum
from typing import List

from termcolor import colored

from objects.core import Object
from utils import Coordinates, Direction

ASCII_ARROW_UP = '\u2191'
ASCII_ARROW_DOWN = '\u2193'
ASCII_ARROW_LEFT = '\u2190'
ASCII_ARROW_RIGHT = '\u2192'


class JunctionTrafficLightColor(Enum):
    RED = "red"
    GREEN = "green"


class JunctionObject(Object):
    __char = "*"

    def __init__(self, position: Coordinates, possible_directions: List[Direction]):
        self.possible_directions: List[Direction] = possible_directions
        self.direction: Direction = random.choice(self.possible_directions)
        self.color = JunctionTrafficLightColor.GREEN
        Object.__init__(self, position, self.__get_char_by_state())
        self.ticks_until_flip = 0

    def __get_char_by_state(self):
        """
        Returns the character to be displayed on the screen based on the current state of the object.
        :return: The character to be displayed on the screen.
        """
        if self.color == JunctionTrafficLightColor.RED:
            return colored("*", self.color.value)

        if self.direction == Direction.UP:
            return colored(ASCII_ARROW_UP, self.color.value)
        elif self.direction == Direction.DOWN:
            return colored(ASCII_ARROW_DOWN, self.color.value)
        elif self.direction == Direction.LEFT:
            return colored(ASCII_ARROW_LEFT, self.color.value)
        elif self.direction == Direction.RIGHT:
            return colored(ASCII_ARROW_RIGHT, self.color.value)

    def update(self):
        """
        Updates the object.
        """
        if self.ticks_until_flip > 0:
            self.ticks_until_flip -= 1
        else:
            self.direction = random.choice([foo for foo in self.possible_directions if foo != self.direction])
            self.color = random.choice(list(JunctionTrafficLightColor))
            self.ticks_until_flip = random.randint(5, 15)

        self.char = self.__get_char_by_state()
