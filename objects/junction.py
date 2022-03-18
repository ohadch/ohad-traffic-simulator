from enum import Enum

from termcolor import colored

from objects.core import Object
from utils import Coordinates


class JunctionState(Enum):
    RED = "RED"
    GREEN = "GREEN"


class JunctionObject(Object):
    __char = "*"

    def __get_char_by_state(self):
        if self.state == JunctionState.RED:
            return colored(self.__char, "red")
        else:
            return colored(self.__char, "green")

    def update(self):
        pass

    def __init__(self, position: Coordinates):
        self.state: JunctionState = JunctionState.GREEN
        Object.__init__(self, position, self.__get_char_by_state())


